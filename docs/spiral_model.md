# Spiral Model (SDLC) for “AI Doctor”

> This document describes the project lifecycle using the **Spiral Model** tailored to your **Flask + ML symptom prediction** and **doctor finder** web application.

## 1) Why Spiral Model for this project
Your system contains multiple risk areas that benefit from iterative refinement:
- **ML behavior risk**: model predictions may not match expectations for real inputs.
- **Data risk**: symptom-to-disease mappings and doctor datasets can be incomplete or inconsistent.
- **Integration risk**: Flask routes, JS UI, and backend prediction/doctor-search need to work together.
- **Deployment risk**: XAMPP ↔ Flask proxy/routing must behave correctly.

The Spiral Model provides repeated cycles of:
1. planning,
2. risk analysis,
3. engineering/implementation,
4. validation (testing) and stakeholder feedback.

---

## 2) Overview of the spiral (Cycles)
Use 4 cycles (you can extend later if needed).

### Cycle 1 — Foundations + Baseline Feasibility
**Objectives**
- Establish working baseline for the application flow.
- Confirm the end-to-end path: UI → Flask → ML service → UI.

**Key activities**
- Verify Flask app boot, routing, templates rendering.
- Validate models load correctly (`decision_tree.pkl`, `random_forest.pkl`).
- Confirm symptom input handling (selected symptoms) and result rendering.
- Run basic tests (`test_end_to_end.py`, `test_fix.py`) if available.

**Risk analysis (examples)**
- Risk: models are missing/wrong format → mitigation: add a startup check + clear errors.
- Risk: symptom mapping mismatch → mitigation: validate mapping keys/types.

**Deliverables**
- Running app at `http://localhost:5000`.
- Minimal working prediction results (even if accuracy is not final).

**Validation**
- Manual test with a few known symptom sets.
- Confirm JSON reads succeed from `data/*.json`.

---

### Cycle 2 — Improve Prediction Correctness + Combination Logic
**Objectives**
- Improve correctness of predicted diseases and alternative suggestions.
- Make two-symptom and multi-symptom combination logic more robust.

**Key activities**
- Audit and refine `services/symptom_mapper.py`:
  - how symptom combinations map to diseases,
  - how missing/extra symptom noise is handled,
  - how confidence scores are computed.
- Update data generation/cleaning scripts if needed:
  - verify `data/symptom_disease_map.json`, `data/symptom_disease_dataset.csv` consistency.
- Retrain models using updated dataset rules (if applicable).

**Risk analysis (examples)**
- Risk: confidence score is not meaningful → mitigation: compare predicted ranking stability.
- Risk: combination logic overfits to synthetic patterns → mitigation: add noise tests and edge-case tests.

**Deliverables**
- Better prediction outputs (primary + alternatives).
- Updated dataset or mapping files (with versioning/backups).

**Validation**
- Run `test_notes_combinations.py` (if it targets combination scenarios).
- Regression check: compare outputs across old vs new dataset versions.

---

### Cycle 3 — Doctor Finder + Data Quality + UX Hardening
**Objectives**
- Ensure doctor finder works accurately for location/specialty/taluk.
- Improve UX responsiveness and reliability.

**Key activities**
- Review doctor dataset structure and matching logic (from `data/doctors_database*.json`).
- Validate search/sort behavior:
  - distance-based sorting,
  - correct district/taluk mapping,
  - correct Google Maps links.
- Update frontend JS if needed:
  - error handling for empty results,
  - loading states,
  - consistent UI labels.

**Risk analysis (examples)**
- Risk: missing coordinates or broken map URLs → mitigation: add dataset validation scripts.
- Risk: performance slowdowns when filtering many doctors → mitigation: optimize data filtering and pre-indexing.

**Deliverables**
- Reliable doctor results page (`templates/consult.html`).
- Clean and validated doctor dataset subset(s) if needed.

**Validation**
- Test at least one location per district.
- Confirm 0-result and error paths are handled gracefully.

---

### Cycle 4 — Deployment + Security + Maintainability
**Objectives**
- Ensure stable deployment in XAMPP environment.
- Harden configuration, improve maintainability, and document usage.

**Key activities**
- Confirm XAMPP proxy/routing works:
  - `index.php`, `proxy.php`, `.htaccess`.
- Add/verify logging:
  - server errors,
  - prediction request/response health.
- Add basic security hardening:
  - input validation for symptom selection,
  - safe handling for JSON parsing.

**Risk analysis (examples)**
- Risk: environment differences (Windows paths vs expected paths) → mitigation: use robust path resolution.
- Risk: missing dependencies on target machine → mitigation: document `requirements.txt` and setup steps.

**Deliverables**
- Stable deployment procedure in README.
- Consistent folder structure and versioned datasets.

**Validation**
- End-to-end test using XAMPP entry (`index.php`).
- Smoke test: load UI and run one full prediction + doctor search.

---

## 3) Spiral Model cycle template (repeatable)
For each cycle, follow this loop:
1. **Plan**: decide which features/risk areas to target.
2. **Risk Analysis**: identify biggest uncertainties; design mitigations.
3. **Engineering**: implement changes (code + data/model updates).
4. **Evaluation**: test + stakeholder review.
5. **Next cycle selection**: select next highest-risk improvements.

---

## 4) Stakeholders & feedback points
- End users (via UI tests): validate output clarity (disease, alternatives, alerts).
- Project developer(s): validate code correctness and integration.
- Maintainer: validate data integrity and reproducibility.

Feedback triggers typically happen after each cycle’s validation step.

---

## 5) Suggested timeline (example)
You can map cycles to weeks depending on your schedule:
- Cycle 1: 1 week
- Cycle 2: 1–2 weeks
- Cycle 3: 1–2 weeks
- Cycle 4: 1 week

---

## 6) Notes / Safety statement
This project is for learning and assistance only. It should not replace professional medical advice.

---

## 7) How to use this doc
- When you make major changes to models/data/UI, start a new spiral cycle.
- Update this document with:
  - what was changed,
  - which tests were run,
  - what risks were mitigated.

