# Azure CI secret scrape -> use -> exfiltrate replay (SOC lab)

A safe, runnable reproduction of the detection-relevant shape of the November
2026 **"wfx" GitHub Actions secret-stealer** campaign, scoped to Azure. It lets
SOC analysts see how CI secrets are scraped and used, and build detections.

Everything here is **synthetic and loopback-only**: invalid seeded credentials,
no real GitHub/org secrets, no Azure sign-in, no OIDC request, and no external
network egress. Live Azure authentication was intentionally **not** implemented
(it was out of scope / denied for this lab). Each Azure credential set is checked
against an exact synthetic tuple before it is "used" or "exfiltrated", so the
replay fails closed if a real credential is ever dropped into the fixtures.

## What the campaign does (and what this lab reproduces)

Per [Aikido](https://www.aikido.dev/blog/compromised-github-accounts-push-ci-secret-stealer-to-tens-of-thousands-of-repositories),
[Endor Labs](https://www.endorlabs.com/learn/github-actions-supply-chain-attack-targeting-ci-secrets-at-scale)
and [SafeDep](https://safedep.io/blog/github-actions-wfx-credential-stealer),
compromised GitHub accounts probe repos (`wfx-docs` branch, PR
`docs: dependency audit notes`), inject a ~1,500-line shell payload, then revert
and delete the run. The payload runs four stages:

| Stage | Campaign behavior | This lab |
| --- | --- | --- |
| **Collect** | Dumps all Actions secrets/vars via an injected step setting `WF_SECRETS="${{ toJSON(secrets) }}"`; also reads credential files for Azure, AWS, GCP, Docker, k8s, npm, SSH, etc. | Scrapes synthetic creds from a seeded `WF_SECRETS` dump **and** from seeded credential files. |
| **Escalate** | Requests an OIDC JWT (`ACTIONS_ID_TOKEN_REQUEST_URL`), exchanges it for cloud access, obtains a Microsoft Graph token. | Not performed — no OIDC request, no real token exchange. |
| **Persist** | Adds an Entra application **federated identity credential** named `wfx-ci-*` trusting the repo; survives secret rotation. | Documented in `reference/` + detections below; not executed. |
| **Exfiltrate** | Gzipped tarball to `http://…:8080/exfil` with campaign token in `WF_CTOKEN` (plus GitHub-infra channels). | Gzips loot and POSTs to a **loopback** sink mirroring the `WF_CTOKEN` header. |
| **Conceal** | Reverts commit, deletes workflow run/logs (missing run number). | N/A (local run). |

**Credential mechanics that matter for interpretation.** Client/tenant/subscription
IDs are identifiers, not secrets. A client secret authenticates the app to Entra,
not to Azure Resource Manager directly; RBAC and Key Vault networking still apply.
A Key Vault token is not a Graph token, and subscription Contributor does not
authorize adding Entra federation credentials. GitHub does not expose existing
secret values through its API — the payload gets them only because the injected
step hands `toJSON(secrets)` into the process.

## Files

| File | Purpose |
| --- | --- |
| `fixtures/service-principal.env` | Azure `AZURE_*` env vars with invalid values (env-file vector). |
| `fixtures/azure-credentials.json` | Azure Login client-secret JSON shape, invalid (cred-file vector). |
| `fixtures/secrets-dump.json` | Seeded `toJSON(secrets)` object: `AZURE_CREDENTIALS` + extra non-Azure secret names (primary vector). |
| `fixtures/azureProfile.json` | Metadata-only counterexample: discoverable IDs do not prove access. |
| `replay.py` | Scrape -> use -> exfiltrate chain with synthetic-only guards and redaction. |
| `mock_cloud.py` | Loopback (`127.0.0.1`) stand-ins for the Entra token endpoint and exfil sink. |
| `test_replay.py` | Chain, redaction, vector parsing, loopback-only and file-boundary checks. |
| `reference/wfx-injected-steps.yml.txt` | Defanged reference of the injected `toJSON(secrets)` steps (DO NOT RUN). |
| `../../.github/workflows/azure-secret-replay.yml` | Manual workflow running the tests and replay; no Azure login. |

## Run it

Python 3.10+, no third-party packages:

```bash
# from repo root
python3 -B -m unittest discover -s attack/ci-secret-replay -p 'test_*.py'

# self-contained: starts its own loopback mock, then scrape -> use -> exfiltrate
python3 -B attack/ci-secret-replay/replay.py

# demonstrate the campaign's env-dump vector explicitly
cd attack/ci-secret-replay
WF_SECRETS="$(cat fixtures/secrets-dump.json)" python3 -B replay.py
```

Or dispatch **Azure CI Secret Replay (Synthetic Only)** (manual trigger only;
no push/PR). It checks out the selected ref, so run only reviewed refs.

Expected output: three `synthetic-credential-scraped` JSONL events (env-file,
cred-file, `toJSON(secrets)` vectors), each with `secret: "[REDACTED]"`, a
loopback `use.authenticated: true`, and `exfil.delivered: true`; then a final
`metadata-only` event with `authenticated: false`. Secret values never appear
in stdout; the loopback sink stores only a size + SHA-256 of the gzipped loot.

The replay reads only allowlisted files under its own `fixtures/`, rejects
symlinks/oversized files, refuses any non-loopback destination, and refuses
credentials that differ from the exact synthetic tuple. Keep real credentials
out of these files.

## Detection use-cases

This lab emits ordinary local output, **not** Azure/GitHub telemetry. Use the
signals below to build and test detections in your own tenant.

### GitHub Actions (Collect / Exfiltrate / Conceal)

- **High-signal:** a workflow or commit introducing `toJSON(secrets)` or
  `toJSON(vars)` assigned into one env var. Legitimate workflows reference
  individual secrets by name.
- Env var names `WF_CALLBACK`, `WF_CTOKEN`, `WF_SECRETS`, `WF_VARS`; step names
  like `Pass runtime` / `Restore cache <id>`; `actions/github-script` added to
  expose runtime tokens.
- Probe branch `wfx-docs`; PR title `docs: dependency audit notes`.
- Outbound to `:8080/exfil` (IOCs `194.150.166.244`, `18.143.168.96`).
- Deleted workflow runs / **missing run numbers** on an attacker commit
  (`workflows.delete` in the GitHub audit log) — the most reliable execution marker.

### Azure / Entra (Escalate / Persist) — the part secret rotation won't fix

Ingest Entra `AuditLogs` and service-principal sign-in logs. Hunt for a new
federated identity credential added to an application:

```kusto
AuditLogs
| where TimeGenerated > ago(7d)
| where OperationName has_any ("Update application", "Update service principal")
| mv-expand Target = TargetResources
| mv-expand Property = Target.modifiedProperties
| extend PropertyName = tostring(Property.displayName)
| where PropertyName has "federated" or tostring(Property.newValue) has "wfx-ci-"
| project TimeGenerated, OperationName, Result,
          Initiator = tostring(InitiatedBy.user.userPrincipalName),
          App = tostring(Target.displayName),
          PropertyName, NewValue = tostring(Property.newValue), CorrelationId
```

Then correlate a federation change with its first use (service-principal sign-in),
noting that `wfx-ci-*` is a name attacker-chose — alert on unexpected
issuer/subject/initiator, not the name alone:

```kusto
AADServicePrincipalSignInLogs
| where TimeGenerated > ago(7d)
| where ResultType == 0
| project TimeGenerated, AppId, ServicePrincipalName, IPAddress,
          ResourceDisplayName,
          FederatedCredentialId = tostring(column_ifexists("FederatedCredentialId",""))
| where isnotempty(FederatedCredentialId)
```

For the "use" stage against Key Vault, enable vault audit diagnostics and alert
on `SecretGet` by an identity outside its approved deployment pattern. Subscription
Activity Log alone does not capture these data-plane or directory events.

## Limits and cleanup

This replay validates the **scrape/use/exfiltrate shape only**, on loopback. It
does **not** perform real Azure authentication, OIDC escalation, Graph calls,
federation persistence, external exfiltration, or log deletion, and it does not
provision or change any cloud resource. Federation persistence must be exercised
and detected separately (see the KQL above); rotating a client secret does not
remove a `wfx-ci-*` federation trust. Nothing here requires teardown because no
real credential, secret store, or cloud resource is touched.
