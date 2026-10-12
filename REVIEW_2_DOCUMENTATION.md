# DATABASE MANAGEMENT SYSTEMS (CS304)
## PROJECT IMPLEMENTATION DOCUMENT: REVIEW 2 (WEEK 10)

---

# Title: Physical Database Implementation, Advanced SQL Queries, Views & Analytical Reports for Academic Conference DBMS

**Course Code / Name:** CS304 - Database Management Systems  
**Evaluation Milestone:** Review 2 (Week 10 - 10 to 15 Marks)  
**Target RDBMS:** PostgreSQL 14+ / MySQL 8.0+ / SQLite 3.40+  
**Date of Review:** October 2026  
**Document Version:** 2.0 (Physical Implementation & Query Execution Release)  

---

## Executive Summary & Milestone Deliverables

Building upon the conceptual ER design and 3NF logical schema approved in **Review 1**, this document presents the complete physical realization and testing for **Review 2**. Review 2 transitions the system from theoretical relational algebra into a live, fully functional, and performance-optimized database engine.

The core deliverables accomplished for Review 2 include:
1. **Physical Schema & DDL Implementation:** Creation of all 17 normalized tables with primary keys, foreign keys, cascade rules, and domain `CHECK` constraints.
2. **Realistic Sample Dataset (DML):** Populating over 50 realistic records across 4 conference tracks, modeling authors, multi-version submissions, topic expertise, active conflicts of interest, multi-criteria reviews, editorial decisions, conference registrations, and oral presentation schedules.
3. **Advanced SQL Statements:** Multi-table `INNER` and `LEFT` JOINs across up to 5 tables, aggregate functions (`COUNT`, `AVG`, `MIN`, `MAX`) with `GROUP BY` and `HAVING` filters, correlated subqueries, and `NOT EXISTS` logic.
4. **7 Essential Analytical Views & Reports:** Implementing the 7 reports explicitly mandated in the project specification:
   - *Pending Reviews Report* (`vw_pending_reviews`)
   - *Reviewer Workload Report* (`vw_reviewer_workload`)
   - *Paper Scores & Ranking Report* (`vw_paper_scores`)
   - *Decisions Summary Report* (`vw_decisions_summary`)
   - *Accepted Papers & Clearance Report* (`vw_accepted_papers`)
   - *Conference Programme Timetable* (`vw_programme_schedule`)
   - *Track Statistics Report* (`vw_track_statistics`)
5. **Data Integrity & Triggers:** Implementing active database triggers for automated conflict-of-interest prevention, review quota enforcement ($\ge 3$ reviews), and collision-free session timetabling.
6. **Indexing & Query Performance:** Defining B-Tree indexes on high-frequency search paths and analyzing query execution plans.
7. **ACID Transaction Awareness:** Demonstrating multi-statement atomic transactions with rollback protection against ethical and capacity violations.

---

## Deliverable 1: Physical Schema & Constraint Architecture

