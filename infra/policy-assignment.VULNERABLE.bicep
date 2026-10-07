// policy-assignment.VULNERABLE.bicep
// DEMO-ONLY: assignment uses the "automatic" portal-style broad grant pattern —
// Contributor at the FULL management group scope — instead of the narrow,
// explicit, single-resource-group grant in the secure baseline. This mirrors
// what the Azure Portal does by default when you tick "Create a Managed Identity"
// without manually tightening scope afterwards.

targetScope = 'managementGroup'

@description('Resource ID of the policy definition to assign')
param policyDefinitionId string

@description('Resource ID of the Log Analytics workspace parameter value')
param logAnalyticsWorkspaceId string

@description('Location for the system-assigned identity')
param location string = 'westeurope'

// VULNERABLE: using Contributor instead of a scoped-down built-in role.
var contributorRoleId = 'b24988ac-6180-42a0-ab88-20f7382dd24c'
var managementGroupId = managementGroup().id

resource policyAssignment 'Microsoft.Authorization/policyAssignments@2022-06-01' = {
  name: 'demo-diag-settings-assignment-vuln'
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    displayName: 'Demo - Deploy diagnostic settings (VULNERABLE variant)'
    policyDefinitionId: policyDefinitionId
    parameters: {
      logAnalyticsWorkspaceId: {
        value: logAnalyticsWorkspaceId
      }
    }
  }
}

// VULNERABLE: Contributor at the entire management group scope — every
// subscription underneath inherits exposure to this identity.
resource remediationRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(managementGroupId, policyAssignment.id, contributorRoleId)
  scope: managementGroup()
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', contributorRoleId)
    principalId: policyAssignment.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

output remediationIdentityPrincipalId string = policyAssignment.identity.principalId
