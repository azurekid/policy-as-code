// pipeline-identity.VULNERABLE.bicep
// DEMO-ONLY MISCONFIGURATION — intentionally loosened for the live demo.
// Differences from the secure baseline:
//   1. FIC subject uses a WILDCARD branch ref instead of an environment-scoped
//      exact match -> ANY branch (including attacker-created branches, if they
//      can push one or open a workflow_dispatch) can mint a token for this identity.
//   2. Pipeline identity is granted Resource Policy Contributor at MANAGEMENT GROUP
//      scope instead of a single resource group -> blast radius covers every
//      subscription under the management group.
//
// DO NOT deploy this against a real environment outside an isolated demo subscription.

targetScope = 'managementGroup'

@description('GitHub organization name')
param githubOrg string

@description('GitHub repository name')
param githubRepo string

@description('Resource group (in a subscription under this management group) where the UAMI is created')
param identitySubscriptionId string

@description('Location for the identity resource group')
param location string = 'westeurope'

var resourcePolicyContributorRoleId = '36243c78-bf99-498c-9df9-86d9f8d28608'
var uamiName = 'uami-gha-policy-pipeline-vuln'
// Computed directly so `guid()` in the role assignment's `name` property is
// calculable without depending on the module's runtime output.
var uamiResourceId = resourceId(identitySubscriptionId, 'rg-policy-pipeline', 'Microsoft.ManagedIdentity/userAssignedIdentities', uamiName)

module uamiModule 'modules/uami-and-fic.bicep' = {
  name: 'uamiAndFicVulnerable'
  scope: resourceGroup(identitySubscriptionId, 'rg-policy-pipeline')
  params: {
    location: location
    uamiName: uamiName
    githubOrg: githubOrg
    githubRepo: githubRepo
    githubEnvironment: 'none-wildcard-demo'
    // VULNERABLE: wildcard ref — trusts a token minted from ANY branch in the repo
    ficSubject: 'repo:${githubOrg}/${githubRepo}:ref:refs/heads/*'
  }
}

// VULNERABLE: Contributor-equivalent policy authority at management group scope,
// i.e. every subscription beneath it, instead of a single resource group.
resource policyContributorAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(uamiResourceId, resourcePolicyContributorRoleId)
  scope: managementGroup()
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', resourcePolicyContributorRoleId)
    principalId: uamiModule.outputs.principalId
    principalType: 'ServicePrincipal'
  }
}

output uamiClientId string = uamiModule.outputs.clientId
output ficSubject string = uamiModule.outputs.ficSubject
