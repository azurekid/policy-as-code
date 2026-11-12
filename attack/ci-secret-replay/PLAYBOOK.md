# SOC demonstration playbook — "wfx" Azure CI secret-stealer

A facilitator script for demonstrating the November 2026 "wfx" GitHub Actions
secret-stealer (Azure-scoped) to SOC analysts, and for turning each stage into a
detection use-case. Pairs with [`SETUP.md`](SETUP.md) and
[`README.md`](README.md).

> Scope reminder: this replay is **synthetic and loopback-only**. It demonstrates
> the *detection-relevant shape* (scrape → use → exfiltrate). It does **not**
> perform real Azure authentication, OIDC escalation, Graph calls, federation
> persistence, external exfiltration, or log deletion. Those stages are covered
> as detection content, not executed.

## Audience and objectives

| Audience | Objective |
| --- | --- |
| SOC analysts / threat hunters | Recognize the attack chain and the high-signal indicators; validate detections. |
| Detection engineers | Author and tune GitHub + Entra/Key Vault analytics using the signals below. |
| Incident responders | Understand why secret rotation alone does not evict the attacker. |

Target duration: **45–60 minutes** (15 min brief, 15 min live replay, 20 min
detection workshop, 5 min wrap-up).

## The attack chain (brief — 15 min)

Walk through the campaign flow (sources: Aikido, Endor Labs, SafeDep):

1. **Initial access** — stolen GitHub credentials (overlap with October
   "GhostAction" wave) are used to write to repositories.
2. **Probe** — a PR titled `docs: dependency audit notes` from a `wfx-docs`
   branch confirms write access.
3. **Inject** — one of three variants adds a ~1,500-line shell payload (workflow
   injection, throwaway workflow, or an npm `postinstall` hook).
4. **Collect** — an injected step sets `WF_SECRETS="${{ toJSON(secrets) }}"`,
   handing *all* Actions secrets/vars to the payload, which also reads cloud and
   tool credential files on the runner.
5. **Escalate** — requests an OIDC JWT, exchanges it for cloud access, obtains a
   Microsoft Graph token.
6. **Persist (Azure)** — adds an Entra application **federated identity
   credential** named `wfx-ci-*` trusting the repo → **survives secret rotation**.
7. **Exfiltrate** — gzipped tarball to `…:8080/exfil` (plus GitHub-infra
   channels), with a campaign token in `WF_CTOKEN`.
8. **Conceal** — reverts the commit and deletes the workflow run → a **missing
   run number** is the most reliable execution marker.

Show the defanged injected steps in
[`reference/wfx-injected-steps.yml.txt`](reference/wfx-injected-steps.yml.txt).

## Live replay (15 min)

Run from the repository root. Narrate each step.

### Step 1 — prove the guardrails

```bash
python3 -B -m unittest discover -s attack/ci-secret-replay -p 'test_*.py'
```

Point out the tests that enforce **synthetic-only** credentials, **loopback-only**
destinations, and **redaction**. This is why the lab is safe to run anywhere.

### Step 2 — run the full chain

```bash
python3 -B attack/ci-secret-replay/replay.py
```

Talking points on the output:
- Three `synthetic-credential-scraped` events = three collection vectors
  (env-file, credential-file, `toJSON(secrets)` dump).
- `also_collected` lists other secret *names* only — "collect everything, use
  Azure" without exposing unrelated secret values.
- `use.authenticated: true` / `mode: loopback` — the scraped client secret was
  exchanged at a **mock** token endpoint, not Entra.
- `exfil.delivered: true` — a gzipped archive was POSTed to a **loopback** sink
  carrying the `WF_CTOKEN` header.
- `secret: "[REDACTED]"` everywhere — values never leave the process.
- The final `metadata-only` event shows `azureProfile.json` (IDs only) **cannot**
  authenticate — identifiers are not credentials.

### Step 3 — show the primary env-dump vector explicitly

```bash
cd attack/ci-secret-replay
WF_SECRETS="$(cat fixtures/secrets-dump.json)" python3 -B replay.py
```

This is the exact mechanic to detect: a single env var receiving the whole
secrets object.

### Step 4 (optional) — fail-closed demo

In a scratch copy, change the fake secret in a fixture to any other string and
re-run; the replay exits non-zero with
`Replay failed: missing, invalid, or non-synthetic inputs`. This proves the lab
cannot be repurposed to handle real credentials.

## Detection workshop (20 min)

Have analysts build/validate these in your SIEM. Full queries are in
[`README.md`](README.md#detection-use-cases).

### Use-case 1 — secrets dump in a workflow (Collect)

- **Signal:** a workflow/commit introducing `toJSON(secrets)` or `toJSON(vars)`
  assigned into one env var; env names `WF_SECRETS`/`WF_VARS`/`WF_CALLBACK`/
  `WF_CTOKEN`; step names like `Pass runtime`, `Restore cache <id>`.
- **Source:** repo content scanning / push events / PR diffs.
- **Why it works:** legitimate workflows reference individual secrets by name.

### Use-case 2 — probe + concealment (Access / Conceal)

- **Signal:** PR title `docs: dependency audit notes`, branch `wfx-docs`;
  `workflows.delete` in the GitHub audit log; **missing run numbers** on an
  attacker commit.
- **Source:** GitHub audit log / Actions run history.

### Use-case 3 — Azure federation persistence (Persist) — the key one

- **Signal:** a new federated identity credential added to an Entra application
  (`Update application`/`Update service principal`, modified property
  `federatedIdentityCredentials`), especially names like `wfx-ci-*`.
- **Source:** Entra `AuditLogs` → Sentinel. KQL in the README.
- **Why it matters:** this is why **rotating secrets does not help** — the trust
  survives. Alert on unexpected issuer/subject/initiator, not the name alone.

### Use-case 4 — new trust used + resource access (Use)

- **Signal:** federation change followed by a service-principal sign-in
  (`AADServicePrincipalSignInLogs` with a `FederatedCredentialId`), then Key Vault
  `SecretGet` by an identity outside its normal pattern.
- **Source:** Entra SP sign-in logs + Key Vault audit diagnostics.

### Correlation exercise

Chain **federation change → first SP sign-in → resource access** within a short
window. Discuss that App object ID, client/App ID, and SP object ID are different
identifiers that must be resolved before joining, and that subscription Activity
Log alone misses these directory/data-plane events.

## Wrap-up (5 min)

- **Rotation is not remediation.** A `wfx-ci-*` federation trust must be audited
  and removed; issued tokens can remain valid until expiry.
- **Clean current branch ≠ safe.** Evidence lives in commit history and run-number
  gaps, not the current tree.
- **Hardening:** least-privilege `GITHUB_TOKEN`, pin actions to SHAs, restrict who
  can edit workflows / run Actions, require reviews on workflow changes, monitor
  Entra app credential changes, and scope OIDC federation subjects tightly.

## Facilitator checklist

- [ ] `SETUP.md` steps completed; `python3 --version` ≥ 3.10.
- [ ] Tests pass (`OK`, 8 tests).
- [ ] Self-contained replay shows redaction + loopback use/exfil.
- [ ] Env-dump (`WF_SECRETS`) demo shown.
- [ ] Fail-closed demo shown (optional).
- [ ] Analysts have the README KQL open for the detection workshop.
- [ ] Entra `AuditLogs`, SP sign-in logs, and Key Vault audit diagnostics are
      flowing to your workspace **before** any separately authorized live test.
