// policy-assignment.bicep
// Assigns the custom policy and gives its remediation identity ONLY the role the
// policy definition declares (Log Analytics Contributor, scoped to the target
// resource group) — NOT a blanket Contributor grant. This is the secure baseline;
// contrast with policy-assignment.VULNERABLE.bicep for the demo.

targetScope = 'managementGroup'

@description('Resource ID of the policy definition to assign')
param policyDefinitionId string

@description('Resource ID of the Log Analytics workspace parameter value')
param logAnalyticsWorkspaceId string

@description('Subscription ID that contains the target resource group — keep the grant as narrow as possible')
param remediationTargetSubscriptionId string

@description('Resource group name the remediation identity is scoped to')
param remediationTargetResourceGroupName string

@description('Location for the system-assigned identity')
param location string = 'westeurope'

var logAnalyticsContributorRoleId = '92aaf0da-9dab-42b6-94a3-d43ce8d16293'

resource policyAssignment 'Microsoft.Authorization/policyAssignments@2022-06-01' = {
  name: 'demo-diag-settings-assignment'
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    displayName: 'Demo - Deploy diagnostic settings (secure baseline)'
    policyDefinitionId: policyDefinitionId
    parameters: {
      logAnalyticsWorkspaceId: {
        value: logAnalyticsWorkspaceId
      }
    }
  }
}

// Explicit, minimal, PR-reviewable grant — scoped to ONE target resource group,
// not the whole management group/subscription, and only the role the policy
// actually needs (Log Analytics Contributor), never Contributor/Owner.
module grantRemediationRole 'modules/scoped-role-assignment.bicep' = {
  name: 'grantRemediationRole'
  scope: resourceGroup(remediationTargetSubscriptionId, remediationTargetResourceGroupName)
  params: {
    principalId: policyAssignment.identity.principalId
    roleDefinitionId: logAnalyticsContributorRoleId
    nameSeed: policyAssignment.id
  }
}

output remediationIdentityPrincipalId string = policyAssignment.identity.principalId
