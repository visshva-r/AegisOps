# AegisOps — Video Demo Narration Script

**Target Duration:** ~2 minutes 45 seconds  
**Live Target Run ID (Demo Reference):** `0ef8cf7c-de50-40fe-a2e3-38ffe4aabff9`  
**Application URL:** `http://127.0.0.1:8000/`

---

## Narration Timeline (B0 → B5)

| Time | Browser Action | Spoken Line | Highlight on Screen |
|:---|:---|:---|:---|
| **0:00 – 0:15** | Open `http://127.0.0.1:8000/`. Scroll down to view the Integration Matrix and Recent Lab Runs table. | *"Hello judges, welcome to AegisOps — an AI-powered Unified VAPT Agent built for safe, authorized security assessments. On the homepage, notice our transparent Integration Matrix: we clearly label tools as Live, Import, or Planned — zero fake-live simulation. Below, our persistent SQLite history tracks recent lab assessments."* | Hover over green/blue/gold tags in the Integration Matrix and point out Recent Lab Runs rows. |
| **0:15 – 0:35** | Clear Target input, type `8.8.8.8`, and click **"Validate scope & generate plan"**. | *"Before launching any scan, safety is non-negotiable. Watch what happens if an analyst enters an out-of-scope external target like 8.8.8.8. AegisOps rejects it immediately with an HTTP 400 error banner. No scans are executed, and zero unauthorized data is persisted."* | Highlight the red alert box: `Target '8.8.8.8' is outside authorized lab scope`. |
| **0:35 – 1:05** | Enter target `lab.vapt.local`, leave pre-filled natural language request, and click **"Validate scope & generate plan"**. | *"Now we submit an authorized lab assessment for lab.vapt.local with a natural-language mission goal. AegisOps validates the lab boundary and dynamically builds an adaptive 3-phase plan: starting with Nmap for port discovery, feeding that service context into Nikto for web misconfigurations, and chaining into OWASP ZAP for application testing without redundant scans."* | Highlight green scope validation banner, `status-planned` badge, and the numbered 3-step plan rationale. |
| **1:05 – 1:45** | Click **"Execute approved scan orchestration"**. Page reloads with findings and approval card. | *"We click 'Execute approved scan orchestration'. In sub-second time, AegisOps ingests the multi-tool outputs. Notice the Tool Runs table: each tool execution maps to verified evidence files. Below, our correlation engine deduplicates findings, calculates confidence scores, and separates observed evidence from inferred findings."* | Point to Tool Runs output paths under `fixtures/`, severity tags in the Unified Findings table, and the amber `status-awaiting_approval` badge. |
| **1:45 – 2:15** | Scroll to the amber **"Human approval required"** card. Type `Demo approval for hackathon video` into Note field and click **"Approve validation"**. | *"Here is our core safety principle: AegisOps will never autonomously exploit a target. Because high-severity vulnerabilities were identified, execution halts at this human-in-the-loop gate. As the authorized analyst, I review the validation queue, enter our approval note, and click Approve."* | Highlight the amber warning banner, the Approval form fields, and click the cyan Approve button. |
| **2:15 – 2:35** | Page refreshes with green completion banner. Scroll down to show Audit Trail. | *"Immediately, the status badge updates to 'complete', the approval form is dismissed, and an immutable audit trail records our human approval alongside the simulated Metasploit validation stub with exact UTC timestamps."* | Highlight the green banner `Assessment completed · Human validation approval logged`, `status-complete` badge, and audit entries `approval_granted` & `metasploit_stub`. |
| **2:35 – 2:50** | Click **"Download VAPT PDF"**, then click **"← New assessment"** to return home. | *"With one click, we download the official client-ready VAPT PDF report. Returning to the homepage, our assessment is automatically cataloged in the Recent Lab Runs table. AegisOps delivers unified, intelligent VAPT orchestration while keeping the human firmly in control."* | Point to downloaded PDF file in browser bar and the top row of Recent Lab Runs showing status `complete`. |

---

## Presenter Closing Statement (Human-in-the-Loop & Safety)

> *"In conclusion, AegisOps solves the twin challenges of modern vulnerability assessments: tool fragmentation and uncontrolled AI autonomy. By grounding conversational AI in strict scope boundaries, transparent tool integration, multi-source correlation, and mandatory human authorization for intrusive actions, AegisOps provides an enterprise-ready blueprint for the future of AI-assisted cybersecurity."*