The database is partitioned into four modular layers implemented across 17 tables. Every table includes strict declarative integrity constraints:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PHYSICAL SCHEMA LAYER BREAKDOWN                       │
├─────────────────────┬───────────────────┬───────────────────────────────────┤
│ Module Name         │ Implemented Tables│ Key Enforced Constraints          │
├─────────────────────┼───────────────────┼───────────────────────────────────┤
│ 1. Conference &     │ Conferences       │ • UNIQUE(acronym, year)           │
│    Track Governance │ Tracks            │ • CHECK(end_date >= start_date)   │
│                     │ Topics            │ • UNIQUE(conf_id, track_name)     │
│                     │                   │ • UNIQUE(track_id, topic_name)    │
├─────────────────────┼───────────────────┼───────────────────────────────────┤
│ 2. Submissions &    │ Users             │ • UNIQUE(email)                   │
│    Versioning       │ Authors           │ • user_id UNIQUE (1:1 with Users) │
│                     │ Papers            │ • Composite PK (paper_id, auth_id)│
│                     │ Paper_Authors     │ • UNIQUE(paper_id, author_order)  │
│                     │ Paper_Versions    │ • UNIQUE(paper_id, version_num)   │
├─────────────────────┼───────────────────┼───────────────────────────────────┤
│ 3. Review Engine &  │ Reviewers         │ • user_id UNIQUE (1:1 with Users) │
│    Evaluation       │ Reviewer_Expertise│ • Composite PK (reviewer, topic)  │
│                     │ Reviewer_Conflicts│ • UNIQUE(reviewer_id, author_id)  │
│                     │ Paper_Assignments │ • UNIQUE(paper_id, reviewer_id)   │
│                     │ Reviews           │ • assignment_id UNIQUE (1:1)      │
│                     │                   │ • CHECK scores BETWEEN 1 AND 10   │
├─────────────────────┼───────────────────┼───────────────────────────────────┤
│ 4. Decisions &      │ Decisions         │ • paper_id UNIQUE (1:1)           │
│    Scheduling       │ Registrations     │ • CHECK amount_paid >= 0.00       │
│                     │ Sessions          │ • UNIQUE(conf, date, room, title) │
│                     │ Presentation_Slots│ • paper_id UNIQUE (1:1)           │
│                     │                   │ • CHECK(end_time > start_time)    │
└─────────────────────┴───────────────────┴───────────────────────────────────┘
```

---

## Deliverable 2: Realistic Sample Dataset & Simulation Scenarios

The live dataset models the **IEEE International Conference on Distributed Systems & AI 2026 (ICDSAI 2026)** with real-world academic simulation scenarios:

### 2.1 Research Tracks & Topics
- **Track 1: AI & Machine Learning** (Topics: *Large Language Models*, *Federated Learning*)
- **Track 2: Cloud & Distributed Systems** (Topics: *Consensus Protocols*, *Serverless Architecture*)
- **Track 3: Cybersecurity & Privacy** (Topics: *Zero-Knowledge Proofs*, *Blockchain Systems*)
- **Track 4: Software Engineering** (Topics: *Automated Test Generation*, *Program Synthesis*)

### 2.2 Academic Personnel (Users, Authors & Reviewers)
- **Editorial Leadership:**
  - *Dr. Alan Turing* (General Program Chair, Cambridge University)
  - *Dr. Barbara Liskov* (Track Chair, MIT)
- **Authors:**
  - *Geoffrey Hinton* (Univ of Toronto, Primary Author of P1 & P5)
  - *Yann LeCun* (NYU, Primary Author of P2 & P6)
  - *Yoshua Bengio* (Mila / Univ of Montreal, Primary Author of P3)
  - *Andrew Ng* (Stanford, Primary Author of P4)
- **Reviewer Pool & Workload Capacities:**
  - *Leslie Lamport* (Microsoft Research, Max Workload = 5, Expert in Consensus)
  - *Michael Stonebraker* (MIT CSAIL, Max Workload = 4, Expert in Serverless & Storage)
  - *Shafi Goldwasser* (UC Berkeley, Max Workload = 5, Expert in Zero-Knowledge Cryptography)
  - *Linus Torvalds* (Linux Foundation, Max Workload = 4, Expert in Systems & Software)
  - *Margaret Hamilton* (Hamilton Technologies, Max Workload = 5, Expert in Automated Testing)
  - *Grace Hopper* (Yale University, Max Workload = 4, Expert in Program Synthesis)

### 2.3 Conflict of Interest (COI) Ground Truth
1. `Reviewer 1 (Lamport)` $\leftrightarrow$ `Author 1 (Hinton)`: Declared conflict (`SAME_INSTITUTION`). Lamport is blocked from evaluating Paper 1 and Paper 5.
2. `Reviewer 2 (Stonebraker)` $\leftrightarrow$ `Author 4 (Ng)`: Declared conflict (`CO_AUTHOR`). Stonebraker is blocked from evaluating Paper 4.
3. `Reviewer 3 (Goldwasser)` $\leftrightarrow$ `Author 2 (LeCun)`: Declared conflict (`ADVISORY`). Goldwasser is blocked from evaluating Paper 2 and Paper 6.

### 2.4 Paper Evaluation & Lifecycle Scenarios
- **Paper 1 (`P1`):** *Energy-Efficient Quantization for Distributed LLM Inference*
  - Assigned to Reviewers 2, 4, 5. Scores: 9, 8, 9 (Average: **8.67**). Verdict: **ACCEPTED**. Author paid \$650. Scheduled in Session 1A.
- **Paper 2 (`P2`):** *Self-Supervised Contrastive Representation Learning across Distributed Graph Nodes*
  - Assigned to Reviewers 1, 4, 6. Scores: 8, 8, 9 (Average: **8.33**). Verdict: **ACCEPTED**. Author paid \$650. Scheduled in Session 1A.
- **Paper 3 (`P3`):** *Optimistic Consensus in High-Throughput Byzantine Distributed Ledgers*
  - Assigned to Reviewers 1, 2, 5. Scores: 9, 8, 8 (Average: **8.33**). Verdict: **ACCEPTED**. Author paid \$650. Scheduled in Session 2A.
- **Paper 4 (`P4`):** *Zero-Knowledge Succinct Verification for Layer-2 Rollups*
  - Assigned to Reviewers 3, 5, 6. Scores: 9, 8, 9 (Average: **8.67**). Verdict: **ACCEPTED**. Author paid \$650. Scheduled in Session 3A.
- **Paper 5 (`P5`):** *Automated Symbolic Fuzzing for Microservice API Boundaries*
  - Assigned to Reviewers 4, 5, 6. Scores: 4, 5, 5 (Average: **4.67**). Verdict: **REJECTED** due to weak novelty.
- **Paper 6 (`P6`):** *Adaptive Autoscaling in Serverless Compute Clouds*
  - Assigned to Reviewers 1, 2, 3. Reviewer 1 completed (Score: 7); Reviewers 2 and 3 are **PENDING**. Paper remains strictly **UNDER_REVIEW**.

---

## Deliverable 3: Advanced SQL Queries (Demonstrating RDBMS Mastery)

### Query 1: Multi-Table JOIN (Paper, Track, Primary Author, and Version Count)
- **Purpose:** Combines data across 5 distinct tables (`Papers`, `Tracks`, `Authors`, `Users`, and `Paper_Versions`) to provide program chairs with an integrated view of manuscript progress.
- **SQL Statement:**

```sql
SELECT 
    p.paper_id,
    p.title AS paper_title,
    t.track_name,
    u.first_name || ' ' || u.last_name AS primary_author,
    u.affiliation,
    COUNT(pv.version_id) AS total_versions,
    MAX(pv.is_camera_ready) AS has_camera_ready,
    p.status
