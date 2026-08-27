# Development Log - azure-blob-ai-doc-summarizer

Auto-generated journal of project changes.
Generated: 2026-01-05 19:39

## 2026-08-27 18:33

**Commit:** `e59360c`

fix(ci): repair invalid HCL that broke terraform init

variables.tf declared its variables as single-line blocks holding two
arguments each; HCL allows only one argument in single-line form, so
'terraform init' could not parse the module and CI has been red since
2026-01-23. Expanded the required_providers, provider features and
site_config blocks the same way, ran terraform fmt, and marked
azure_openai_key sensitive.

Verified locally: terraform fmt -check, init -backend=false and
validate all pass.

**Files:** infra/main.tf,infra/variables.tf

---


## 2026-01-23 12:37

**Commit:** 

Auto-update DEVLOG.md

**Files:** DEVLOG.md

---


## 2026-01-23 12:34

**Commit:** 

Update .gitignore and sync CHANGELOG/DEVLOG files

**Files:** .gitignore,CHANGELOG.md,DEVLOG.md

---


## 2025-12-25

**Commit:** `242ec59`

Add .DS_Store to gitignore

---

## 2025-10-03

**Commit:** `f327f78`

fix: Add white background to SVG diagrams for dark mode visibility

---

## 2025-10-03

**Commit:** `9e4d433`

docs: Add documentation and diagrams

---

## 2025-10-03

**Commit:** `f281ab4`

Update README.md

---

## 2025-10-03

**Commit:** `0528631`

Update README.md

---

## 2025-10-03

**Commit:** `36d048e`

Update README.md

---

## 2025-10-03

**Commit:** `d0434ee`

feat: initial commit

---

