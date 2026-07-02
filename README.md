# Profile Maker

Profile Maker is a one-time companion tool for Career Agent.

It reads all supported career-related documents placed inside the `data/` folder, extracts factual career evidence from each document, and creates two reviewable candidate profile drafts.

The user should manually review those drafts and then manually create the final `candidate_profile.json` for Career Agent.

---

## Purpose

The goal is to transform messy personal career documents into compact, structured candidate knowledge that can later support:

- CV tailoring
- Cover letter generation
- truthfulness checking
- evidence-aware job application workflows

Profile Maker does **not** depend on fixed input file names such as `master_cv.tex`, `master_thesis.pdf`, or `reference_letters.pdf`.

Any supported file inside `data/` will be processed automatically.

---

## Supported Input Files

Place career-related files inside:

```text
data/
```

Supported file types:

```text
.pdf
.tex
.txt
.md
.docx
.json
.csv
```

Example:

```text
data/
cv.pdf
data/thesis.pdf
data/reference_letter_1.pdf
data/certificates.pdf
data/project_portfolio.docx
data/extra_notes.md
```

The file names are used only for source tracking in `outputs/00_source_index.json`.
They are not used to decide whether a document is a CV, thesis, reference letter, certificate, or project document.

---

## Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file from `.env.example`:

```bash
copy .env.example .env
```

Then add your API keys inside `.env`.

---

## Main Command

```bash
python profile_maker.py
```

---

## Pipeline

### Stage 0 — Source Discovery

The script scans `data/` recursively and finds all supported documents.

Output:

```text
outputs/00_source_index.json
```

This file maps generic source IDs such as `DOC-001` and `DOC-002` to the original local file paths.

---

### Stage 1 — Generic Document Extraction

Each discovered document is processed with one generic extraction prompt:

```text
prompts/extract_document.txt
```

Outputs:

```text
outputs/01_doc-001_extraction.json
outputs/02_doc-002_extraction.json
...
```

Each extraction also saves the raw model response:

```text
outputs/01_doc-001_extraction.raw.txt
outputs/02_doc-002_extraction.raw.txt
...
```

---

### Stage 2 — Profile Synthesis

Two models create profile draft version 1:

```text
GPT Profile V1
Claude Profile V1
```

Outputs:

```text
outputs/05_candidate_profile_gpt_v1.json
outputs/06_candidate_profile_claude_v1.json
```

---

### Stage 3 — Cross Review

Each model reviews the other model's profile draft.

Outputs:

```text
outputs/07_gpt_review_of_claude.json
outputs/08_claude_review_of_gpt.json
```

---

### Stage 4 — Profile Improvement

Each model creates an improved profile using the cross-review feedback.

Outputs:

```text
outputs/09_candidate_profile_gpt_v2.json
outputs/10_candidate_profile_claude_v2.json
```

---

## Final Human Review

Review these two files manually:

```text
outputs/09_candidate_profile_gpt_v2.json
outputs/10_candidate_profile_claude_v2.json
```

Then manually create:

```text
candidate_profile.json
```

This manually reviewed file is the final profile that Career Agent should consume.

Profile Maker does not automatically generate or overwrite `candidate_profile.json`.

---

## Folder Structure

```text
profile_maker/
├── profile_maker.py
├── requirements.txt
├── .env.example
├── data/
│   └── .gitkeep
├── outputs/
│   └── .gitkeep
├── prompts/
│   ├── extract_document.txt
│   ├── improve_profile.txt
│   ├── review_profile.txt
│   └── synthesize_digital_twin.txt
├── schemas/
└── src/
```

---

## Output Philosophy

The final profile should be:

- truthful
- evidence-aware
- compact
- reusable
- suitable for CV tailoring
- suitable for cover letter generation
- suitable for truthfulness auditing

The objective is not to preserve every detail.

The objective is to preserve the most useful career information in a structured format.

---

## When to Rebuild

Run Profile Maker again when:

- a new CV version is created
- a new role is added
- a thesis, publication, or major project is completed
- a new reference letter is received
- a major certification is obtained
- important career information changes

Otherwise, continue using the existing manually reviewed `candidate_profile.json`.

---

## Git Safety

Do not commit:

```text
.env
data/*
outputs/*
candidate_profile.json
__pycache__/
*.pyc
```

These are ignored by `.gitignore`.