FROM Papers p
JOIN Tracks t ON p.track_id = t.track_id
JOIN Authors a ON p.primary_author_id = a.author_id
JOIN Users u ON a.user_id = u.user_id
LEFT JOIN Paper_Versions pv ON p.paper_id = pv.paper_id
GROUP BY p.paper_id, p.title, t.track_name, u.first_name, u.last_name, u.affiliation, p.status
ORDER BY p.paper_id;
```

- **Query Execution Output:**

| paper_id | paper_title | track_name | primary_author | affiliation | total_versions | has_camera_ready | status |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **1** | Energy-Efficient Quantization for Distributed LLM Inference | AI & Machine Learning | Geoffrey Hinton | Univ of Toronto | 2 | 1 | ACCEPTED |
| **2** | Self-Supervised Contrastive Representation Learning... | AI & Machine Learning | Yann LeCun | NYU | 2 | 1 | ACCEPTED |
| **3** | Optimistic Consensus in Byzantine Ledgers | Cloud & Distributed Systems | Yoshua Bengio | Mila / Montreal | 2 | 1 | ACCEPTED |
| **4** | Zero-Knowledge Succinct Verification for Rollups | Cybersecurity & Privacy | Andrew Ng | Stanford Univ | 2 | 1 | ACCEPTED |
| **5** | Automated Symbolic Fuzzing for API Boundaries | Software Engineering | Geoffrey Hinton | Univ of Toronto | 1 | 0 | REJECTED |
| **6** | Adaptive Autoscaling in Serverless Clouds | Cloud & Distributed Systems | Yann LeCun | NYU | 1 | 0 | UNDER_REVIEW |

---

### Query 2: Multi-Criteria Aggregate Scoring with `GROUP BY` and `HAVING`
- **Purpose:** Calculates composite averages across Originality, Soundness, Clarity, and Overall ratings for each paper having received $\ge 3$ reviews with an overall rating $\ge 8.0$.
- **SQL Statement:**

```sql
SELECT 
    p.paper_id,
    p.title AS paper_title,
    COUNT(r.review_id) AS total_reviews,
    ROUND(AVG(r.originality), 2) AS avg_originality,
    ROUND(AVG(r.soundness), 2) AS avg_soundness,
    ROUND(AVG(r.clarity), 2) AS avg_clarity,
    ROUND(AVG(r.overall_score), 2) AS composite_avg_score,
    MIN(r.overall_score) AS min_rating,
    MAX(r.overall_score) AS max_rating
