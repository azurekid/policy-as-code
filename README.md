# Demo: Stealing & Abusing Azure Identities via Policy-as-Code (GitHub OIDC)

## Scenario
A platform team deploys Azure Policy (deployIfNotExists / modify) through a GitHub Actions
pipeline. The pipeline authenticates to Azure using a **user-assigned managed identity (UAMI)**
trusted via a **federated identity credential (FIC)** — no client secret, no stored credential.
The pipeline identity itself holds only **Resource Policy Contributor** (least privilege, no
`roleAssignments/write`).

The twist: every policy **assignment** with a `deployIfNotExists`/`modify` effect needs its own
**separate runtime managed identity** to perform the actual remediation deployment. That identity
is granted whatever roles the policy's `roleDefinitionIds` lists — commonly **Contributor**. The
pipeline never holds `roleAssignments/write`, but code it deploys controls what that *other*
identity does. This is the privilege-laundering seam the demo exploits.

## Folder structure

What's in `files/azure-identity-demo/` (saved to your session storage)

| File | Purpose |
| --- | --- |
| `infra/pipeline-identity.bicep` | **Secure baseline**: UAMI + FIC scoped to `environment:production` (exact match), Resource Policy Contributor only |
| `infra/pipeline-identity.VULNERABLE.bicep` | **Demo variant**: wildcard FIC subject (`ref:refs/heads/*`), Contributor at management-group scope |
| `infra/policy-definition.bicep` | Realistic custom `deployIfNotExists` policy (diagnostic settings) |
| `infra/policy-assignment.bicep` / `.VULNERABLE.bicep` | Contrast: explicit minimal remediation role vs. broad auto-granted Contributor |
| `.github/workflows/deploy-policy.yml` / `.VULNERABLE.yml` | Secure pipeline (required reviewers, pinned actions) vs. vulnerable one (any branch, mutable action tag) |
| `attack/malicious-template-injection.json` | The attacker payload — injects an Owner role assignment, laundered through the remediation identity |
| `attack/attack-walkthrough.md` | Full live-demo script: setup, attack steps, reset commands, closing mitigation slide |


## Two configurations to contrast

| | Secure baseline | Vulnerable demo variant |
|---|---|---|
| FIC subject | `repo:org/repo:environment:production` (exact match) | `repo:org/repo:ref:refs/heads/*` (wildcard — any branch) |
| GitHub Environment protection | Required reviewers + restricted to `main` | None |
| Pipeline identity scope | Resource Policy Contributor at **one resource group's management scope only** | Resource Policy Contributor at **management group** |
| Remediation MI role grant | Explicit, minimal (e.g. `Log Analytics Contributor`), scoped to target RG, reviewed in PR diff | `Contributor` at management group scope, auto-expanded by a "helper" policy initiative |
| Branch protection on policy repo | Required PR review, no direct push to `main` | Direct push allowed / stale unpinned third-party Action |

1. Run the secure baseline first to show "this looks airtight, OIDC, no secrets, least privilege."
2. Switch to the vulnerable variant to show how a single loosened control (wildcard FIC subject,
   or an unpinned/compromised Action in the workflow) reopens the exact same escalation path from
   earlier in the talk this time laundered through a CI/CD pipeline instead of a human.
