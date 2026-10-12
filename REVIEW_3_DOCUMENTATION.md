# DATABASE MANAGEMENT SYSTEMS (CS304)
## FINAL PROJECT IMPLEMENTATION DOCUMENT: REVIEW 3 (WEEK 14)

---

# Title: Front-End Web Application, Full-Stack Database Integration & Systematic Testing for Academic Conference DBMS

**Course Code / Name:** CS304 - Database Management Systems  
**Evaluation Milestone:** Review 3 (Final Evaluation - 15 to 20 Marks)  
**Target Architecture:** Python Flask + SQLite / PostgreSQL / MySQL + Bootstrap 5  
**Date of Review:** October 2026  
**Document Version:** 3.0 (Full-Stack Production Release)  

---

## Executive Summary & Milestone Deliverables

This document presents the complete final realization for **Review 3**, concluding the development of the **Academic Conference Paper Submission and Review System**. Review 3 builds upon the conceptual ER design approved in **Review 1** and the physical schema, dataset, queries, and analytical views approved in **Review 2**, delivering a fully functional, role-based front-end web application with automated business rule enforcement and systematic testing.

The core deliverables completed for Review 3 include:
1. **Front-End Web Application (`app.py`):** An intuitive, responsive web application built with Python Flask and Bootstrap 5, providing role-based portals for Authors, Reviewers, and Program Chairs.
2. **Complete Conference Lifecycle Modules:**
   - *Paper Submission & Multi-Version Lifecycle:* Supports track selection, abstract entry, co-authorship assignment, and revision uploads with changelog tracking.
   - *COI-Aware Reviewer Assignment Engine:* Automatically checks the database for institutional, co-authorship, or advisory conflicts before permitting an assignment.
   - *Double-Blind Peer Review Entry:* Masks author identities and captures multi-criteria numeric ratings (1–10) while separating public constructive feedback from confidential chair remarks.
   - *Editorial Decision Gating:* Enforces the mandatory $\ge 3$ completed reviews quota before allowing a chair verdict to be recorded.
   - *Registration & Collision-Free Timetable:* Validates author registration fees and schedules accepted papers into conference sessions while preventing author schedule collisions across halls.
3. **Live Analytical Reporting Dashboard:** Directly queries the 7 database views created in Review 2 to display pending reviews, reviewer capacity saturation, and track statistics.
4. **Systematic Verification Suite (`test_suite.py`):** Automated test suite verifying 5 critical database constraints and integrity triggers with a 100% pass rate in 0.024s.

---

## Deliverable 1: Full-Stack System Architecture

The system follows a decoupled 3-tier client-server architecture:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            FULL-STACK ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [ CLIENT TIER ]                                                            │
│  Browser Web Interface (HTML5, Bootstrap 5, Jinja2 Templates)               │
│  ├── Author Portal (/author)                                                │
│  ├── Reviewer Portal (/reviewer)                                            │
│  ├── Program Chair Dashboard (/chair)                                       │
│  └── Master Programme Timetable (/schedule)                                 │
│                                      │                                      │
│                                      ▼ HTTP / REST Requests                 │
│                                                                             │
│  [ APPLICATION / CONTROLLER TIER ]                                          │
│  Python Flask Web Engine (app.py)                                           │
│  ├── Input Sanitation & Validation Logic                                    │
│  ├── Conflict of Interest (COI) Pre-Screening Interceptor                    │
│  ├── 3-Review Quota Gatekeeper                                              │
│  ├── Author Schedule Overlap Clash Detector                                 │
│  └── Session & Flash Messaging Controller                                   │
│                                      │                                      │
│                                      ▼ SQL Prepared Statements              │
│                                                                             │
│  [ DATABASE & STORAGE TIER ]                                                │
│  Relational Database Engine (SQLite / PostgreSQL / MySQL)                   │
│  ├── 17 Normalized Tables (3NF)                                             │
│  ├── B-Tree Indexes (track_id, status, reviewer_id, paper_id)               │
│  ├── 7 Live Analytical Views (vw_pending_reviews, vw_track_stats, etc.)     │
│  └── ACID Transaction Management (BEGIN...COMMIT / ROLLBACK)                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Deliverable 2: Five Core Functional Application Modules

### 2.1 Module 1: Paper Submission & Multi-Version Lifecycle (`/author`)
- **Capabilities:**
  - Authors submit manuscript details: Title, Abstract, Conference Track, and Primary/Co-Authors.
  - Generates initial submission record in `Papers` and inserts Version 1 into `Paper_Versions` with file path `p{id}_v1_blind.pdf`.
  - Authors upload subsequent revisions ($V_2, V_3$) with changelog notes.
  - When a paper is accepted, authors can upload the final camera-ready copy (`is_camera_ready = 1`) including author affiliations and acknowledgments.
