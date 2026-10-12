# REVIEW 1 SPEAKER NOTES & VIVA PREPARATION
## 10-Slide Human Presentation Guide (5-Minute Script)

---

## Slide-by-Slide Script (Exactly What to Say)

### Slide 1: Title Slide (15 seconds)
> "Good morning, professors. Today I am presenting Review 1 of our DBMS project: **Academic Conference Paper Submission & Review System**. In this review, we cover our problem identification, scope, conceptual ER model with 14 principal entities, and our initial 3NF relational schema."

---

### Slide 2: Problem Statement (35 seconds)
> "Conferences today face four major problems when relying on emails and spreadsheets:
> 1. **Version Confusion:** Authors email updated PDFs, but reviewers end up evaluating older drafts.
> 2. **Conflict of Interest:** Reviewers are accidentally assigned papers written by friends or colleagues.
> 3. **Workload Imbalance:** Some reviewers receive 10 papers while others get none, leading to missed deadlines and papers with fewer than 3 reviews.
> 4. **Schedule Collisions:** Authors with multiple accepted papers get double-booked in two halls at the same time.
> Our relational database solves all four problems using database-level constraints."

---

### Slide 3: Project Scope & Objectives (25 seconds)
> "Our core objectives are:
> - Designing a normalized 3NF database to eliminate redundancy.
> - Supporting double-blind peer reviews with zero conflict bias.
> - Tracking multiple versions from initial draft to camera-ready PDF.
> - Enforcing conflict-free presentation timetables.
> We support five key user roles: Program Chair, Track Chairs, Authors, Reviewers, and Attendees."

---

### Slide 4: System Workflow (35 seconds)
> "Here is our 5-step conference workflow:
> - **Step 1 (Submission):** Author uploads paper metadata, co-authors, and a blinded PDF as Version 1.
> - **Step 2 (Reviewer Match):** Reviewers set topic expertise and declare conflicts. The system matches qualified reviewers without conflicts.
> - **Step 3 (Peer Review):** Enforces at least 3 reviews per paper on a 1-to-10 score scale.
> - **Step 4 (Decision):** Program Chair records the final Accept or Reject verdict, unlocking camera-ready uploads.
> - **Step 5 (Scheduling):** Accepted, paid papers are assigned halls and time slots without overlaps."

---

### Slide 5: Key Functional Requirements (30 seconds)
> "We broke down the system into six core modules:
> 1. **Paper Submission & Versions:** Auto-increment IDs, multi-author order, and discrete version files.
> 2. **Expertise & COI:** Competence mapping and automated conflict blocking.
> 3. **Assignment Engine:** Workload caps (max 5) and minimum 3 reviews per paper.
> 4. **Review Scoring:** 1 to 10 ratings for Originality, Soundness, and Clarity.
> 5. **Decisions:** Chair verdicts recorded with feedback logs.
> 6. **Presentation Slots:** Hall and time interval validation."

---

### Slide 6: The 14 Principal Entities (35 seconds)
> "As per the project guidelines, all 14 principal entities are modeled in four clean groups:
> 1. **Structure:** Conferences, Tracks, and Topics.
> 2. **Submission:** Authors, Papers, and Versions.
> 3. **Review Engine:** Reviewers, Expertise, Conflicts, Assignments, and Reviews.
> 4. **Scheduling:** Decisions, Registrations, and Presentation Slots.
> We also included `Users` as a central account entity and `Paper_Authors` as a bridge table."

---

### Slide 7: Conceptual ER Diagram (35 seconds)
> "This slide shows our ER architecture:
> - Conferences have multiple Tracks, and Tracks have multiple Topics ($1:N$).
> - Authors and Papers have a Many-to-Many relationship, resolved via `Paper_Authors`.
> - Papers link to `Paper_Versions` ($1:N$) so draft revisions never overwrite the original.
> - Reviewers evaluate Papers via `Paper_Assignments`, which has a strict $1:1$ link with `Reviews`.
> - Finally, accepted papers receive one Decision and one Presentation Slot."

---

### Slide 8: Relational Schema & Keys (35 seconds)
> "Here is our relational schema table:
> - Primary keys and foreign keys are explicitly defined for all tables.
> - Notice `Paper_Versions` enforces `UNIQUE(paper_id, version_num)`.
> - `Reviewer_Conflicts` has `UNIQUE(reviewer_id, author_id)` to prevent duplicate conflict entries.
> - `Reviews` uses a 1:1 `UNIQUE(assignment_id)` and domain `CHECK` constraints ensuring scores stay between 1 and 10.
> - `Presentation_Slots` checks that slot end times are strictly after start times."

---

### Slide 9: Normalization & Business Rules (35 seconds)
> "Our schema strictly adheres to Third Normal Form (3NF):
> - **1NF:** Multi-authors and file versions are stored as atomic rows, not comma-separated lists.
> - **2NF:** In composite keys like `Paper_Authors(paper_id, author_id)`, author order depends on both keys, with author bios stored separately in `Authors`.
> - **3NF:** Transitive dependencies are removed—track names belong in `Tracks`, not `Papers`.
> On the right are our 5 core business rules: unique IDs, automated COI barring, minimum 3 reviews, 1–10 scores, and non-overlapping presentation slots."

---

### Slide 10: Conclusion & Discussion (15 seconds)
> "In summary, all Review 1 deliverables—problem identification, scope, the 14-entity ER model, and the 3NF schema—are completed and validated with sample SQL data. Thank you, and I am happy to answer any questions."

---

## Top 10 Quick Viva Q&As (2-Sentence Answers)

1. **Why have a separate `Paper_Versions` table?**  
   *"To preserve revision history without overwriting drafts, separate blinded review PDFs from camera-ready copies, and keep the `Papers` table in 3NF."*

2. **How does the database support Double-Blind review?**  
   *"Reviewers query assigned papers through a view that shows only the blinded PDF and abstract, completely excluding author identities from `Paper_Authors`."*

3. **Why do you have both a `Users` table and `Authors`/`Reviewers` tables?**  
   *"A person can be both an author and a reviewer. Storing shared account details in `Users` prevents duplicate data and update anomalies."*

4. **How do you prevent a reviewer from reviewing their collaborator's paper?**  
   *"We maintain a `Reviewer_Conflicts` table. A `BEFORE INSERT` trigger on assignments checks whether the reviewer has a declared conflict with any co-author of that paper."*

5. **How is 3NF satisfied in your schema?**  
   *"All non-key columns depend strictly on the primary key alone. For example, track details are kept in `Tracks` rather than duplicated inside `Papers`."*

6. **How do you enforce the minimum 3 reviews quota?**  
   *"A database trigger on `Decisions` counts completed reviews for that paper and blocks the chair from recording an acceptance verdict if fewer than 3 reviews exist."*

7. **How do you ensure authors don't have overlapping presentations?**  
   *"Each slot enforces `paper_id UNIQUE`, and an overlap trigger verifies that no co-author of the paper is scheduled in another hall at the same date and time."*

8. **What is the relationship between `Paper_Assignments` and `Reviews`?**  
   *"It is a $1:1$ relationship enforced via `UNIQUE(assignment_id)`. This keeps assignments and submitted evaluation scores cleanly decoupled."*

9. **What domain constraints did you use?**  
   *"Domain `CHECK` constraints on review scores ($1–10$), presentation times (`end_time > start_time`), and conference dates (`end_date >= start_date`)."*

10. **What is your deliverable for Review 2?**  
    *"In Review 2, we will execute the DDL in PostgreSQL/MySQL, populate 50+ rows of test data, and demonstrate complex queries, joins, and analytical views."*