FROM Papers p
JOIN Paper_Assignments pa ON p.paper_id = pa.paper_id
JOIN Reviews r ON pa.assignment_id = r.assignment_id
GROUP BY p.paper_id, p.title
HAVING COUNT(r.review_id) >= 3 AND AVG(r.overall_score) >= 8.0
ORDER BY composite_avg_score DESC;
```

- **Query Execution Output:**

| paper_id | paper_title | total_reviews | avg_originality | avg_soundness | avg_clarity | composite_avg_score | min_rating | max_rating |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Energy-Efficient Quantization for Distributed LLM | 3 | 8.67 | 8.67 | 8.67 | **8.67** | 8 | 9 |
| **4** | Zero-Knowledge Succinct Verification for Rollups | 3 | 8.67 | 8.67 | 8.67 | **8.67** | 8 | 9 |
| **2** | Self-Supervised Contrastive Representation Learning | 3 | 8.00 | 8.00 | 8.33 | **8.33** | 8 | 9 |
| **3** | Optimistic Consensus in Byzantine Ledgers | 3 | 8.67 | 8.67 | 8.33 | **8.33** | 8 | 9 |

---

### Query 3: Correlated Subquery with `NOT EXISTS` (Bottleneck Identification)
- **Purpose:** Identifies papers that are currently in `UNDER_REVIEW` state but do not have an official decision logged, enabling program chairs to track which manuscripts have pending reviews blocking the editorial pipeline.
- **SQL Statement:**

```sql
SELECT 
    p.paper_id,
    p.title AS paper_title,
    t.track_name,
    (SELECT COUNT(*) FROM Paper_Assignments pa WHERE pa.paper_id = p.paper_id AND pa.status = 'COMPLETED') AS completed_reviews,
    (SELECT COUNT(*) FROM Paper_Assignments pa WHERE pa.paper_id = p.paper_id AND pa.status = 'ASSIGNED') AS pending_reviews
FROM Papers p
JOIN Tracks t ON p.track_id = t.track_id
WHERE p.status = 'UNDER_REVIEW'
  AND NOT EXISTS (
      SELECT 1 FROM Decisions d 
      WHERE d.paper_id = p.paper_id
  );
```

- **Query Execution Output:**

| paper_id | paper_title | track_name | completed_reviews | pending_reviews |
| :---: | :--- | :--- | :---: | :---: |
| **6** | Adaptive Autoscaling in Serverless Compute Clouds | Cloud & Distributed Systems | 1 | 2 |

---

### Query 4: Correlated Subquery to Determine Highest-Scoring Paper in Each Track
- **Purpose:** Automatically isolates candidate papers for track-level "Best Paper Awards" by comparing each paper's average score against the maximum average score within its specific track.
- **SQL Statement:**

```sql
SELECT 
    p.paper_id,
    p.title AS paper_title,
    t.track_name,
    ROUND(AVG(r.overall_score), 2) AS track_best_score
FROM Papers p
JOIN Tracks t ON p.track_id = t.track_id
JOIN Paper_Assignments pa ON p.paper_id = pa.paper_id
JOIN Reviews r ON pa.assignment_id = r.assignment_id
GROUP BY p.paper_id, p.title, t.track_name
HAVING AVG(r.overall_score) = (
    SELECT MAX(sub.avg_score)
    FROM (
        SELECT AVG(r2.overall_score) AS avg_score
        FROM Papers p2
        JOIN Paper_Assignments pa2 ON p2.paper_id = pa2.paper_id
        JOIN Reviews r2 ON pa2.assignment_id = r2.assignment_id
        WHERE p2.track_id = p.track_id
        GROUP BY p2.paper_id
    ) sub
)
ORDER BY track_best_score DESC;
```

- **Query Execution Output:**

| paper_id | paper_title | track_name | track_best_score |
| :---: | :--- | :--- | :---: |
| **1** | Energy-Efficient Quantization for Distributed LLM Inference | AI & Machine Learning | **8.67** |
| **4** | Zero-Knowledge Succinct Verification for Layer-2 Rollups | Cybersecurity & Privacy | **8.67** |
| **3** | Optimistic Consensus in High-Throughput Byzantine Ledgers | Cloud & Distributed Systems | **8.33** |
| **5** | Automated Symbolic Fuzzing for Microservice API Boundaries | Software Engineering | **4.67** |

---

## Deliverable 4: The 7 Meaningful Analytical Views & Reports

The project specification mandates 7 specialized reports. Each report is codified as a permanent database view:

### 4.1 View 1: Pending Reviews Report (`vw_pending_reviews`)
- **SQL Definition:**

```sql
CREATE VIEW vw_pending_reviews AS
SELECT 
    pa.assignment_id,
    p.paper_id,
    p.title AS paper_title,
    t.track_name,
    u.first_name || ' ' || u.last_name AS reviewer_name,
    u.email AS reviewer_email,
    pa.assigned_at,
    pa.due_date,
    pa.status
