// modules/uami-and-fic.bicep
// Creates the user-assigned managed identity and its federated identity credential.
// `ficSubject` is passed in by the caller so the secure vs. vulnerable top-level
// templates can control exactly how tight (or loose) the trust is.

@description('Location for the identity')
param location string

@description('Name to give the user-assigned managed identity')
param uamiName string = 'uami-gha-policy-pipeline'

@description('GitHub organization name (used only for naming/tags)')
param githubOrg string

@description('GitHub repository name (used only for naming/tags)')
param githubRepo string

@description('GitHub environment name (used only for naming/tags)')
param githubEnvironment string

@description('Exact subject claim the federated credential will trust, e.g. repo:org/repo:environment:production')
param ficSubject string

resource uami 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: uamiName
  location: location
  tags: {
    purpose: 'github-actions-policy-pipeline'
    repo: '${githubOrg}/${githubRepo}'
    environment: githubEnvironment
  }
}

resource fic 'Microsoft.ManagedIdentity/userAssignedIdentities/federatedIdentityCredentials@2023-01-31' = {
  parent: uami
  name: 'gha-${githubEnvironment}'
  properties: {
    issuer: 'https://token.actions.githubusercontent.com'
    audiences: [
      'api://AzureADTokenExchange'
    ]
    subject: ficSubject
  }
}

output clientId string = uami.properties.clientId
output principalId string = uami.properties.principalId
output resourceId string = uami.id
output ficSubject string = fic.properties.subject
