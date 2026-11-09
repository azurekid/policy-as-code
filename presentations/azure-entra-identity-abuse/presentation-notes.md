# No Malware. Just the Right Identity.

**Presenter:** Rogier Dijkman / azurekid
**Format:** 40-minute technical talk; 25 core slides plus source and repository appendices.
**Research snapshot:** 9 November 2026.
**Scope:** Public repositories only. Real incident: Microsoft's published Midnight Blizzard breach. Six examples are lab scenarios, not claimed customer incidents. No attack was executed.
**Website limitation:** azurehacking.com did not resolve. Four article links were recovered from BlackCat's README; their article bodies were not reviewed.

Suggested pacing: slides 1-4, 5 minutes; 5-9, 8 minutes; 10-16, 12 minutes; 17, 5 minutes; 18-24, 9 minutes; 25, 1 minute. Remaining slides are backup.

---

## 01. NO MALWARE. JUST THE RIGHT IDENTITY.

**OPENING** | Stealing and abusing misconfigured identities in Microsoft Azure and Entra

- **Rogier Dijkman / azurekid:** Cloud identity abuse, real incident evidence, and six practical lab scenarios.
- **The central question:** Who can act as your most powerful identity?
- **The promise:** Trace the trust chain. Prove the impact. Break the path.

**Speaker notes:** Suggested format: 40-minute technical talk plus discussion. Introduce yourself as Rogier Dijkman, using the public profile as the attribution source. This talk is for cloud engineers, defenders and authorized security testers. We discuss mechanisms and safe evidence, not production credential theft. No customer incident is attributed to you. The real story is Microsoft's published Midnight Blizzard incident; the other examples are explicitly lab scenarios.