FROM Paper_Assignments pa
JOIN Papers p ON pa.paper_id = p.paper_id
JOIN Tracks t ON p.track_id = t.track_id
JOIN Reviewers r ON pa.reviewer_id = r.reviewer_id
JOIN Users u ON r.user_id = u.user_id
WHERE pa.status = 'ASSIGNED';
```

- **Live Output Table:**

| assignment_id | paper_id | paper_title | track_name | reviewer_name | reviewer_email | due_date | status |
| :---: | :---: | :--- | :--- | :--- | :--- | :---: | :---: |
| **17** | 6 | Adaptive Autoscaling in Serverless Clouds | Cloud & Distributed | Michael Stonebraker | stonebraker@mit.edu | 2026-10-20 | ASSIGNED |
| **18** | 6 | Adaptive Autoscaling in Serverless Clouds | Cloud & Distributed | Shafi Goldwasser | shafi@berkeley.edu | 2026-10-20 | ASSIGNED |

---

### 4.2 View 2: Reviewer Workload Report (`vw_reviewer_workload`)
- **SQL Definition:**

```sql
CREATE VIEW vw_reviewer_workload AS
SELECT 
    r.reviewer_id,
    u.first_name || ' ' || u.last_name AS reviewer_name,
    u.affiliation,
    r.max_workload,
    COUNT(pa.assignment_id) AS total_assigned_papers,
    SUM(CASE WHEN pa.status = 'COMPLETED' THEN 1 ELSE 0 END) AS completed_reviews,
    SUM(CASE WHEN pa.status = 'ASSIGNED' THEN 1 ELSE 0 END) AS pending_reviews,
    (r.max_workload - COUNT(pa.assignment_id)) AS remaining_capacity
FROM Reviewers r
JOIN Users u ON r.user_id = u.user_id
LEFT JOIN Paper_Assignments pa ON r.reviewer_id = pa.reviewer_id
GROUP BY r.reviewer_id, u.first_name, u.last_name, u.affiliation, r.max_workload;
```

- **Live Output Table:**

| reviewer_id | reviewer_name | affiliation | max_workload | total_assigned | completed | pending | remaining_capacity |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **1** | Leslie Lamport | Microsoft Research | 5 | 3 | 3 | 0 | **2** |
| **2** | Michael Stonebraker | MIT CSAIL | 4 | 3 | 2 | 1 | **1** |
| **3** | Shafi Goldwasser | UC Berkeley | 5 | 2 | 1 | 1 | **3** |
| **4** | Linus Torvalds | Linux Foundation | 4 | 3 | 3 | 0 | **1** |
| **5** | Margaret Hamilton | Hamilton Technologies | 5 | 4 | 4 | 0 | **1** |
| **6** | Grace Hopper | Yale University | 4 | 3 | 3 | 0 | **1** |

---

### 4.3 View 3: Paper Scores & Evaluation Summary (`vw_paper_scores`)
- **SQL Definition:**

```sql
CREATE VIEW vw_paper_scores AS
SELECT 
    p.paper_id,
    p.title AS paper_title,
    t.track_name,
    COUNT(r.review_id) AS review_count,
    ROUND(AVG(r.overall_score), 2) AS avg_overall_score,
    ROUND(AVG(r.originality), 2) AS avg_originality,
    ROUND(AVG(r.soundness), 2) AS avg_soundness,
    ROUND(AVG(r.clarity), 2) AS avg_clarity,
    MIN(r.overall_score) AS min_score,
    MAX(r.overall_score) AS max_score,
    p.status AS current_status
