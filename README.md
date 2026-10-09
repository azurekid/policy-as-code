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
| `.github/workflows/deploy-identity.yml` | Manually bootstrap the secure pipeline identity |
| `.github/workflows/deploy-policy.yml` | Deploy the secure policy definition, then its assignment and scoped remediation role |
| `attack/malicious-template-injection.json` | The attacker payload — injects an Owner role assignment, laundered through the remediation identity |
| `attack/attack-walkthrough.md` | Full live-demo script: setup, attack steps, reset commands, closing mitigation slide |


## Two configurations to contrast

| | Secure baseline | Vulnerable demo variant |
|---|---|---|
| FIC subject | `repo:org/repo:environment:production` (exact match) | `repo:org/repo:ref:refs/heads/*` (wildcard — any branch) |
| GitHub Environment protection | Required reviewers + restricted to `main` | None |
| Pipeline identity scope | Resource Policy Contributor at **subscription scope** in the identity template; management-group access must be provisioned separately for policy deployment | Resource Policy Contributor at **management group** |
| Remediation MI role grant | Explicit, minimal (e.g. `Log Analytics Contributor`), scoped to target RG, reviewed in PR diff | `Contributor` at management group scope, auto-expanded by a "helper" policy initiative |
| Branch protection on policy repo | Required PR review, no direct push to `main` | Direct push allowed / stale unpinned third-party Action |

1. Run the secure baseline first to show "this looks airtight, OIDC, no secrets, least privilege."
2. Switch to the vulnerable variant to show how a single loosened control (wildcard FIC subject,
   or an unpinned/compromised Action in the workflow) reopens the exact same escalation path from
   earlier in the talk this time laundered through a CI/CD pipeline instead of a human.

## Deploying with GitHub Actions

The workflows deploy only the secure Bicep templates, never the `.VULNERABLE`
variants or attack payloads. Both workflows run only from `main` and use OIDC
with commit-pinned actions. No client secrets are needed.

### Environments and variables

Create `production` and `production-bootstrap` GitHub environments. Configure
required reviewers and restrict deployment branches to `main` on **both**
environments; these protections must be configured in repository settings.
Protect `main` with required PR reviews, especially for workflow and Bicep changes.

Set the following repository-level Actions variables:

| Variable | Value |
| --- | --- |
| `AZURE_TENANT_ID` | Azure tenant ID |
| `AZURE_SUBSCRIPTION_ID` | Subscription containing the pipeline identity |
| `MANAGEMENT_GROUP_ID` | Management group containing the policy definition and assignment |
| `LOG_ANALYTICS_WORKSPACE_ID` | Full resource ID of an existing Log Analytics workspace |
| `REMEDIATION_TARGET_SUBSCRIPTION_ID` | Subscription containing the remediation target RG |
| `REMEDIATION_TARGET_RESOURCE_GROUP` | Existing RG to receive the remediation role grant |
| `AZURE_LOCATION` | Optional deployment/identity location; defaults to `westeurope` |
| `IDENTITY_RESOURCE_GROUP` | Optional identity RG name; defaults to `rg-policy-pipeline` |

Set `AZURE_CLIENT_ID` **separately on each environment**:

- `production-bootstrap`: an independently provisioned bootstrap identity with
  an exact federated subject
  `repo:<owner>/<repo>:environment:production-bootstrap`. It must already exist
  before either workflow can use it. Grant it resource-group, managed-identity,
  federated-credential, and deployment management permissions in the identity
  subscription, plus permission to create the template's subscription role
  assignment. For policy assignment deployment it also needs policy assignment
  and deployment permissions at the management group, and deployment and role
  assignment permissions at the remediation target RG. Scope RBAC administration
  narrowly and use role-assignment conditions where possible.
- `production`: the `uamiClientId` output of the identity deployment. Its FIC
  trusts exactly `repo:<owner>/<repo>:environment:production`. The template
  grants Resource Policy Contributor at subscription scope, **not** management
  group scope. An administrator must separately grant Resource Policy Contributor
  at the configured management group so it can deploy the policy definition.
  Do not grant this identity RBAC administration permissions.

Environment-scoped tenant/subscription variables may override the repository
values if the bootstrap identity uses a different login subscription.

### Deployment order

1. Provision the bootstrap identity and environment protections out of band.
2. Run **Deploy Pipeline Identity** manually from `main`. It creates the
   identity RG, UAMI, production FIC, and subscription policy-contributor grant.
   The final step prints the template outputs, including `uamiClientId`.
3. Set the `production` environment's `AZURE_CLIENT_ID` to that output and grant
   its management-group policy permissions as described above.
4. Run **Deploy Policy** manually from `main`, or push a change to its workflow
   or secure policy templates. The production job deploys the definition; the
   separately approved bootstrap job then deploys the assignment and explicit
   RG-scoped Log Analytics Contributor grant using the definition's output ID.

The workspace and remediation target RG must already exist, and the target
subscription must belong to the selected management group's hierarchy. The
workflows build the Bicep templates before deployment and serialize runs to
avoid overlapping updates. They do not create remediation tasks for existing
noncompliant resources; trigger those separately when needed.