**Sources:**
- [azurekid/azurekid](https://github.com/azurekid/azurekid/blob/main/README.md) - Public README read.
- [azurekid/blackcat](https://github.com/azurekid/blackcat/blob/main/README.md) - Public README read.

---

## 02. "It is only a test account."

**AUDIENCE MOMENT** | A sentence that sounds harmless until the test identity trusts production.

- **Ask the room:** Would you protect a test tenant like production?
- **Then change the question:** What if a test application could read production mail?
- **The hook:** Environment labels do not constrain permissions. Trust relationships do.

**Speaker notes:** Pause after the title. Invite a show of hands, not an account of anyone's actual breach. Reveal the second card, then transition: this was not merely a theoretical risk. The following story is a published Microsoft incident. Do not say you investigated it or that your tools were used in it.

**Sources:**
- [Microsoft Security Blog, 25 January 2024: Midnight Blizzard](https://www.microsoft.com/en-us/security/blog/2024/01/25/midnight-blizzard-guidance-for-responders-on-nation-state-attack/) - Directly read. Historical incident; not a claim about current EWS availability.

---

## 03. Identity abuse has three ingredients

**CONCEPT** | Credential or execution control + authority + a reachable resource

**Trust chain:** BECOME -> INHERIT -> ACT

- **BECOME:** Password, application credential, session token, trusted workload or delegated tool execution.
- **INHERIT:** Azure RBAC, Entra directory roles, Graph application permissions and resource-specific grants.
- **ACT:** Read data, change configuration, run workloads or modify identities, within the granted scope.

**Speaker notes:** Distinguish stealing a credential from abusing a legitimately authenticated executor. A compromised agent or deployment pipeline may use its existing identity without exporting any token. Tokens are audience-bound and time-limited: possession of an ARM token does not make it a Graph token. Permissions still constrain every action. Federated identity credentials establish trust; they are not themselves bearer tokens.

**Sources:**
- [azurekid/blackcat](https://github.com/azurekid/blackcat/blob/main/README.md) - Public README read.
- [Microsoft Learn: Use managed identities on an Azure VM](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-to-use-vm-token) - Microsoft Learn search excerpts reviewed; direct page retrieval failed.
- [azurekid/policy-as-code](https://github.com/azurekid/policy-as-code/blob/main/README.md) - Public README read.

---

## 04. Four permissions worlds. Not one.

**TECHNICAL GUARDRAIL** | Azure resource authority is not the same as Entra directory authority.

- **AZURE CONTROL PLANE:** Manage resources at management-group, subscription, resource-group or resource scope.
- **ENTRA + GRAPH:** Directory roles, delegated scopes and application permissions govern identity operations.
- **RESOURCE DATA PLANE:** Key Vault secrets, storage data and mail each have their own access model.

**Speaker notes:** Do not equate Azure Owner with Entra Global Administrator. Ordinary Contributor does not include roleAssignments/write. Managing a vault is not automatically the same as reading its secrets: the permission model and any ability to change it matter. ScEntra shows potential relationships; validate the actual action, scope, deny assignments and conditions before calling a path exploitable. Eligible PIM access is potential, not already-active authority.

**Sources:**
- [azurekid/ScEntra](https://github.com/azurekid/ScEntra/blob/main/README.md) - Public README read.
- [Microsoft Learn: Plan a PIM deployment](https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-deployment-plan) - Microsoft Learn search excerpts reviewed.
- [azurekid/blackcat](https://github.com/azurekid/blackcat/blob/main/README.md) - Public README read.

---

## 05. The real story: Midnight Blizzard

**DOCUMENTED INCIDENT** | Microsoft detected an attack on its corporate systems on 12 January 2024.

- **ENTRY:** A legacy, non-production test tenant account without MFA.
- **BRIDGE:** A legacy test OAuth application with elevated corporate access.
- **IMPACT:** Actor-controlled OAuth applications accessed corporate email through EWS.

**Speaker notes:** Read the cards as a causal story rather than a product failure headline. Microsoft published its detailed guidance on 25 January 2024. Its investigation was ongoing at that time. This is the historical case and terminology from that source. The specific EWS mechanism is not a recommendation for a 2026 live demo. BlackCat the research module is not the ALPHV/BlackCat ransomware group, and neither is attributed to this incident.

**Sources:**
- [Microsoft Security Blog, 25 January 2024: Midnight Blizzard](https://www.microsoft.com/en-us/security/blog/2024/01/25/midnight-blizzard-guidance-for-responders-on-nation-state-attack/) - Directly read. Historical incident; not a claim about current EWS availability.

---

## 06. Scene 1: the forgotten identity

**DOCUMENTED INCIDENT** | The initial access was a password spray, not a zero-day.

- **WHAT MICROSOFT REPORTED:** The compromised test account did not have MFA enabled.
- **WHY IT MATTERED:** That identity was a foothold into a larger trust relationship.
- **DEFENDER QUESTION:** Which legacy, test and exception accounts can still authenticate?

**Speaker notes:** Keep password spraying conceptual; do not show evasion settings or execute it against real tenants. The source describes a password-spray compromise of a legacy non-production account. The important lesson is coverage: an excluded or forgotten account can defeat an otherwise mature control deployment. Later we use VizCa for coverage review and cite spraycat only as an authorized testing reference.

**Sources:**
- [Microsoft Security Blog, 25 January 2024: Midnight Blizzard](https://www.microsoft.com/en-us/security/blog/2024/01/25/midnight-blizzard-guidance-for-responders-on-nation-state-attack/) - Directly read. Historical incident; not a claim about current EWS availability.
- [azurekid/VizCa](https://github.com/azurekid/VizCa/blob/main/README.md) - Public README read.
- [azurekid/spraycat](https://github.com/azurekid/spraycat/blob/main/README.MD) - Public README read.

---

## 07. Scene 2: the test app crossed the boundary

**DOCUMENTED INCIDENT** | A human foothold became application-level access.

**Trust chain:** TEST ACCOUNT -> LEGACY OAUTH APP -> MALICIOUS APPS -> MAIL ACCESS

- **LEGACY APP:** The actor identified and compromised a test OAuth application with elevated corporate access.
- **NEW APP IDENTITIES:** The actor created malicious OAuth applications and a new user used to grant consent.
- **HIGH-IMPACT GRANT:** The legacy app granted the Exchange Online full_access_as_app role.

**Speaker notes:** Use Microsoft's exact causal description. Do not invent the secret source or imply every compromised user can grant application permissions. Sufficient authority existed in this case through the legacy application. Application permissions differ from delegated permissions: the resulting app-only authority can operate without a human interactive sign-in.

**Sources:**
- [Microsoft Security Blog, 25 January 2024: Midnight Blizzard](https://www.microsoft.com/en-us/security/blog/2024/01/25/midnight-blizzard-guidance-for-responders-on-nation-state-attack/) - Directly read. Historical incident; not a claim about current EWS availability.

---

## 08. Scene 3: valid identity, malicious purpose

**DOCUMENTED INCIDENT** | The applications authenticated to Exchange Online and collected corporate email.

- **THE AUTHENTICATION WORKED:** The service recognized an application holding granted authority.
- **THE PURPOSE WAS MALICIOUS:** Successful authentication did not make the activity legitimate.
- **THE RESPONSE MUST FOLLOW:** Removing the original user foothold alone may leave application access.

**Speaker notes:** The Microsoft source describes collection through Exchange Web Services and explains that OAuth misuse can maintain access after loss of the initial account. Do not promise a password reset revokes all app credentials or already-issued tokens. The response must include applications, service principals, permission grants and resource activity.

**Sources:**
- [Microsoft Security Blog, 25 January 2024: Midnight Blizzard](https://www.microsoft.com/en-us/security/blog/2024/01/25/midnight-blizzard-guidance-for-responders-on-nation-state-attack/) - Directly read. Historical incident; not a claim about current EWS availability.
- [Microsoft Learn: Continuous access evaluation for workload identities](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-continuous-access-evaluation-workload) - Microsoft Learn search excerpts reviewed. Managed identities are not supported.

---

## 09. The breach was a chain of trust

**LESSON** | The test label was not the security boundary.

- **ENTRY CONTROL:** Protect every account, including exceptions and non-production identities.
- **AUTHORITY CONTROL:** Review app-only grants and cross-environment application trust.
- **OBSERVABILITY:** Correlate sign-ins, identity changes and actual resource access.

**Speaker notes:** Summarize the story in one sentence: a forgotten human identity enabled application abuse across an environment boundary. Ask where your organization has a similar bridge, without asking the audience to disclose secrets. Transition from Microsoft's incident to your own public projects: these tools help discover, govern and detect analogous risks; they are not claimed to have investigated the breach.

**Sources:**
- [Microsoft Security Blog, 25 January 2024: Midnight Blizzard](https://www.microsoft.com/en-us/security/blog/2024/01/25/midnight-blizzard-guidance-for-responders-on-nation-state-attack/) - Directly read. Historical incident; not a claim about current EWS availability.
- [azurekid/ScEntra](https://github.com/azurekid/ScEntra/blob/main/README.md) - Public README read.
- [azurekid/VizCa](https://github.com/azurekid/VizCa/blob/main/README.md) - Public README read.

---

## 10. Your projects tell the whole story

**PROJECT MAP** | Discover the path, test a safe claim, govern the grant, detect the behavior.

- **DISCOVER + VALIDATE:** ScEntra: identity relationships. VizCa: Conditional Access coverage. BlackCat: authorized Azure posture validation.
- **GOVERN + CONSTRAIN:** PIM / PaC / Piceb: privilege configuration. policy-as-code: pipeline and remediation trust. skillseal: approved agent skills.
- **DETECT + INVESTIGATE:** DefenderXDR / SigmaXDR / detection-mcp. Sentinel and Sigma forks, clearly attributed. AgentTrap: AgentLens inspection platform.

**Speaker notes:** All 61 public repositories are inventoried in the appendix and companion source inventory. Not all are identity tools; unrelated applications and learning repositories are labeled supporting context, not forced into the attack narrative. Forks retain upstream attribution. Project capabilities here come from public READMEs, not independent execution testing.

**Sources:**
- [azurekid/ScEntra](https://github.com/azurekid/ScEntra/blob/main/README.md) - Public README read.
- [azurekid/VizCa](https://github.com/azurekid/VizCa/blob/main/README.md) - Public README read.
- [azurekid/blackcat](https://github.com/azurekid/blackcat/blob/main/README.md) - Public README read.
- [azurekid/PIM](https://github.com/azurekid/PIM/blob/main/README.md) - Public README read.
- [azurekid/PaC](https://github.com/azurekid/PaC/blob/main/README.md) - Public README read.
- [azurekid/Piceb](https://github.com/azurekid/Piceb/blob/main/README.md) - Public README read.
- [azurekid/policy-as-code](https://github.com/azurekid/policy-as-code/blob/main/README.md) - Public README read.
- [azurekid/skillseal](https://github.com/azurekid/skillseal/blob/main/README.md) - Public README read.
- [azurekid/DefenderXDR](https://github.com/azurekid/DefenderXDR/blob/main/README.md) - Public README read.
- [azurekid/SigmaXDR](https://github.com/azurekid/SigmaXDR/blob/main/README.md) - Public README read.
- [azurekid/detection-mcp](https://github.com/azurekid/detection-mcp/blob/main/README.md) - Public README read.
- [azurekid/AgentTrap](https://github.com/azurekid/AgentTrap/blob/main/README.md) - Public README read.

---

## 11. Example 1 / The account outside the policy

**LAB SCENARIO** | Lab scenario: the exception is the entry point.

- **MISCONFIGURATION:** A legacy or test user falls outside enforced authentication policy coverage.
- **SAFE PROOF:** Inspect exported CA policy coverage for a synthetic test user; show the gap, not a password attack.
- **BREAK THE PATH:** Protect exceptions, use phishing-resistant MFA where appropriate, and review emergency-access controls.

**Speaker notes:** Project tie-in: VizCa describes policy export, visualization, coverage testing and security-gap analysis. spraycat is a password-spray testing project, not a prerequisite for this demonstration. Use a synthetic user and a policy export or isolated tenant; never test public accounts. Emergency-access accounts have special availability requirements and should be designed and monitored, not blindly subjected to a blanket policy. This is a lab example inspired by a documented technique, not your own reported breach.

**Sources:**
- [azurekid/VizCa](https://github.com/azurekid/VizCa/blob/main/README.md) - Public README read.
- [azurekid/spraycat](https://github.com/azurekid/spraycat/blob/main/README.MD) - Public README read.
- [Microsoft Security Blog, 25 January 2024: Midnight Blizzard](https://www.microsoft.com/en-us/security/blog/2024/01/25/midnight-blizzard-guidance-for-responders-on-nation-state-attack/) - Directly read. Historical incident; not a claim about current EWS availability.

---

## 12. Example 2 / The service principal in the build

**LAB SCENARIO** | Lab scenario: a leaked application secret inherits every existing grant.

- **MISCONFIGURATION:** A reusable client secret is exposed in an artifact, setting or repository; the app is overprivileged.
- **SAFE PROOF:** Use a deliberately created lab credential to read one synthetic canary the identity was granted.
- **BREAK THE PATH:** Remove exposed credentials, inspect grants, minimize scope and prefer tightly constrained workload federation.

**Speaker notes:** Project tie-in: BlackCat describes credential-access validation and secret exposure; ScEntra describes service-principal permission analysis. Show the identity's tenant, object ID, grant and synthetic resource result, but never the secret or token. Replacing a secret with OIDC removes that reusable secret, not excessive authorization. Treat key-vault-function as integration context only: its README is a Custom Log Function, not an attack tool. Do not imply that seeing a client ID or tenant ID constitutes credential exposure.

**Sources:**
- [azurekid/blackcat](https://github.com/azurekid/blackcat/blob/main/README.md) - Public README read.
- [azurekid/ScEntra](https://github.com/azurekid/ScEntra/blob/main/README.md) - Public README read.
- [azurekid/key-vault-function](https://github.com/azurekid/key-vault-function/blob/main/readme.md) - Public README read.

---

## 13. Example 3 / The managed identity belongs to the workload

**LAB SCENARIO** | Lab scenario: compute compromise becomes identity use.

- **MISCONFIGURATION:** A compromised VM or workload carries a managed identity with unnecessary sensitive access.
- **SAFE PROOF:** An approved process on an isolated VM accesses a synthetic canary using the workload identity.
- **BREAK THE PATH:** Harden workload execution and scope each managed identity to the smallest required resource set.

**Speaker notes:** Microsoft states the VM is the managed-identity security boundary: code running there can request tokens for managed identities available to it. A remote outsider cannot simply query another VM's metadata endpoint. SSRF exploitation depends on reaching the relevant endpoint and satisfying its request requirements; it is not automatic. BlackCat also documents UAMI token techniques using deployment scripts or federated credentials; those have distinct write/attach/trust prerequisites and are not the same as local VM metadata access. User MFA is not a managed-identity control.

**Sources:**
- [Microsoft Learn: Use managed identities on an Azure VM](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-to-use-vm-token) - Microsoft Learn search excerpts reviewed; direct page retrieval failed.
- [azurekid/blackcat](https://github.com/azurekid/blackcat/blob/main/README.md) - Public README read.
- [azurekid/ScEntra](https://github.com/azurekid/ScEntra/blob/main/README.md) - Public README read.
- [Microsoft Learn: Continuous access evaluation for workload identities](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-continuous-access-evaluation-workload) - Microsoft Learn search excerpts reviewed. Managed identities are not supported.

---

## 14. Example 4 / Who can change the identity?

**LAB SCENARIO** | Lab scenario: credential and federation writers are part of the privilege graph.

- **MISCONFIGURATION:** A principal can alter a sensitive application's credentials or a UAMI's federation trust.
- **SAFE PROOF:** Inspect effective writer authority, object type, current grants and trust configuration in a disposable lab.
- **BREAK THE PATH:** Constrain credential writers, review ownership, lock federation trust and alert on changes.

**Speaker notes:** BlackCat documents service-principal credential changes and managed-identity federated credentials. ScEntra analyzes ownership chains and dangerous permissions. Application objects, service-principal objects and user-assigned managed identity resources have different management APIs and authorization checks; ownership of one does not prove write access to every related object. Exact ownership semantics, existing app permissions, scope and consent must be verified. Adding a credential or trust alone does not grant new roles; it can expose authority already assigned to the affected identity.

**Sources:**
- [azurekid/blackcat](https://github.com/azurekid/blackcat/blob/main/README.md) - Public README read.
- [azurekid/ScEntra](https://github.com/azurekid/ScEntra/blob/main/README.md) - Public README read.

---

## 15. Example 5 / The policy pipeline is not the executor

**PROJECT-BASED LAB** | Your policy-as-code project provides the strongest demonstration of delegated authority.

**Trust chain:** REPOSITORY CHANGE -> PIPELINE -> POLICY CONTENT -> REMEDIATION MI

- **PIPELINE IDENTITY:** Deploys policy definitions and assignments under its own restricted grant.
- **REMEDIATION IDENTITY:** Runs the policy's deployment using separately provisioned resource permissions.
- **THE TRUST SEAM:** Control over executable policy content may influence a more powerful runtime identity.

**Speaker notes:** The public README contrasts pipeline federation, protected environments and a separate remediation UAMI. This is a confused-deputy model: examine who can change code executed by another identity. Critical source caveat: the README lists an Owner-role payload, but ordinary Contributor does not include roleAssignments/write; a Contributor-only executor cannot successfully create that Owner assignment. Do not present that escalation as proven. Use only a harmless action allowed by the remediation identity's actual grants. Standard federated identity credentials use exact matching; do not teach a literal wildcard as universally supported. Any flexible expression requires separate feature and configuration validation.

**Sources:**
- [azurekid/policy-as-code](https://github.com/azurekid/policy-as-code/blob/main/README.md) - Public README read.

---

## 16. Example 6 / The agent already has your identity

**LAB SCENARIO** | Lab scenario: malicious instructions can misuse legitimate tools without stealing a token.

- **MISCONFIGURATION:** Untrusted agent guidance can influence a tool session carrying sensitive authority.
- **SAFE PROOF:** Use a defanged SkillVenom sample and a mocked cloud tool; show the attempted boundary crossing.
- **BREAK THE PATH:** Inspect with AgentLens, verify approved skills with Skillseal and scope tool identities.

**Speaker notes:** AgentTrap's current README calls the defensive platform AgentLens. SkillVenom is the separate defanged, test-backed research catalogue. Skillseal verifies approved signed skills. Do not imply signing guarantees a skill is harmless: it establishes approved provenance and integrity, while review and tool permissions still matter. Keep this demonstration offline or use mocked tools and synthetic data. No real token, credential, outbound collection endpoint or privileged cloud action is needed. The conceptual result is identity use via a confused deputy, not necessarily token theft.

**Sources:**
- [azurekid/AgentTrap](https://github.com/azurekid/AgentTrap/blob/main/README.md) - Public README read.
- [azurekid/SkillVenom](https://github.com/azurekid/SkillVenom/blob/main/README.md) - Public README read.
- [azurekid/skillseal](https://github.com/azurekid/skillseal/blob/main/README.md) - Public README read.

---

## 17. Flagship demo / No secrets. Still too much trust.

**SAFE DEMO STORYBOARD** | Show a before-and-after policy remediation boundary in an isolated lab.

- **BEFORE:** Approved synthetic policy content can influence a broadly scoped remediation identity.
- **PROOF:** Create only a disposable, permitted lab resource or marker. Record caller identity and resource scope.
- **AFTER:** Pre-provision a minimal remediation identity out of band; repeat and show the excessive action is denied.

**Speaker notes:** Five-minute demo storyboard, not a verified executed demo. Preflight in a disposable subscription; use explicit authorization, synthetic data and no production connections. Pick an action within the actual grants, such as creating a harmless lab resource where permitted; never an unproven Owner assignment. Capture the policy definition revision, assignment identity, actual resource operation and denial after narrowing scope. Protected deployment environments and content review must also be in place. A valid prevention result shows both the intended policy task still works and the excessive operation fails. Use recorded evidence if a safe live environment is unavailable.

**Sources:**
- [azurekid/policy-as-code](https://github.com/azurekid/policy-as-code/blob/main/README.md) - Public README read.

---

## 18. Detect the sequence, not just the login

**DEFENDER PLAYBOOK** | A sign-in explains authentication. Resource activity explains impact.

- **IDENTITY EVENTS:** User/workload sign-ins, app credentials, consent grants, role changes and PIM activations.
- **AZURE EVENTS:** Control-plane operations, policy/identity changes and resource-specific data access.
- **CORRELATE:** Credential or trust change -> workload sign-in -> sensitive resource operation.

**Speaker notes:** Relevant Entra exports may include SigninLogs, AADNonInteractiveUserSignInLogs, AADServicePrincipalSignInLogs, AADManagedIdentitySignInLogs and AuditLogs, depending on configuration and licensing. AzureActivity records control-plane events; it is not comprehensive Key Vault or Storage data-plane auditing. Export appropriate resource diagnostics and Microsoft 365 audit data. Correlate tenant, object/app IDs, scope, resource, timestamps and initiator; a shared IP alone is not proof. Coverage, retention and licensing must be checked before promising detection.

**Sources:**
- [Microsoft Security Blog, 25 January 2024: Midnight Blizzard](https://www.microsoft.com/en-us/security/blog/2024/01/25/midnight-blizzard-guidance-for-responders-on-nation-state-attack/) - Directly read. Historical incident; not a claim about current EWS availability.
- [azurekid/DefenderXDR](https://github.com/azurekid/DefenderXDR/blob/main/README.md) - Public README read.
- [azurekid/SigmaXDR](https://github.com/azurekid/SigmaXDR/blob/main/README.md) - Public README read.
- [azurekid/detection-mcp](https://github.com/azurekid/detection-mcp/blob/main/README.md) - Public README read.
- [azurekid/Azure-Sentinel (fork)](https://github.com/azurekid/Azure-Sentinel/blob/master/README.md) - Public README read.

---

## 19. Four high-value detection stories

**DETECTION DESIGN** | Turn your testing evidence into operational detections.

- **IDENTITY MUTATION:** Unexpected credential, owner or federation change followed by workload activity.
- **AUTHORITY EXPANSION:** Sensitive app grant or role assignment followed by access to a new resource.
- **EXECUTOR MISUSE:** Policy/remediation changes or agent-driven actions outside the established workload baseline.

**Speaker notes:** The fourth story is control impairment: diagnostic-setting deletion or changes followed by sensitive operations. BlackCat's README links an AzureHacking article on diagnostic-setting manipulation; the article body was not retrieved. For implementation, use DefenderXDR, SigmaXDR and detection-mcp as project references, not guarantees that a converted rule is production-correct. Validate schema, available fields, entity mapping, expected benign events and false positives. The Sentinel and Sigma repositories here are forks. Do not label these suggested detections as already deployed or measured.

**Sources:**
- [azurekid/DefenderXDR](https://github.com/azurekid/DefenderXDR/blob/main/README.md) - Public README read.
- [azurekid/SigmaXDR](https://github.com/azurekid/SigmaXDR/blob/main/README.md) - Public README read.
- [azurekid/detection-mcp](https://github.com/azurekid/detection-mcp/blob/main/README.md) - Public README read.
- [azurekid/Azure-Sentinel (fork)](https://github.com/azurekid/Azure-Sentinel/blob/master/README.md) - Public README read.
- [azurekid/sigma (fork)](https://github.com/azurekid/sigma/blob/master/README.md) - Public README read.
- [Impairing Azure Defenses Through Diagnostic Setting Manipulation](https://azurehacking.com/post.html?slug=impairing-azure-defenses-through-diagnostic-setting-manipulation) - Link/topic found in BlackCat README. Article body NOT retrieved; website DNS failed.

---

## 20. "We reset the password." Is the incident over?

**INCIDENT RESPONSE** | Contain the identity graph, not only the initial user.

- **PRESERVE + CONTAIN:** Preserve logs; disable affected identities/workloads and revoke exposed credentials or sessions appropriately.
- **REMOVE THE BRIDGES:** Review malicious grants, app credentials, owners, federation trust, roles and automation changes.
- **VERIFY + RECOVER:** Check residual token validity, investigate accessed data and re-enable only the required trust.

**Speaker notes:** There is no universal instant revocation for every Azure/Entra token or downstream service. Disabling an identity or changing a credential can block new authentication while issued tokens may remain usable until expiry or supported revocation enforcement. CAE for workload identities has explicit application/service and identity limitations; managed identities are unsupported. For a managed identity, contain the compromised workload, reduce or remove affected grants, and follow resource-specific response guidance. Rotate downstream secrets if there is evidence they were accessed. Preserve evidence before destructive changes where operationally feasible.

**Sources:**
- [Microsoft Security Blog, 25 January 2024: Midnight Blizzard](https://www.microsoft.com/en-us/security/blog/2024/01/25/midnight-blizzard-guidance-for-responders-on-nation-state-attack/) - Directly read. Historical incident; not a claim about current EWS availability.
- [Microsoft Learn: Continuous access evaluation for workload identities](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-continuous-access-evaluation-workload) - Microsoft Learn search excerpts reviewed. Managed identities are not supported.
- [Microsoft Learn: Use managed identities on an Azure VM](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-to-use-vm-token) - Microsoft Learn search excerpts reviewed; direct page retrieval failed.

---

## 21. Govern the people who govern the identities

**PREVENTION** | PIM helps, but standing app permissions and indirect writers still need review.

- **ACTIVATION:** Time-bound human privilege, appropriate approval and authentication requirements.
- **CONFIGURATION:** Review PIM / PaC / Piceb policy-as-code changes with the same care as application code.
- **INDIRECT AUTHORITY:** Credential writers, app owners, group managers, workload code writers and remediation bindings.

**Speaker notes:** PIM, PaC and Piceb document governance/configuration use cases; they are not proof that all identities are automatically protected by PIM. Enumerate active and eligible human access and the actual activation requirements. Standing application permissions and runtime identities need their own least-privilege and lifecycle controls. A principal administering PIM configuration can weaken the controls; protect the automation identity and review changes. ScEntra's potential-path output is a review aid, not a guarantee of exploitability.

**Sources:**
- [azurekid/PIM](https://github.com/azurekid/PIM/blob/main/README.md) - Public README read.
- [azurekid/PaC](https://github.com/azurekid/PaC/blob/main/README.md) - Public README read.
- [azurekid/Piceb](https://github.com/azurekid/Piceb/blob/main/README.md) - Public README read.
- [Microsoft Learn: Plan a PIM deployment](https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-deployment-plan) - Microsoft Learn search excerpts reviewed.
- [azurekid/ScEntra](https://github.com/azurekid/ScEntra/blob/main/README.md) - Public README read.

---

## 22. The MFA myth: users are not workloads

**CONTROL REALITY** | Use the right control for the identity type.

- **HUMAN USERS:** Authentication policy coverage, phishing-resistant methods and secure sessions.
- **SERVICE PRINCIPALS:** Scoped grants, credential lifecycle and supported workload-identity CA policies.
- **MANAGED IDENTITIES:** Workload execution boundaries, least privilege and controlled attachment/federation writers.

**Speaker notes:** Microsoft's workload Conditional Access documentation describes policies for supported organization-owned service principals, with block controls, not interactive MFA. Feature eligibility and Workload Identities Premium licensing matter. Managed identities are not covered by these service-principal controls; Microsoft's workload CAE page explicitly excludes them. An assertion that 'we require MFA for everybody' is therefore not evidence of workload identity protection. Federation is good credential hygiene but does not solve code control or excess authority.

**Sources:**
- [Microsoft Learn: Conditional Access for workload identities](https://learn.microsoft.com/en-us/entra/identity/conditional-access/workload-identity) - Microsoft Learn search excerpts reviewed; direct page retrieval failed.
- [Microsoft Learn: Continuous access evaluation for workload identities](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-continuous-access-evaluation-workload) - Microsoft Learn search excerpts reviewed. Managed identities are not supported.
- [Microsoft Learn: Use managed identities on an Azure VM](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-to-use-vm-token) - Microsoft Learn search excerpts reviewed; direct page retrieval failed.
- [azurekid/VizCa](https://github.com/azurekid/VizCa/blob/main/README.md) - Public README read.

---

## 23. What to do on Monday

**TAKEAWAY** | Start with powerful identities and the people or code that can become them.

- **DISCOVER:** Inventory sensitive grants and indirect writers. Visualize candidate paths with ScEntra.
- **CONSTRAIN:** Close CA gaps with VizCa; narrow workload grants; protect federation and privileged code changes.
- **VALIDATE + WATCH:** Use safe BlackCat assessments; standardize PIM; validate identity-to-resource detection stories.

**Speaker notes:** Avoid unsupported percentages or an invented risk-reduction promise. Establish a baseline: identities with sensitive standing grants, exceptions with compensating controls, credential/trust writers, paths validated and paths removed. Track whether synthetic canary access is denied after remediation while intended workload behavior remains healthy. Choose one high-impact trust chain rather than trying to fix every repository or policy at once.

**Sources:**
- [azurekid/ScEntra](https://github.com/azurekid/ScEntra/blob/main/README.md) - Public README read.
- [azurekid/VizCa](https://github.com/azurekid/VizCa/blob/main/README.md) - Public README read.
- [azurekid/blackcat](https://github.com/azurekid/blackcat/blob/main/README.md) - Public README read.
- [azurekid/PIM](https://github.com/azurekid/PIM/blob/main/README.md) - Public README read.
- [azurekid/policy-as-code](https://github.com/azurekid/policy-as-code/blob/main/README.md) - Public README read.
- [azurekid/DefenderXDR](https://github.com/azurekid/DefenderXDR/blob/main/README.md) - Public README read.

---

## 24. Your perimeter is the trust graph.

**CLOSING** | Not the test label. Not the absence of secrets. Not a successful MFA prompt.

- **REMEMBER:** Authentication proves an identity, not an intention.
- **ASK:** Who can act as our most powerful workload?
- **BREAK:** Remove one unnecessary trust edge before it becomes the next incident.

**Speaker notes:** End with the opening question. The real incident showed a test-to-production bridge. The lab examples showed six ways identity control can arise: forgotten user coverage, leaked app credential, compromised compute, identity writers, delegated remediation and agent tool misuse. The common solution is to review both grants and who can influence the identity. Sources and all 61 public repositories follow as backup slides. Website article bodies remain unverified due to DNS failure in this research environment.

**Sources:**
- [Microsoft Security Blog, 25 January 2024: Midnight Blizzard](https://www.microsoft.com/en-us/security/blog/2024/01/25/midnight-blizzard-guidance-for-responders-on-nation-state-attack/) - Directly read. Historical incident; not a claim about current EWS availability.
- [azurekid/ScEntra](https://github.com/azurekid/ScEntra/blob/main/README.md) - Public README read.
- [azurekid/blackcat](https://github.com/azurekid/blackcat/blob/main/README.md) - Public README read.

---

## 25. Evidence and boundaries

**SOURCE TRANSPARENCY** | What was reviewed, what was inferred, and what was not executed.

- **REVIEWED:** 61 public repositories inventoried; 59 READMEs retrieved. Microsoft incident source directly read.
- **QUALIFIED:** Microsoft Learn search excerpts reviewed. Four AzureHacking links found in BlackCat README.
- **NOT CLAIMED:** No private projects, executed attack paths, customer incident, live demo results or measured detection coverage.

**Speaker notes:** Research snapshot: 9 November 2026. azurehacking.com and www.azurehacking.com did not resolve from this environment; article links and topics came from the public BlackCat README, not retrieved article bodies. The two repositories without an accessible README were 1Password-Sentinel and mc2connect. Every project's inventory entry identifies whether it is a fork and whether the assessment is README-backed or metadata-only. The policy-as-code README has an Owner-payload claim that cannot be justified by ordinary Contributor alone; this deck explicitly limits impact to actual effective permissions. Project READMEs are documentation evidence, not independent code validation.

**Sources:**
- [azurekid/blackcat](https://github.com/azurekid/blackcat/blob/main/README.md) - Public README read.
- [azurekid/policy-as-code](https://github.com/azurekid/policy-as-code/blob/main/README.md) - Public README read.
- [Microsoft Security Blog, 25 January 2024: Midnight Blizzard](https://www.microsoft.com/en-us/security/blog/2024/01/25/midnight-blizzard-guidance-for-responders-on-nation-state-attack/) - Directly read. Historical incident; not a claim about current EWS availability.

---

## 26. All projects / 1 of 7

**REPOSITORY APPENDIX** | Complete public inventory; primary examples are intentionally curated.

- **1Password-Sentinel:** PROJECT / METADATA ONLY Metadata-only: 1Password to Sentinel integration
- **AADInternals:** FORK Upstream fork / supporting reference; not claimed as original authorship
- **AgentTrap:** PROJECT AgentLens defensive inspection platform
- **AzShortLink:** PROJECT Supporting project context; not asserted to be an identity attack tool
- **azure-docs:** FORK Upstream fork / supporting reference; not claimed as original authorship
- **Azure-Lighthouse-samples:** FORK Upstream fork / supporting reference; not claimed as original authorship
- **azure-opt:** PROJECT Supporting project context; not asserted to be an identity attack tool
- **azure-orphan-resources:** FORK Upstream fork / supporting reference; not claimed as original authorship
- **azure-powershell:** FORK Upstream fork / supporting reference; not claimed as original authorship

**Speaker notes:** Backup slide, not part of the timed talk. Each repository title links to its public GitHub repository. Do not infer a security capability from a repository name. For non-primary projects the exact public description and README availability are preserved in source-inventory.md and repository-research.json.

**Sources:**
- [azurekid/1Password-Sentinel](https://github.com/azurekid/1Password-Sentinel) - Repository metadata only; no accessible README.
- [azurekid/AADInternals (fork)](https://github.com/azurekid/AADInternals/blob/master/README.md) - Public README read.
- [azurekid/AgentTrap](https://github.com/azurekid/AgentTrap/blob/main/README.md) - Public README read.
- [azurekid/AzShortLink](https://github.com/azurekid/AzShortLink/blob/main/README.md) - Public README read.
- [azurekid/azure-docs (fork)](https://github.com/azurekid/azure-docs/blob/master/README.md) - Public README read.
- [azurekid/Azure-Lighthouse-samples (fork)](https://github.com/azurekid/Azure-Lighthouse-samples/blob/master/README.md) - Public README read.
- [azurekid/azure-opt](https://github.com/azurekid/azure-opt/blob/main/README.md) - Public README read.
- [azurekid/azure-orphan-resources (fork)](https://github.com/azurekid/azure-orphan-resources/blob/main/README.md) - Public README read.
- [azurekid/azure-powershell (fork)](https://github.com/azurekid/azure-powershell/blob/master/README.md) - Public README read.

---

## 27. All projects / 2 of 7

**REPOSITORY APPENDIX** | Complete public inventory; primary examples are intentionally curated.

- **azure-resource-manager-schemas:** FORK Upstream fork / supporting reference; not claimed as original authorship
- **Azure-Sentinel:** FORK Upstream fork / supporting reference; not claimed as original authorship
- **Azure-Stencils:** PROJECT Supporting project context; not asserted to be an identity attack tool
- **azurekid:** PROJECT Presenter profile and project attribution
- **AzurePermissionInsight:** FORK Upstream fork / supporting reference; not claimed as original authorship
- **Bio-Compliancy:** FORK Upstream fork / supporting reference; not claimed as original authorship
- **blackcat:** PROJECT Authorized Azure/Entra security validation
- **blog:** PROJECT Supporting project context; not asserted to be an identity attack tool
- **bluemountainbank:** PROJECT Supporting project context; not asserted to be an identity attack tool

**Speaker notes:** Backup slide, not part of the timed talk. Each repository title links to its public GitHub repository. Do not infer a security capability from a repository name. For non-primary projects the exact public description and README availability are preserved in source-inventory.md and repository-research.json.

**Sources:**
- [azurekid/azure-resource-manager-schemas (fork)](https://github.com/azurekid/azure-resource-manager-schemas/blob/master/README.md) - Public README read.
- [azurekid/Azure-Sentinel (fork)](https://github.com/azurekid/Azure-Sentinel/blob/master/README.md) - Public README read.
- [azurekid/Azure-Stencils](https://github.com/azurekid/Azure-Stencils/blob/master/README.md) - Public README read.
- [azurekid/azurekid](https://github.com/azurekid/azurekid/blob/main/README.md) - Public README read.
- [azurekid/AzurePermissionInsight (fork)](https://github.com/azurekid/AzurePermissionInsight/blob/main/README.md) - Public README read.
- [azurekid/Bio-Compliancy (fork)](https://github.com/azurekid/Bio-Compliancy/blob/main/README.md) - Public README read.
- [azurekid/blackcat](https://github.com/azurekid/blackcat/blob/main/README.md) - Public README read.
- [azurekid/blog](https://github.com/azurekid/blog/blob/master/README.md) - Public README read.
- [azurekid/bluemountainbank](https://github.com/azurekid/bluemountainbank/blob/main/README.md) - Public README read.

---

## 28. All projects / 3 of 7

**REPOSITORY APPENDIX** | Complete public inventory; primary examples are intentionally curated.

- **bluemountaintravel:** PROJECT Supporting project context; not asserted to be an identity attack tool
- **cloud-custodian:** FORK Upstream fork / supporting reference; not claimed as original authorship
- **codespaces:** PROJECT Supporting project context; not asserted to be an identity attack tool
- **Copilot-For-Security:** FORK Upstream fork / supporting reference; not claimed as original authorship
- **DefenderXDR:** PROJECT Defender XDR configuration and security operations
- **detection-mcp:** PROJECT Detection engineering MCP server
- **doodle-to-code:** FORK Upstream fork / supporting reference; not claimed as original authorship
- **extensions:** PROJECT Supporting project context; not asserted to be an identity attack tool
- **fastbuster:** PROJECT Supporting project context; not asserted to be an identity attack tool

**Speaker notes:** Backup slide, not part of the timed talk. Each repository title links to its public GitHub repository. Do not infer a security capability from a repository name. For non-primary projects the exact public description and README availability are preserved in source-inventory.md and repository-research.json.

**Sources:**
- [azurekid/bluemountaintravel](https://github.com/azurekid/bluemountaintravel/blob/main/README.md) - Public README read.
- [azurekid/cloud-custodian (fork)](https://github.com/azurekid/cloud-custodian/blob/master/README.md) - Public README read.
- [azurekid/codespaces](https://github.com/azurekid/codespaces/blob/main/README.md) - Public README read.
- [azurekid/Copilot-For-Security (fork)](https://github.com/azurekid/Copilot-For-Security/blob/main/README.md) - Public README read.
- [azurekid/DefenderXDR](https://github.com/azurekid/DefenderXDR/blob/main/README.md) - Public README read.
- [azurekid/detection-mcp](https://github.com/azurekid/detection-mcp/blob/main/README.md) - Public README read.
- [azurekid/doodle-to-code (fork)](https://github.com/azurekid/doodle-to-code/blob/main/README.md) - Public README read.
- [azurekid/extensions](https://github.com/azurekid/extensions/blob/master/README.md) - Public README read.
- [azurekid/fastbuster](https://github.com/azurekid/fastbuster/blob/main/README.md) - Public README read.

---

## 29. All projects / 4 of 7

**REPOSITORY APPENDIX** | Complete public inventory; primary examples are intentionally curated.

- **HashSight:** PROJECT Supporting project context; not asserted to be an identity attack tool
- **jsonize:** PROJECT Supporting project context; not asserted to be an identity attack tool
- **KeepIt:** PROJECT Supporting project context; not asserted to be an identity attack tool
- **key-vault-function:** PROJECT Supporting Custom Log Function / Key Vault integration
- **linkedin-skill-assessments-quizzes:** FORK Upstream fork / supporting reference; not claimed as original authorship
- **mc2-connect:** PROJECT Supporting project context; not asserted to be an identity attack tool
- **mc2connect:** PROJECT / METADATA ONLY Metadata-only: mc2 connect use case
- **Microsoft-Defender-for-Cloud:** FORK Upstream fork / supporting reference; not claimed as original authorship
- **Microsoft-Sentinel2Go:** FORK Upstream fork / supporting reference; not claimed as original authorship

**Speaker notes:** Backup slide, not part of the timed talk. Each repository title links to its public GitHub repository. Do not infer a security capability from a repository name. For non-primary projects the exact public description and README availability are preserved in source-inventory.md and repository-research.json.

**Sources:**
- [azurekid/HashSight](https://github.com/azurekid/HashSight/blob/main/README.md) - Public README read.
- [azurekid/jsonize](https://github.com/azurekid/jsonize/blob/main/README.md) - Public README read.
- [azurekid/KeepIt](https://github.com/azurekid/KeepIt/blob/main/README.md) - Public README read.
- [azurekid/key-vault-function](https://github.com/azurekid/key-vault-function/blob/main/readme.md) - Public README read.
- [azurekid/linkedin-skill-assessments-quizzes (fork)](https://github.com/azurekid/linkedin-skill-assessments-quizzes/blob/master/README.md) - Public README read.
- [azurekid/mc2-connect](https://github.com/azurekid/mc2-connect/blob/main/README.md) - Public README read.
- [azurekid/mc2connect](https://github.com/azurekid/mc2connect) - Repository metadata only; no accessible README.
- [azurekid/Microsoft-Defender-for-Cloud (fork)](https://github.com/azurekid/Microsoft-Defender-for-Cloud/blob/main/README.md) - Public README read.
- [azurekid/Microsoft-Sentinel2Go (fork)](https://github.com/azurekid/Microsoft-Sentinel2Go/blob/master/README.md) - Public README read.

---

## 30. All projects / 5 of 7

**REPOSITORY APPENDIX** | Complete public inventory; primary examples are intentionally curated.

- **operation-blackcat:** PROJECT Investigation exercise context; not a documented Entra breach
- **PaC:** PROJECT PIM-as-code policy configuration
- **ParcelPinPoint:** PROJECT Supporting project context; not asserted to be an identity attack tool
- **pester-tests-report:** FORK Upstream fork / supporting reference; not claimed as original authorship
- **Piceb:** PROJECT PIM deployment and management using Bicep
- **PIM:** PROJECT PIM policy configuration automation
- **policy-as-code:** PROJECT Pipeline and remediation identity trust demonstration
- **r1ckr0ll3r:** PROJECT Supporting project context; not asserted to be an identity attack tool
- **ScEntra:** PROJECT Identity relationship and candidate escalation-path analysis

**Speaker notes:** Backup slide, not part of the timed talk. Each repository title links to its public GitHub repository. Do not infer a security capability from a repository name. For non-primary projects the exact public description and README availability are preserved in source-inventory.md and repository-research.json.

**Sources:**
- [azurekid/operation-blackcat](https://github.com/azurekid/operation-blackcat/blob/main/README.md) - Public README read.
- [azurekid/PaC](https://github.com/azurekid/PaC/blob/main/README.md) - Public README read.
- [azurekid/ParcelPinPoint](https://github.com/azurekid/ParcelPinPoint/blob/main/README.md) - Public README read.
- [azurekid/pester-tests-report (fork)](https://github.com/azurekid/pester-tests-report/blob/master/README.md) - Public README read.
- [azurekid/Piceb](https://github.com/azurekid/Piceb/blob/main/README.md) - Public README read.
- [azurekid/PIM](https://github.com/azurekid/PIM/blob/main/README.md) - Public README read.
- [azurekid/policy-as-code](https://github.com/azurekid/policy-as-code/blob/main/README.md) - Public README read.
- [azurekid/r1ckr0ll3r](https://github.com/azurekid/r1ckr0ll3r/blob/main/README.md) - Public README read.
- [azurekid/ScEntra](https://github.com/azurekid/ScEntra/blob/main/README.md) - Public README read.

---

## 31. All projects / 6 of 7

**REPOSITORY APPENDIX** | Complete public inventory; primary examples are intentionally curated.

- **sentinel-deploy:** PROJECT Supporting project context; not asserted to be an identity attack tool
- **Sentinel-playground:** FORK Upstream fork / supporting reference; not claimed as original authorship
- **shadowcat:** PROJECT Supporting Windows security research platform
- **sigma:** FORK Upstream fork / supporting reference; not claimed as original authorship
- **SigmaXDR:** PROJECT Sigma to Defender XDR detection conversion
- **skills-code-with-codespaces:** PROJECT Supporting project context; not asserted to be an identity attack tool
- **skills-copilot-codespaces-vscode:** PROJECT Supporting project context; not asserted to be an identity attack tool
- **skills-introduction-to-github:** PROJECT Supporting project context; not asserted to be an identity attack tool
- **skillseal:** PROJECT Approved skill signing and verification

**Speaker notes:** Backup slide, not part of the timed talk. Each repository title links to its public GitHub repository. Do not infer a security capability from a repository name. For non-primary projects the exact public description and README availability are preserved in source-inventory.md and repository-research.json.

**Sources:**
- [azurekid/sentinel-deploy](https://github.com/azurekid/sentinel-deploy/blob/main/README.md) - Public README read.
- [azurekid/Sentinel-playground (fork)](https://github.com/azurekid/Sentinel-playground/blob/main/README.md) - Public README read.
- [azurekid/shadowcat](https://github.com/azurekid/shadowcat/blob/main/README.md) - Public README read.
- [azurekid/sigma (fork)](https://github.com/azurekid/sigma/blob/master/README.md) - Public README read.
- [azurekid/SigmaXDR](https://github.com/azurekid/SigmaXDR/blob/main/README.md) - Public README read.
- [azurekid/skills-code-with-codespaces](https://github.com/azurekid/skills-code-with-codespaces/blob/main/README.md) - Public README read.
- [azurekid/skills-copilot-codespaces-vscode](https://github.com/azurekid/skills-copilot-codespaces-vscode/blob/main/README.md) - Public README read.
- [azurekid/skills-introduction-to-github](https://github.com/azurekid/skills-introduction-to-github/blob/main/README.md) - Public README read.
- [azurekid/skillseal](https://github.com/azurekid/skillseal/blob/main/README.md) - Public README read.

---

## 32. All projects / 7 of 7

**REPOSITORY APPENDIX** | Complete public inventory; primary examples are intentionally curated.

- **SkillVenom:** PROJECT Defanged agent-file attack research catalogue
- **spraycat:** PROJECT Authorized password-spray testing reference; no live attack required
- **SQLizer:** PROJECT Supporting project context; not asserted to be an identity attack tool
- **steampipe:** FORK Upstream fork / supporting reference; not claimed as original authorship
- **template-analyzer:** FORK Upstream fork / supporting reference; not claimed as original authorship
- **VizCa:** PROJECT Conditional Access visualization and coverage analysis
- **warstick:** PROJECT Supporting project context; not asserted to be an identity attack tool

**Speaker notes:** Backup slide, not part of the timed talk. Each repository title links to its public GitHub repository. Do not infer a security capability from a repository name. For non-primary projects the exact public description and README availability are preserved in source-inventory.md and repository-research.json.

**Sources:**
- [azurekid/SkillVenom](https://github.com/azurekid/SkillVenom/blob/main/README.md) - Public README read.
- [azurekid/spraycat](https://github.com/azurekid/spraycat/blob/main/README.MD) - Public README read.
- [azurekid/SQLizer](https://github.com/azurekid/SQLizer/blob/main/README.md) - Public README read.
- [azurekid/steampipe (fork)](https://github.com/azurekid/steampipe/blob/main/README.md) - Public README read.
- [azurekid/template-analyzer (fork)](https://github.com/azurekid/template-analyzer/blob/main/README.md) - Public README read.
- [azurekid/VizCa](https://github.com/azurekid/VizCa/blob/main/README.md) - Public README read.
- [azurekid/warstick](https://github.com/azurekid/warstick/blob/main/README.md) - Public README read.

---

## 33. Read next / Your research

**FURTHER READING** | AzureHacking links are cited by your BlackCat README; article bodies were not retrieved.

- **Azure Tenant Takeover: From Exposed Config to Global Admin:** azurehacking.com tabletop-tenant-takeover-scenario
- **Detecting Privilege Escalation in Entra ID:** azurehacking.com detecting-privilege-escalation-in-entra-id
- **ScEntra: Visualizing Entra ID Privilege Escalation Paths:** azurehacking.com scentra-visualizing-entra-id-privilege-escalation-paths
- **Impairing Azure Defenses Through Diagnostic Setting Manipulation:** azurehacking.com impairing-azure-defenses-through-diagnostic-setting-manipulation

**Speaker notes:** These are further-reading links, not verified article summaries. Restore website access and review the article bodies before quoting them or claiming their specific examples. The deck's technical claims are supported by reviewed repository documentation and Microsoft sources instead.

**Sources:**
- [Azure Tenant Takeover: From Exposed Config to Global Admin](https://azurehacking.com/post.html?slug=tabletop-tenant-takeover-scenario) - Link/topic found in BlackCat README. Article body NOT retrieved; website DNS failed.
- [Detecting Privilege Escalation in Entra ID](https://azurehacking.com/post.html?slug=detecting-privilege-escalation-in-entra-id) - Link/topic found in BlackCat README. Article body NOT retrieved; website DNS failed.
- [ScEntra: Visualizing Entra ID Privilege Escalation Paths](https://azurehacking.com/post.html?slug=scentra-visualizing-entra-id-privilege-escalation-paths) - Link/topic found in BlackCat README. Article body NOT retrieved; website DNS failed.
- [Impairing Azure Defenses Through Diagnostic Setting Manipulation](https://azurehacking.com/post.html?slug=impairing-azure-defenses-through-diagnostic-setting-manipulation) - Link/topic found in BlackCat README. Article body NOT retrieved; website DNS failed.
- [azurekid/blackcat](https://github.com/azurekid/blackcat/blob/main/README.md) - Public README read.

---

## 34. Read next / The incident and controls

**REFERENCES** | Primary vendor sources, with retrieval status in the companion source inventory.

- **Microsoft / Midnight Blizzard:** The January 2024 incident chain and responder guidance.
- **Microsoft / Managed identities:** VM execution is the identity security boundary.
- **Microsoft / Workload CA and CAE:** Supported identity types, licensing and revocation limitations.
- **Microsoft / PIM:** Time-bound and approval-based privilege activation.

**Speaker notes:** This is a source slide. All exact URLs are included as clickable links and in the Markdown notes. The historical incident blog was directly read; Microsoft Learn pages were reviewed through search excerpts because direct retrieval failed. Reconfirm current feature support before implementing controls.

**Sources:**
- [Microsoft Security Blog, 25 January 2024: Midnight Blizzard](https://www.microsoft.com/en-us/security/blog/2024/01/25/midnight-blizzard-guidance-for-responders-on-nation-state-attack/) - Directly read. Historical incident; not a claim about current EWS availability.
- [Microsoft Learn: Use managed identities on an Azure VM](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-to-use-vm-token) - Microsoft Learn search excerpts reviewed; direct page retrieval failed.
- [Microsoft Learn: Conditional Access for workload identities](https://learn.microsoft.com/en-us/entra/identity/conditional-access/workload-identity) - Microsoft Learn search excerpts reviewed; direct page retrieval failed.
- [Microsoft Learn: Continuous access evaluation for workload identities](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-continuous-access-evaluation-workload) - Microsoft Learn search excerpts reviewed. Managed identities are not supported.
- [Microsoft Learn: Plan a PIM deployment](https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-deployment-plan) - Microsoft Learn search excerpts reviewed.