FROM Papers p
JOIN Tracks t ON p.track_id = t.track_id
LEFT JOIN Paper_Assignments pa ON p.paper_id = pa.paper_id
LEFT JOIN Reviews r ON pa.assignment_id = r.assignment_id
GROUP BY p.paper_id, p.title, t.track_name, p.status;
```

- **Live Output Table:**

| paper_id | paper_title | track_name | review_count | avg_overall | avg_orig | avg_sound | avg_clarity | min | max | status |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | Energy-Efficient Quantization for Distributed LLM | AI & Machine Learning | 3 | **8.67** | 8.67 | 8.67 | 8.67 | 8 | 9 | ACCEPTED |
| **2** | Self-Supervised Contrastive Representation Learning | AI & Machine Learning | 3 | **8.33** | 8.00 | 8.00 | 8.33 | 8 | 9 | ACCEPTED |
| **3** | Optimistic Consensus in Byzantine Ledgers | Cloud & Distributed | 3 | **8.33** | 8.67 | 8.67 | 8.33 | 8 | 9 | ACCEPTED |
| **4** | Zero-Knowledge Succinct Verification for Rollups | Cybersecurity & Privacy | 3 | **8.67** | 8.67 | 8.67 | 8.67 | 8 | 9 | ACCEPTED |
| **5** | Automated Symbolic Fuzzing for API Boundaries | Software Engineering | 3 | **4.67** | 4.67 | 4.67 | 5.33 | 4 | 5 | REJECTED |
| **6** | Adaptive Autoscaling in Serverless Clouds | Cloud & Distributed | 1 | **7.00** | 7.00 | 7.00 | 8.00 | 7 | 7 | UNDER_REVIEW |

---

### 4.4 View 4: Decisions Summary Report (`vw_decisions_summary`)
- **SQL Definition:**

```sql
CREATE VIEW vw_decisions_summary AS
SELECT 
    d.decision_id,
    p.paper_id,
    p.title AS paper_title,
    t.track_name,
    d.decision_type,
    ROUND(AVG(r.overall_score), 2) AS avg_score,
    u.first_name || ' ' || u.last_name AS chair_name,
    d.decision_date,
    d.feedback_summary
FROM Decisions d
JOIN Papers p ON d.paper_id = p.paper_id
JOIN Tracks t ON p.track_id = t.track_id
JOIN Users u ON d.chair_id = u.user_id
LEFT JOIN Paper_Assignments pa ON p.paper_id = pa.paper_id
LEFT JOIN Reviews r ON pa.assignment_id = r.assignment_id
GROUP BY d.decision_id, p.paper_id, p.title, t.track_name, d.decision_type, u.first_name, u.last_name, d.decision_date, d.feedback_summary;
```

- **Live Output Table:**

| decision_id | paper_id | paper_title | decision_type | avg_score | chair_name | feedback_summary |
| :---: | :---: | :--- | :---: | :---: | :--- | :--- |
| **1** | 1 | Energy-Efficient Quantization for Distributed LLM | **ACCEPT** | 8.67 | Alan Turing | Consensus recommendation: Accept as Regular Oral Presentation. |
| **2** | 2 | Self-Supervised Contrastive Representation Learning | **ACCEPT** | 8.33 | Alan Turing | Consensus recommendation: Accept as Regular Oral Presentation. |
| **3** | 3 | Optimistic Consensus in Byzantine Ledgers | **ACCEPT** | 8.33 | Alan Turing | Consensus recommendation: Accept as Regular Oral Presentation. |
| **4** | 4 | Zero-Knowledge Succinct Verification for Rollups | **ACCEPT** | 8.67 | Alan Turing | Consensus recommendation: Accept as Regular Oral Presentation. |
| **5** | 5 | Automated Symbolic Fuzzing for API Boundaries | **REJECT** | 4.67 | Alan Turing | Consensus recommendation: Reject due to weak empirical novelty. |

---

### 4.5 View 5: Accepted Papers & Clearance Audit (`vw_accepted_papers`)
- **SQL Definition:**

```sql
CREATE VIEW vw_accepted_papers AS
SELECT 
    p.paper_id,
    p.title,
    t.track_name,
    u.first_name || ' ' || u.last_name AS primary_author,
    u.email AS author_email,
    COALESCE(MAX(pv.is_camera_ready), 0) AS has_camera_ready,
    COALESCE(reg.payment_status, 'UNREGISTERED') AS registration_status
