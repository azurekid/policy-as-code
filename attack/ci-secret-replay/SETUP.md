# Setup guide — Azure CI secret-stealer SOC replay

This guide gets the lab running locally and (optionally) as a manual GitHub
Actions run. Everything is **synthetic and loopback-only**: no real secrets, no
Azure sign-in, no external network egress. Nothing here needs a cloud tenant or
credentials to run.

## 1. Prerequisites

| Requirement | Notes |
| --- | --- |
| Python 3.10+ | Standard library only; **no `pip install`** needed. |
| Git checkout of this repo | Run commands from the repository root unless noted. |
| (Optional) GitHub repo access | Only to dispatch the manual workflow. |

Verify Python:

```bash
python3 --version   # expect 3.10 or newer
```

No virtualenv, packages, or network access are required. The replay only reads
files under `attack/ci-secret-replay/fixtures/` and talks to a loopback
(`127.0.0.1`) mock it starts itself.

## 2. Local setup (2 minutes)

```bash
# from the repository root
cd /path/to/policy-as-code

# 1) run the test suite (proves guards + redaction work)
python3 -B -m unittest discover -s attack/ci-secret-replay -p 'test_*.py'

# 2) run the self-contained scrape -> use -> exfiltrate chain
python3 -B attack/ci-secret-replay/replay.py
```

Expected: `OK` for 8 tests, then four JSONL events — three
`synthetic-credential-scraped` (one per vector) with `secret: "[REDACTED]"`,
`use.authenticated: true`, `exfil.delivered: true`, and a final `metadata-only`
event with `authenticated: false`.

## 3. Explicit env-dump vector (the campaign's primary mechanic)

The real payload injects a step setting `WF_SECRETS="${{ toJSON(secrets) }}"`.
Reproduce that shape with the **seeded** dump (not real secrets):

```bash
cd attack/ci-secret-replay
WF_SECRETS="$(cat fixtures/secrets-dump.json)" python3 -B replay.py
```

The `toJSON(secrets):WF_SECRETS` event shows the Azure credentials extracted and
the names (only) of other secrets the payload would have collected
(`GITHUB_TOKEN`, `NPM_TOKEN`).

## 4. Optional: run as a GitHub Actions workflow

The workflow **Azure CI Secret Replay (Synthetic Only)**
(`.github/workflows/azure-secret-replay.yml`) is **manual-trigger only** and
performs no Azure login, OIDC request, or external egress.

1. Merge this branch (or push it) so the workflow is on the target branch.
2. In GitHub: **Actions → Azure CI Secret Replay (Synthetic Only) → Run workflow**.
3. Select a **reviewed** ref (the workflow checks out the ref you pick).
4. Inspect the run logs: the replay and the explicit `WF_SECRETS` demo both run.

No repository secrets or variables are required.

## 5. Safety model / guardrails

- **Synthetic-only:** every Azure credential set is compared to an exact invalid
  tuple before use; a real credential dropped into the fixtures makes the run
  fail closed.
- **Loopback-only:** `use`/`exfil` refuse any destination that is not
  `http://127.0.0.1:<port>`.
- **Redaction:** secret values never appear in stdout; the mock sink stores only
  a byte count + SHA-256 of the gzipped loot.
- **Bounded file reads:** only allowlisted files under `fixtures/`; symlinks and
  oversized files are rejected.
- **No cleanup required:** no real credential, secret store, or cloud resource is
  ever touched.

## 6. Troubleshooting

| Symptom | Cause / fix |
| --- | --- |
| `Replay failed: missing, invalid, or non-synthetic inputs` | A fixture was edited to a non-synthetic value, or a file is missing. Restore the original fixtures. |
| `Refusing non-loopback destination` | `WF_CALLBACK`/`WF_TOKEN_URL` points off-box. Leave them unset for the self-contained run. |
| `ModuleNotFoundError: mock_cloud` | Run from inside `attack/ci-secret-replay/`, or use the `discover -s` form shown above. |
| Port bind errors | The mock uses an ephemeral port on `127.0.0.1`; retry, or check for a restrictive sandbox. |

Next: see [`PLAYBOOK.md`](PLAYBOOK.md) for the step-by-step SOC demonstration.
