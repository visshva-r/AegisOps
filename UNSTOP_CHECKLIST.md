# AegisOps — Unstop Submission Pre-Flight Checklist

Ensure every item below is verified prior to the final hackathon submission deadline.

---

## 1. Submission Links Verification
- [ ] **PPT Google Drive Link:**
  - Access setting configured to **"Anyone with the link can view"** (not restricted to domain/organization).
  - Download permission enabled.
- [ ] **Demo Video Google Drive Link:**
  - Video format: MP4 (1080p recommended).
  - Duration: Between 2:30 and 4:00 minutes.
  - Access setting configured to **"Anyone with the link can view"**.
- [ ] **GitHub Repository Link:**
  - Repository visibility set to **Public**.
  - `README.md` includes clear Quick Start instructions and Problem Statement 1 mapping.
  - Integration status matrix is visible in the README.

---

## 2. Incognito / Private Window Verification
- [ ] **Incognito Test — PPT Link:** Opened link in a private/incognito browser window without Google login; slide presentation loads directly.
- [ ] **Incognito Test — Video Link:** Opened link in a private/incognito browser window without Google login; video streams without permission request.
- [ ] **Incognito Test — GitHub Link:** Opened repository in a private window; all source code and markdown documents are accessible.

---

## 3. Slide Deck Structure Compliance (Discord Format)
- [ ] Slide 1: Team Introduction & Problem Statement (PS-1)
- [ ] Slide 2: The Problem
- [ ] Slide 3: Your Solution
- [ ] Slide 4: Project Architecture & Structure
- [ ] Slide 5: Tech Stack
- [ ] Slide 6: Features (PS-1 Judge Checklist items 1–7)
- [ ] Slide 7: Feasibility
- [ ] Slide 8: Limitations
- [ ] Slide 9: Future Scope
- [ ] Embedded evidence figures: `shot1_home_recent.png` through `shot5_complete_audit_pdf.png` included.

---

## 4. Git Initialization & Remote Push Commands

If you have not yet initialized or pushed your local Project folder to your GitHub repository, execute the following commands in PowerShell from the `Project` directory:

```powershell
# 1. Navigate to Project directory
cd "C:\Users\vissh\Documents\My Projects\Hackathon Projects\DataOps Innovation Hackathon 2026\Project"

# 2. Check current status
git status

# 3. If git is uninitialized, initialize and configure remote:
git init
git branch -M main
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPO_NAME>.git

# 4. Stage and commit all project deliverables
git add .
git commit -m "AegisOps: Unified AI VAPT Agent submission pack (PS-1)"

# 5. Push to GitHub
git push -u origin main

# 6. Verify remote URL
git remote -v
```