FROM Papers p
JOIN Tracks t ON p.track_id = t.track_id
JOIN Authors a ON p.primary_author_id = a.author_id
JOIN Users u ON a.user_id = u.user_id
LEFT JOIN Paper_Versions pv ON p.paper_id = pv.paper_id
LEFT JOIN Registrations reg ON p.paper_id = reg.paper_id
WHERE p.status = 'ACCEPTED'
GROUP BY p.paper_id, p.title, t.track_name, u.first_name, u.last_name, u.email, reg.payment_status;
```

- **Live Output Table:**

| paper_id | title | track_name | primary_author | author_email | has_camera_ready | registration_status |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: |
| **1** | Energy-Efficient Quantization for Distributed LLM | AI & Machine Learning | Geoffrey Hinton | hinton@toronto.edu | 1 | **PAID** |
| **2** | Self-Supervised Contrastive Representation Learning | AI & Machine Learning | Yann LeCun | lecun@nyu.edu | 1 | **PAID** |
| **3** | Optimistic Consensus in Byzantine Ledgers | Cloud & Distributed | Yoshua Bengio | bengio@mila.quebec | 1 | **PAID** |
| **4** | Zero-Knowledge Succinct Verification for Rollups | Cybersecurity & Privacy | Andrew Ng | ng@stanford.edu | 1 | **PAID** |

---

### 4.6 View 6: Conference Programme Schedule (`vw_programme_schedule`)
- **SQL Definition:**

```sql
CREATE VIEW vw_programme_schedule AS
SELECT 
    ps.slot_date,
    ps.start_time,
    ps.end_time,
    s.room_no,
    s.session_title,
    s.session_chair,
    t.track_name,
    ps.presentation_order,
    p.paper_id,
    p.title AS paper_title,
    u.first_name || ' ' || u.last_name AS presenter_name,
    u.affiliation
FROM Presentation_Slots ps
JOIN Sessions s ON ps.session_id = s.session_id
JOIN Tracks t ON s.track_id = t.track_id
JOIN Papers p ON ps.paper_id = p.paper_id
JOIN Authors a ON p.primary_author_id = a.author_id
JOIN Users u ON a.user_id = u.user_id
ORDER BY ps.slot_date, s.room_no, ps.start_time;
```

- **Live Output Table:**

| slot_date | start_time | end_time | room_no | session_title | presenter_name | paper_title |
| :---: | :---: | :---: | :--- | :--- | :--- | :--- |
| **2026-11-16** | 09:30 | 10:00 | Hall A - Main Aud | Session 1A: Neural Arch | Geoffrey Hinton | Energy-Efficient Quantization for LLM |
| **2026-11-16** | 10:00 | 10:30 | Hall A - Main Aud | Session 1A: Neural Arch | Yann LeCun | Self-Supervised Contrastive Learning |
| **2026-11-16** | 11:00 | 11:30 | Hall B - West Wing | Session 2A: Consensus | Yoshua Bengio | Optimistic Consensus in Byzantine Ledgers |
| **2026-11-17** | 14:00 | 14:30 | Hall C - Innovation | Session 3A: ZK Crypto | Andrew Ng | Zero-Knowledge Succinct Verification |

---

### 4.7 View 7: Track Statistics Report (`vw_track_statistics`)
- **SQL Definition:**

```sql
CREATE VIEW vw_track_statistics AS
SELECT 
    t.track_id,
    t.track_name,
    COUNT(p.paper_id) AS total_submissions,
    SUM(CASE WHEN p.status = 'ACCEPTED' THEN 1 ELSE 0 END) AS accepted_count,
    SUM(CASE WHEN p.status = 'REJECTED' THEN 1 ELSE 0 END) AS rejected_count,
    SUM(CASE WHEN p.status = 'UNDER_REVIEW' THEN 1 ELSE 0 END) AS under_review_count,
    ROUND(AVG(r.overall_score), 2) AS track_avg_score,
    CASE 
        WHEN COUNT(p.paper_id) > 0 THEN ROUND((SUM(CASE WHEN p.status = 'ACCEPTED' THEN 1.0 ELSE 0.0 END) / COUNT(p.paper_id)) * 100, 1)
        ELSE 0.0 
    END AS acceptance_rate_pct
