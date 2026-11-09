# Source inventory

Snapshot: 9 November 2026. All 61 repositories returned by the public azurekid repository API were inventoried, including forks. 59 public READMEs were retrieved. Private repositories were not accessed. README review does not establish that code or attack paths execute as documented.

azurehacking.com and www.azurehacking.com failed DNS resolution from this environment. The four further-reading URLs below were found in BlackCat's README, not directly read. Microsoft Learn support claims are based on returned search excerpts, not full-page retrieval.

Important qualification: policy-as-code's README mentions an Owner-role payload and a Contributor remediation identity. Contributor alone cannot create role assignments. This deck does not claim that escalation works, and uses a harmless action within verified effective grants. It also does not assume wildcard federation matching is universally supported.

## Complete repository inventory

| Repository | Attribution | Evidence | Public description | Presentation role |
|---|---|---|---|---|
| [1Password-Sentinel](https://github.com/azurekid/1Password-Sentinel) | azurekid project | Metadata only | Data integration for 1Password to Microsoft Sentinel | Metadata-only: 1Password to Sentinel integration |
| [AADInternals](https://github.com/azurekid/AADInternals) | Upstream fork | README reviewed | AADInternals PowerShell module for administering Azure AD and Office 365 | Upstream fork / supporting reference; not claimed as original authorship |
| [AgentTrap](https://github.com/azurekid/AgentTrap) | azurekid project | README reviewed | No public description | AgentLens defensive inspection platform |
| [AzShortLink](https://github.com/azurekid/AzShortLink) | azurekid project | README reviewed | No public description | Supporting project context; not asserted to be an identity attack tool |
| [azure-docs](https://github.com/azurekid/azure-docs) | Upstream fork | README reviewed | Open source documentation of Microsoft Azure | Upstream fork / supporting reference; not claimed as original authorship |
| [Azure-Lighthouse-samples](https://github.com/azurekid/Azure-Lighthouse-samples) | Upstream fork | README reviewed | Provide samples for understanding managed service solutions | Upstream fork / supporting reference; not claimed as original authorship |
| [azure-opt](https://github.com/azurekid/azure-opt) | azurekid project | README reviewed | Microsodft Azure - One Time Password solution | Supporting project context; not asserted to be an identity attack tool |
| [azure-orphan-resources](https://github.com/azurekid/azure-orphan-resources) | Upstream fork | README reviewed | Centralize orphan resources in Azure environments | Upstream fork / supporting reference; not claimed as original authorship |
| [azure-powershell](https://github.com/azurekid/azure-powershell) | Upstream fork | README reviewed | Microsoft Azure PowerShell | Upstream fork / supporting reference; not claimed as original authorship |
| [azure-resource-manager-schemas](https://github.com/azurekid/azure-resource-manager-schemas) | Upstream fork | README reviewed | Schemas used to author and validate Resource Manager Templates | Upstream fork / supporting reference; not claimed as original authorship |
| [Azure-Sentinel](https://github.com/azurekid/Azure-Sentinel) | Upstream fork | README reviewed | Cloud-native SIEM for intelligent security analytics for your entire enterprise. | Upstream fork / supporting reference; not claimed as original authorship |
| [Azure-Stencils](https://github.com/azurekid/Azure-Stencils) | azurekid project | README reviewed | No public description | Supporting project context; not asserted to be an identity attack tool |
| [azurekid](https://github.com/azurekid/azurekid) | azurekid project | README reviewed | No public description | Presenter profile and project attribution |
| [AzurePermissionInsight](https://github.com/azurekid/AzurePermissionInsight) | Upstream fork | README reviewed | No public description | Upstream fork / supporting reference; not claimed as original authorship |
| [Bio-Compliancy](https://github.com/azurekid/Bio-Compliancy) | Upstream fork | README reviewed | No public description | Upstream fork / supporting reference; not claimed as original authorship |
| [blackcat](https://github.com/azurekid/blackcat) | azurekid project | README reviewed | BlackCat is a PowerShell module designed to validate the security of Microsoft Azure. It provides a set of functions to identify potential security holes. | Authorized Azure/Entra security validation |
| [blog](https://github.com/azurekid/blog) | azurekid project | README reviewed | No public description | Supporting project context; not asserted to be an identity attack tool |
| [bluemountainbank](https://github.com/azurekid/bluemountainbank) | azurekid project | README reviewed | No public description | Supporting project context; not asserted to be an identity attack tool |
| [bluemountaintravel](https://github.com/azurekid/bluemountaintravel) | azurekid project | README reviewed | Bluemountain travel | Supporting project context; not asserted to be an identity attack tool |
| [cloud-custodian](https://github.com/azurekid/cloud-custodian) | Upstream fork | README reviewed | Rules engine for cloud security, cost optimization, and governance, DSL in yaml for policies to query, filter, and take actions on resources | Upstream fork / supporting reference; not claimed as original authorship |
| [codespaces](https://github.com/azurekid/codespaces) | azurekid project | README reviewed | Base Template for codespaces | Supporting project context; not asserted to be an identity attack tool |
| [Copilot-For-Security](https://github.com/azurekid/Copilot-For-Security) | Upstream fork | README reviewed | Microsoft Copilot for Security is a generative AI-powered security solution that helps increase the efficiency and capabilities of defenders to improve security outcomes at machine speed and scale, while remaining compliant to responsible AI principles | Upstream fork / supporting reference; not claimed as original authorship |
| [DefenderXDR](https://github.com/azurekid/DefenderXDR) | azurekid project | README reviewed | PowerShell module for Defender XDR configurations | Defender XDR configuration and security operations |
| [detection-mcp](https://github.com/azurekid/detection-mcp) | azurekid project | README reviewed | MCP for detection engineering | Detection engineering MCP server |
| [doodle-to-code](https://github.com/azurekid/doodle-to-code) | Upstream fork | README reviewed | From Doodle to Code: Understand the concepts of Generative AI principles through doodles and apply the knowledge by coding! | Upstream fork / supporting reference; not claimed as original authorship |
| [extensions](https://github.com/azurekid/extensions) | azurekid project | README reviewed | DevOps extensions | Supporting project context; not asserted to be an identity attack tool |
| [fastbuster](https://github.com/azurekid/fastbuster) | azurekid project | README reviewed | No public description | Supporting project context; not asserted to be an identity attack tool |
| [HashSight](https://github.com/azurekid/HashSight) | azurekid project | README reviewed | hash signature intelligence | Supporting project context; not asserted to be an identity attack tool |
| [jsonize](https://github.com/azurekid/jsonize) | azurekid project | README reviewed | This function beautifies a json string to a user friendly format | Supporting project context; not asserted to be an identity attack tool |
| [KeepIt](https://github.com/azurekid/KeepIt) | azurekid project | README reviewed | No public description | Supporting project context; not asserted to be an identity attack tool |
| [key-vault-function](https://github.com/azurekid/key-vault-function) | azurekid project | README reviewed | No public description | Supporting Custom Log Function / Key Vault integration |
| [linkedin-skill-assessments-quizzes](https://github.com/azurekid/linkedin-skill-assessments-quizzes) | Upstream fork | README reviewed | Full reference of LinkedIn answers 2021 for skill assessments, LinkedIn test, questions and answers (aws-lambda, rest-api, javascript, react, git, html, jquery, mongodb, java, Go, python, machine-learning, power-point) linkedin excel test lösungen, linkedin machine learning test | Upstream fork / supporting reference; not claimed as original authorship |
| [mc2-connect](https://github.com/azurekid/mc2-connect) | azurekid project | README reviewed | No public description | Supporting project context; not asserted to be an identity attack tool |
| [mc2connect](https://github.com/azurekid/mc2connect) | azurekid project | Metadata only | usecase for mc2 connect | Metadata-only: mc2 connect use case |
| [Microsoft-Defender-for-Cloud](https://github.com/azurekid/Microsoft-Defender-for-Cloud) | Upstream fork | README reviewed | Welcome to the Microsoft Defender for Cloud community repository | Upstream fork / supporting reference; not claimed as original authorship |
| [Microsoft-Sentinel2Go](https://github.com/azurekid/Microsoft-Sentinel2Go) | Upstream fork | README reviewed | Microsoft Sentinel2Go is an open source project developed to expedite the deployment of a Microsoft Sentinel research lab.  | Upstream fork / supporting reference; not claimed as original authorship |
| [operation-blackcat](https://github.com/azurekid/operation-blackcat) | azurekid project | README reviewed | No public description | Investigation exercise context; not a documented Entra breach |
| [PaC](https://github.com/azurekid/PaC) | azurekid project | README reviewed | PIM as Code | PIM-as-code policy configuration |
| [ParcelPinPoint](https://github.com/azurekid/ParcelPinPoint) | azurekid project | README reviewed | This repository contains a web application to find the parel pickup and drop-off locations | Supporting project context; not asserted to be an identity attack tool |
| [pester-tests-report](https://github.com/azurekid/pester-tests-report) | Upstream fork | README reviewed | GitHub Action to run Pester tests and generate report attached to Workflow Run | Upstream fork / supporting reference; not claimed as original authorship |
| [Piceb](https://github.com/azurekid/Piceb) | azurekid project | README reviewed | This repository contains the full deployment and management stack for Privileged Identity Management as Bicep code | PIM deployment and management using Bicep |
| [PIM](https://github.com/azurekid/PIM) | azurekid project | README reviewed | No public description | PIM policy configuration automation |
| [policy-as-code](https://github.com/azurekid/policy-as-code) | azurekid project | README reviewed | No public description | Pipeline and remediation identity trust demonstration |
| [r1ckr0ll3r](https://github.com/azurekid/r1ckr0ll3r) | azurekid project | README reviewed | No public description | Supporting project context; not asserted to be an identity attack tool |
| [ScEntra](https://github.com/azurekid/ScEntra) | azurekid project | README reviewed | Scan Entra for risk in role assignments and escalation paths | Identity relationship and candidate escalation-path analysis |
| [sentinel-deploy](https://github.com/azurekid/sentinel-deploy) | azurekid project | README reviewed | No public description | Supporting project context; not asserted to be an identity attack tool |
| [Sentinel-playground](https://github.com/azurekid/Sentinel-playground) | Upstream fork | README reviewed | Solution to deploy a Sentinel to Go demo environment | Upstream fork / supporting reference; not claimed as original authorship |
| [shadowcat](https://github.com/azurekid/shadowcat) | azurekid project | README reviewed | No public description | Supporting Windows security research platform |
| [sigma](https://github.com/azurekid/sigma) | Upstream fork | README reviewed | Main Sigma Rule Repository | Upstream fork / supporting reference; not claimed as original authorship |
| [SigmaXDR](https://github.com/azurekid/SigmaXDR) | azurekid project | README reviewed | Convert Sigma Rules to Defender XDR detections | Sigma to Defender XDR detection conversion |
| [skills-code-with-codespaces](https://github.com/azurekid/skills-code-with-codespaces) | azurekid project | README reviewed | My clone repository | Supporting project context; not asserted to be an identity attack tool |
| [skills-copilot-codespaces-vscode](https://github.com/azurekid/skills-copilot-codespaces-vscode) | azurekid project | README reviewed | My clone repository | Supporting project context; not asserted to be an identity attack tool |
| [skills-introduction-to-github](https://github.com/azurekid/skills-introduction-to-github) | azurekid project | README reviewed | My clone repository | Supporting project context; not asserted to be an identity attack tool |
| [skillseal](https://github.com/azurekid/skillseal) | azurekid project | README reviewed | Only let AI agents load skills that were approved and signed (OMS/Sigstore + fail-closed agent hooks) | Approved skill signing and verification |
| [SkillVenom](https://github.com/azurekid/SkillVenom) | azurekid project | README reviewed | No public description | Defanged agent-file attack research catalogue |
| [spraycat](https://github.com/azurekid/spraycat) | azurekid project | README reviewed | Entra ID Password Spray tool | Authorized password-spray testing reference; no live attack required |
| [SQLizer](https://github.com/azurekid/SQLizer) | azurekid project | README reviewed | A Database injection tool for testing against well known vulnerabilities | Supporting project context; not asserted to be an identity attack tool |
| [steampipe](https://github.com/azurekid/steampipe) | Upstream fork | README reviewed | Use SQL to instantly query your cloud services (AWS, Azure, GCP and more). Open source CLI. No DB required.  | Upstream fork / supporting reference; not claimed as original authorship |
| [template-analyzer](https://github.com/azurekid/template-analyzer) | Upstream fork | README reviewed | Template scanner for security misconfiguration and best practices | Upstream fork / supporting reference; not claimed as original authorship |
| [VizCa](https://github.com/azurekid/VizCa) | azurekid project | README reviewed | Visualize Conditional Access Policies and impact | Conditional Access visualization and coverage analysis |
| [warstick](https://github.com/azurekid/warstick) | azurekid project | README reviewed | pendrive hosted AI WarStick | Supporting project context; not asserted to be an identity attack tool |

## Exact source links and retrieval status

- **MS24** - [Microsoft Security Blog, 25 January 2024: Midnight Blizzard](https://www.microsoft.com/en-us/security/blog/2024/01/25/midnight-blizzard-guidance-for-responders-on-nation-state-attack/). Directly read. Historical incident; not a claim about current EWS availability.
- **MI** - [Microsoft Learn: Use managed identities on an Azure VM](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-to-use-vm-token). Microsoft Learn search excerpts reviewed; direct page retrieval failed.
- **WCA** - [Microsoft Learn: Conditional Access for workload identities](https://learn.microsoft.com/en-us/entra/identity/conditional-access/workload-identity). Microsoft Learn search excerpts reviewed; direct page retrieval failed.
- **CAE** - [Microsoft Learn: Continuous access evaluation for workload identities](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-continuous-access-evaluation-workload). Microsoft Learn search excerpts reviewed. Managed identities are not supported.
- **PIMDOC** - [Microsoft Learn: Plan a PIM deployment](https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-deployment-plan). Microsoft Learn search excerpts reviewed.
- **ScEntra** - [azurekid/ScEntra](https://github.com/azurekid/ScEntra/blob/main/README.md). Public README read.
- **skillseal** - [azurekid/skillseal](https://github.com/azurekid/skillseal/blob/main/README.md). Public README read.
- **blackcat** - [azurekid/blackcat](https://github.com/azurekid/blackcat/blob/main/README.md). Public README read.
- **SkillVenom** - [azurekid/SkillVenom](https://github.com/azurekid/SkillVenom/blob/main/README.md). Public README read.
- **AgentTrap** - [azurekid/AgentTrap](https://github.com/azurekid/AgentTrap/blob/main/README.md). Public README read.
- **policy-as-code** - [azurekid/policy-as-code](https://github.com/azurekid/policy-as-code/blob/main/README.md). Public README read.
- **Piceb** - [azurekid/Piceb](https://github.com/azurekid/Piceb/blob/main/README.md). Public README read.
- **DefenderXDR** - [azurekid/DefenderXDR](https://github.com/azurekid/DefenderXDR/blob/main/README.md). Public README read.
- **warstick** - [azurekid/warstick](https://github.com/azurekid/warstick/blob/main/README.md). Public README read.
- **HashSight** - [azurekid/HashSight](https://github.com/azurekid/HashSight/blob/main/README.md). Public README read.
- **Azure-Sentinel** - [azurekid/Azure-Sentinel (fork)](https://github.com/azurekid/Azure-Sentinel/blob/master/README.md). Public README read.
- **AzShortLink** - [azurekid/AzShortLink](https://github.com/azurekid/AzShortLink/blob/main/README.md). Public README read.
- **KeepIt** - [azurekid/KeepIt](https://github.com/azurekid/KeepIt/blob/main/README.md). Public README read.
- **jsonize** - [azurekid/jsonize](https://github.com/azurekid/jsonize/blob/main/README.md). Public README read.
- **Azure-Stencils** - [azurekid/Azure-Stencils](https://github.com/azurekid/Azure-Stencils/blob/master/README.md). Public README read.
- **SQLizer** - [azurekid/SQLizer](https://github.com/azurekid/SQLizer/blob/main/README.md). Public README read.
- **fastbuster** - [azurekid/fastbuster](https://github.com/azurekid/fastbuster/blob/main/README.md). Public README read.
- **1Password-Sentinel** - [azurekid/1Password-Sentinel](https://github.com/azurekid/1Password-Sentinel). Repository metadata only; no accessible README.
- **PaC** - [azurekid/PaC](https://github.com/azurekid/PaC/blob/main/README.md). Public README read.
- **PIM** - [azurekid/PIM](https://github.com/azurekid/PIM/blob/main/README.md). Public README read.
- **operation-blackcat** - [azurekid/operation-blackcat](https://github.com/azurekid/operation-blackcat/blob/main/README.md). Public README read.
- **azurekid** - [azurekid/azurekid](https://github.com/azurekid/azurekid/blob/main/README.md). Public README read.
- **mc2-connect** - [azurekid/mc2-connect](https://github.com/azurekid/mc2-connect/blob/main/README.md). Public README read.
- **bluemountaintravel** - [azurekid/bluemountaintravel](https://github.com/azurekid/bluemountaintravel/blob/main/README.md). Public README read.
- **mc2connect** - [azurekid/mc2connect](https://github.com/azurekid/mc2connect). Repository metadata only; no accessible README.
- **spraycat** - [azurekid/spraycat](https://github.com/azurekid/spraycat/blob/main/README.MD). Public README read.
- **sigma** - [azurekid/sigma (fork)](https://github.com/azurekid/sigma/blob/master/README.md). Public README read.
- **VizCa** - [azurekid/VizCa](https://github.com/azurekid/VizCa/blob/main/README.md). Public README read.
- **SigmaXDR** - [azurekid/SigmaXDR](https://github.com/azurekid/SigmaXDR/blob/main/README.md). Public README read.
- **detection-mcp** - [azurekid/detection-mcp](https://github.com/azurekid/detection-mcp/blob/main/README.md). Public README read.
- **Microsoft-Defender-for-Cloud** - [azurekid/Microsoft-Defender-for-Cloud (fork)](https://github.com/azurekid/Microsoft-Defender-for-Cloud/blob/main/README.md). Public README read.
- **template-analyzer** - [azurekid/template-analyzer (fork)](https://github.com/azurekid/template-analyzer/blob/main/README.md). Public README read.
- **ParcelPinPoint** - [azurekid/ParcelPinPoint](https://github.com/azurekid/ParcelPinPoint/blob/main/README.md). Public README read.
- **Copilot-For-Security** - [azurekid/Copilot-For-Security (fork)](https://github.com/azurekid/Copilot-For-Security/blob/main/README.md). Public README read.
- **cloud-custodian** - [azurekid/cloud-custodian (fork)](https://github.com/azurekid/cloud-custodian/blob/master/README.md). Public README read.
- **shadowcat** - [azurekid/shadowcat](https://github.com/azurekid/shadowcat/blob/main/README.md). Public README read.
- **bluemountainbank** - [azurekid/bluemountainbank](https://github.com/azurekid/bluemountainbank/blob/main/README.md). Public README read.
- **r1ckr0ll3r** - [azurekid/r1ckr0ll3r](https://github.com/azurekid/r1ckr0ll3r/blob/main/README.md). Public README read.
- **AADInternals** - [azurekid/AADInternals (fork)](https://github.com/azurekid/AADInternals/blob/master/README.md). Public README read.
- **steampipe** - [azurekid/steampipe (fork)](https://github.com/azurekid/steampipe/blob/main/README.md). Public README read.
- **azure-opt** - [azurekid/azure-opt](https://github.com/azurekid/azure-opt/blob/main/README.md). Public README read.
- **codespaces** - [azurekid/codespaces](https://github.com/azurekid/codespaces/blob/main/README.md). Public README read.
- **doodle-to-code** - [azurekid/doodle-to-code (fork)](https://github.com/azurekid/doodle-to-code/blob/main/README.md). Public README read.
- **blog** - [azurekid/blog](https://github.com/azurekid/blog/blob/master/README.md). Public README read.
- **pester-tests-report** - [azurekid/pester-tests-report (fork)](https://github.com/azurekid/pester-tests-report/blob/master/README.md). Public README read.
- **Microsoft-Sentinel2Go** - [azurekid/Microsoft-Sentinel2Go (fork)](https://github.com/azurekid/Microsoft-Sentinel2Go/blob/master/README.md). Public README read.
- **Bio-Compliancy** - [azurekid/Bio-Compliancy (fork)](https://github.com/azurekid/Bio-Compliancy/blob/main/README.md). Public README read.
- **skills-copilot-codespaces-vscode** - [azurekid/skills-copilot-codespaces-vscode](https://github.com/azurekid/skills-copilot-codespaces-vscode/blob/main/README.md). Public README read.
- **skills-code-with-codespaces** - [azurekid/skills-code-with-codespaces](https://github.com/azurekid/skills-code-with-codespaces/blob/main/README.md). Public README read.
- **skills-introduction-to-github** - [azurekid/skills-introduction-to-github](https://github.com/azurekid/skills-introduction-to-github/blob/main/README.md). Public README read.
- **sentinel-deploy** - [azurekid/sentinel-deploy](https://github.com/azurekid/sentinel-deploy/blob/main/README.md). Public README read.
- **extensions** - [azurekid/extensions](https://github.com/azurekid/extensions/blob/master/README.md). Public README read.
- **azure-orphan-resources** - [azurekid/azure-orphan-resources (fork)](https://github.com/azurekid/azure-orphan-resources/blob/main/README.md). Public README read.
- **AzurePermissionInsight** - [azurekid/AzurePermissionInsight (fork)](https://github.com/azurekid/AzurePermissionInsight/blob/main/README.md). Public README read.
- **azure-resource-manager-schemas** - [azurekid/azure-resource-manager-schemas (fork)](https://github.com/azurekid/azure-resource-manager-schemas/blob/master/README.md). Public README read.
- **key-vault-function** - [azurekid/key-vault-function](https://github.com/azurekid/key-vault-function/blob/main/readme.md). Public README read.
- **azure-docs** - [azurekid/azure-docs (fork)](https://github.com/azurekid/azure-docs/blob/master/README.md). Public README read.
- **linkedin-skill-assessments-quizzes** - [azurekid/linkedin-skill-assessments-quizzes (fork)](https://github.com/azurekid/linkedin-skill-assessments-quizzes/blob/master/README.md). Public README read.
- **Sentinel-playground** - [azurekid/Sentinel-playground (fork)](https://github.com/azurekid/Sentinel-playground/blob/main/README.md). Public README read.
- **Azure-Lighthouse-samples** - [azurekid/Azure-Lighthouse-samples (fork)](https://github.com/azurekid/Azure-Lighthouse-samples/blob/master/README.md). Public README read.
- **azure-powershell** - [azurekid/azure-powershell (fork)](https://github.com/azurekid/azure-powershell/blob/master/README.md). Public README read.
- **AH1** - [Azure Tenant Takeover: From Exposed Config to Global Admin](https://azurehacking.com/post.html?slug=tabletop-tenant-takeover-scenario). Link/topic found in BlackCat README. Article body NOT retrieved; website DNS failed.
- **AH2** - [Detecting Privilege Escalation in Entra ID](https://azurehacking.com/post.html?slug=detecting-privilege-escalation-in-entra-id). Link/topic found in BlackCat README. Article body NOT retrieved; website DNS failed.
- **AH3** - [ScEntra: Visualizing Entra ID Privilege Escalation Paths](https://azurehacking.com/post.html?slug=scentra-visualizing-entra-id-privilege-escalation-paths). Link/topic found in BlackCat README. Article body NOT retrieved; website DNS failed.
- **AH4** - [Impairing Azure Defenses Through Diagnostic Setting Manipulation](https://azurehacking.com/post.html?slug=impairing-azure-defenses-through-diagnostic-setting-manipulation). Link/topic found in BlackCat README. Article body NOT retrieved; website DNS failed.