- **Data Integrity:** `UNIQUE(paper_id, version_num)` prevents version collision; all previous PDF drafts remain immutable in the historical audit log.

### 2.2 Module 2: COI-Aware Reviewer Assignment Engine (`/chair`)
- **Capabilities:**
  - Program Chairs assign candidate reviewers to papers with an evaluation deadline.
  - **Automated COI Interceptor:** Before executing an `INSERT INTO Paper_Assignments`, the engine queries `Reviewer_Conflicts` joined with `Paper_Authors` for all authors of the manuscript.
  - If a conflict (`SAME_INSTITUTION`, `CO_AUTHOR`, `ADVISORY`, `PERSONAL_RELATION`) exists, the application immediately aborts the operation and displays a descriptive alert banner:
    > `❌ INTEGRITY VIOLATION BLOCKED: Reviewer has an active Conflict of Interest ('SAME_INSTITUTION') with author Geoffrey Hinton! Assignment aborted.`
  - Reviewer workload capacity is validated against `Reviewers.max_workload` to avoid evaluator burnout.

### 2.3 Module 3: Double-Blind Peer Review Entry (`/reviewer`)
- **Capabilities:**
  - Reviewers view their assigned papers with masked metadata: manuscript title and abstract are visible, but author names and affiliations are concealed.
  - Reviewers submit numeric ratings on a scale of 1 to 10 across four dimensions:
    1. *Originality* (1–10)
    2. *Technical Soundness* (1–10)
    3. *Writing Clarity* (1–10)
    4. *Overall Score* (1–10)
  - **Dual Feedback Channels:** Captures public constructive feedback visible to the author alongside confidential remarks visible only to the Program Chair.
  - **Atomic Status Update:** Submitting a review atomically updates `Paper_Assignments.status = 'COMPLETED'`.