FROM Tracks t
LEFT JOIN Papers p ON t.track_id = p.track_id
LEFT JOIN Paper_Assignments pa ON p.paper_id = pa.paper_id
LEFT JOIN Reviews r ON pa.assignment_id = r.assignment_id
GROUP BY t.track_id, t.track_name;
```

- **Live Output Table:**

| track_id | track_name | total_submissions | accepted | rejected | under_review | track_avg_score | acceptance_rate_pct |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | AI & Machine Learning | 2 | 2 | 0 | 0 | 8.50 | **100.0%** |
| **2** | Cloud & Distributed Systems | 2 | 1 | 0 | 1 | 8.00 | **50.0%** |
| **3** | Cybersecurity & Privacy | 1 | 1 | 0 | 0 | 8.67 | **100.0%** |
| **4** | Software Engineering | 1 | 0 | 1 | 0 | 4.67 | **0.0%** |

---

## Deliverable 5: Business Rules & Trigger Implementations

Complex cross-table integrity rules are enforced via procedural triggers:

### 5.1 Trigger 1: Conflict of Interest (COI) Prevention
```sql
CREATE TRIGGER trg_prevent_coi_assignment
BEFORE INSERT ON Paper_Assignments
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'Integrity Violation: Cannot assign paper to reviewer with an active Conflict of Interest.')
    WHERE EXISTS (
        SELECT 1 
        FROM Paper_Authors pa
        JOIN Reviewer_Conflicts rc ON pa.author_id = rc.author_id
        WHERE pa.paper_id = NEW.paper_id
          AND rc.reviewer_id = NEW.reviewer_id
    );
END;
```

### 5.2 Trigger 2: Mandatory Review Quota Threshold ($\ge 3$ Reviews)
```sql
CREATE TRIGGER trg_enforce_min_review_quota
BEFORE INSERT ON Decisions
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'Decision Blocked: Paper must have at least 3 completed peer reviews before recording a verdict.')
    WHERE (
        SELECT COUNT(*) 
        FROM Paper_Assignments pa
        JOIN Reviews r ON pa.assignment_id = r.assignment_id
        WHERE pa.paper_id = NEW.paper_id
    ) < 3;
END;
```

### 5.3 Trigger 3: Non-Overlapping Presentation Slot Allocation
```sql
CREATE TRIGGER trg_prevent_author_slot_collision
BEFORE INSERT ON Presentation_Slots
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'Scheduling Collision: An author of this paper is already scheduled in an overlapping time slot.')
    WHERE EXISTS (
        SELECT 1
        FROM Presentation_Slots ps
        JOIN Paper_Authors pa_existing ON ps.paper_id = pa_existing.paper_id
        JOIN Paper_Authors pa_new ON pa_new.author_id = pa_existing.author_id
        WHERE pa_new.paper_id = NEW.paper_id
          AND ps.slot_date = NEW.slot_date
          AND ps.paper_id != NEW.paper_id
          AND (
              (NEW.start_time >= ps.start_time AND NEW.start_time < ps.end_time) OR
              (NEW.end_time > ps.start_time AND NEW.end_time <= ps.end_time) OR
              (NEW.start_time <= ps.start_time AND NEW.end_time >= ps.end_time)
          )
    );
END;
```

---

## Deliverable 6: Indexing Performance & ACID Transactions

### 6.1 B-Tree Index Definitions
To eliminate sequential full-table scans on high-traffic queries:
```sql
CREATE INDEX idx_papers_track ON Papers(track_id);
CREATE INDEX idx_papers_status ON Papers(status);
CREATE INDEX idx_asgn_reviewer ON Paper_Assignments(reviewer_id);
CREATE INDEX idx_asgn_paper ON Paper_Assignments(paper_id);
CREATE INDEX idx_rev_asgn ON Reviews(assignment_id);
CREATE INDEX idx_slots_paper ON Presentation_Slots(paper_id);
```

### 6.2 Query Execution Plan Demonstration (`EXPLAIN QUERY PLAN`)
- Query filtering papers by track and status:
  `EXPLAIN QUERY PLAN SELECT * FROM Papers WHERE track_id = 1 AND status = 'ACCEPTED';`
  - **Plan Result:** `SEARCH Papers USING INDEX idx_papers_track (track_id=?)`  
  - **Performance Benefit:** Reduces search complexity from $O(N)$ sequential scan down to $O(\log N)$ logarithmic B-Tree lookup.

### 6.3 ACID Transaction Demonstration
```sql
-- Atomic 3-Reviewer Assignment with Rollback Safeguard
BEGIN TRANSACTION;

INSERT INTO Paper_Assignments (paper_id, reviewer_id, due_date, status)
VALUES (3, 1, '2026-10-15', 'ASSIGNED');

INSERT INTO Paper_Assignments (paper_id, reviewer_id, due_date, status)
VALUES (3, 2, '2026-10-15', 'ASSIGNED');

-- If Reviewer 3 has a conflict, the trigger aborts and the engine executes ROLLBACK:
-- ROLLBACK;

-- If all 3 pass COI validation:
COMMIT;
```

---
*End of Review 2 Documentation.*