### 2.4 Module 4: Editorial Decisions & Review Quota Gating (`/chair`)
- **Capabilities:**
  - Program Committee evaluates aggregated paper scores and min/max score spreads.
  - **Mandatory Review Quota Gate:** Enforces that a paper must possess $\ge 3$ completed peer reviews before an editorial verdict (`ACCEPT`, `REJECT`, `MAJOR_REVISION`) can be recorded.
  - If the chair attempts to record a verdict on an under-reviewed paper (e.g., Paper #6 with only 1 completed review), the system displays:
    > `❌ DECISION BLOCKED: Paper #6 has only 1 completed reviews! University business rule mandates at least 3 completed reviews before a decision can be recorded.`
  - Upon recording an `ACCEPT` verdict, the paper state transitions to `'ACCEPTED'` and author camera-ready upload permissions are unlocked.

### 2.5 Module 5: Registration & Collision-Free Conference Timetabling (`/schedule`)
- **Capabilities:**
  - Audits author registration fee payment (\$650 regular author fee) via `Registrations`.
  - Chairs allocate accepted papers to conference sessions, dates, and halls (Hall A, Hall B, Hall C).
  - **Author Schedule Clash Prevention:** The engine validates that no co-author of the paper is scheduled in an overlapping time slot in another room on the same date:
    $$\text{Overlap Condition: } (T_{\text{start}}^{\text{new}} < T_{\text{end}}^{\text{exist}}) \land (T_{\text{end}}^{\text{new}} > T_{\text{start}}^{\text{exist}})$$
  - Prevents presenters from being scheduled simultaneously in two different halls.
  - Displays the chronological conference programme schedule via `vw_programme_schedule`.

---

## Deliverable 3: Live Analytical Reporting Dashboard (`/`)

The web dashboard queries the database views created in Review 2 to display live metrics:

| Report / View Name | SQL Object | Live Metrics Displayed in UI |
| :--- | :--- | :--- |
| **Track Statistics** | `vw_track_statistics` | Submissions, Accepts, Rejects, Under Review, Track Avg Score, Acceptance Rate % with visual progress bars. |
| **Reviewer Workload** | `vw_reviewer_workload` | Reviewer names, affiliations, assigned papers vs max workload, completed reviews, and remaining capacity badges. |
| **Urgent Pending Reviews** | `vw_pending_reviews` | Unsubmitted review assignments with paper titles, assigned reviewer names, emails, and due dates. |
| **Decisions Summary** | `vw_decisions_summary` | Official editorial verdicts, composite scores, chair rationale, and review counts. |
| **Programme Timetable** | `vw_programme_schedule` | Complete schedule ordered by date, room, and start time, with presenter and paper details. |

---

## Deliverable 4: Systematic Testing & Verification Suite (`test_suite.py`)

A formal automated test suite was developed using Python's `unittest` framework to verify data integrity and business rules:

```python
# test_suite.py Execution Results
Ran 5 tests in 0.024s
Status: OK (100% Pass Rate)
```

### Test Case Breakdown

| Test ID | Method Name | Verification Description | Result |
| :---: | :--- | :--- | :---: |
| **Test 1** | `test_01_paper_submission_and_versioning` | Verifies that Paper 1 has $\ge 2$ recorded versions and that a camera-ready copy is tagged without version loss. | **PASSED** |
| **Test 2** | `test_02_conflict_of_interest_detection` | Verifies that active COI records (`SAME_INSTITUTION` between Reviewer 1 and Author 1) are detected before assignment. | **PASSED** |
| **Test 3** | `test_03_mandatory_review_quota_threshold` | Verifies that Paper #6 has $< 3$ reviews and that no premature decision exists in `Decisions`. | **PASSED** |
| **Test 4** | `test_04_presentation_schedule_no_author_overlap` | Verifies that no scheduled author is double-booked across overlapping time slots in any room. | **PASSED** |
| **Test 5** | `test_05_score_domain_check_constraint` | Verifies that 100% of review ratings conform to integer bounds `BETWEEN 1 AND 10`. | **PASSED** |

---

## Deliverable 5: Live Demonstration & Execution Guide

### How to Run the Web Application
```bash
# 1. Navigate to project workspace
cd "c:\Users\harva\OneDrive\Documents\DMBS"

# 2. Run automated test suite
python test_suite.py

# 3. Launch Flask web application
python app.py
```
- Open any browser and navigate to: **`http://127.0.0.1:5000`**
- The application automatically connects to `conference_review2.db` with sample data.

### Live Demonstration Walkthrough Steps for Evaluators
1. **Show Dashboard (`/`):** Point out track acceptance rates, reviewer workloads, and pending reviews.
2. **Demonstrate Author Portal (`/author`):** Submit a new research paper titled *"Scalable Sharding in Proof-of-Stake"* in the Cloud track. Notice Version 1 is automatically created.
3. **Demonstrate Conflict of Interest Protection (`/chair`):**
   - Attempt to assign **Leslie Lamport** to **Paper #1** (Primary Author: Geoffrey Hinton).
   - Click *Verify COI & Assign Reviewer*.
   - **Result:** The system displays a red danger alert blocking the assignment due to the `SAME_INSTITUTION` conflict.
4. **Demonstrate Mandatory Review Quota Gating (`/chair`):**
   - Attempt to record an `ACCEPT` verdict for **Paper #6** (Autoscaling in Serverless Clouds).
   - Click *Record Decision*.
   - **Result:** The system blocks the verdict, explaining that Paper #6 has only 1 completed review and requires at least 3.
5. **Demonstrate Master Timetable (`/schedule`):**
   - Show the clash-free schedule with oral sessions in Hall A, Hall B, and Hall C.

---

## Deliverable 6: Complete 3-Review Project Retrospective

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PROJECT EVOLUTION RETROSPECTIVE                       │
├─────────────────────┬───────────────────┬───────────────────────────────────┤
│ Review Milestone    │ Scope & Focus     │ Key Achievements                  │
├─────────────────────┼───────────────────┼───────────────────────────────────┤
│ Review 1 (Week 7)   │ Conceptual Design │ • 14 Principal Entities           │
│                     │ & Normalization   │ • Relational Crow's Foot ERD      │
│                     │                   │ • Normalization up to 3NF         │
├─────────────────────┼───────────────────┼───────────────────────────────────┤
│ Review 2 (Week 10)  │ Physical Schema & │ • 17 Tables DDL with CHECK/FKs    │
│                     │ Advanced Queries  │ • 50+ Rows Realistic Test Data    │
│                     │                   │ • 7 Analytical Views              │
│                     │                   │ • B-Tree Indexing & Triggers      │
├─────────────────────┼───────────────────┼───────────────────────────────────┤
│ Review 3 (Week 14)  │ Front-End Web App │ • Python Flask Web Engine         │
│                     │ & End-to-End Demo │ • Author, Reviewer & Chair Portals│
│                     │                   │ • Automated COI & Quota Guards    │
│                     │                   │ • 5/5 Automated Unit Tests Passed │
└─────────────────────┴───────────────────┴───────────────────────────────────┘
```

---
*End of Review 3 Documentation.*
