# REVIEW 2 SPEAKER NOTES & VIVA / EXAMINER PREPARATION GUIDE
## Physical Implementation, Advanced SQL, Views & Reports (5-Minute Script)

---

## Part 1: Slide-by-Slide Presentation Script (25–35 Seconds per Slide)

### Slide 1: Title Slide (15 seconds)
> **What to Say:**  
> "Good morning, respected professors and evaluators. Today we present **Review 2** of our DBMS project: the **Academic Conference Paper Submission and Review System**. In this review, we demonstrate our physical database implementation, live sample dataset, advanced multi-table SQL queries, and the 7 analytical reporting views required by the university specification."

---

### Slide 2: Review 2 Objectives (30 seconds)
> **What to Say:**  
> "Review 2 transitions our design from relational theory into a live, executing database engine:
> 1. We executed physical DDL for all 17 normalized tables with multi-tier integrity constraints.
> 2. We populated over 50 realistic rows simulating 4 tracks, multi-version submissions, and active COIs.
> 3. We prepared advanced queries featuring multi-table joins, aggregations, and correlated subqueries.
> 4. We implemented all 7 analytical views for workloads, pending reviews, scores, decisions, and scheduling."

---

### Slide 3: Physical DDL & Constraints (35 seconds)
> **What to Say:**  
> "Our physical implementation spans 17 tables organized into four modules: Conference Structure, Submissions, Review Engine, and Scheduling.  
> We enforce multi-tiered integrity:
> - Primary and Foreign Keys with appropriate cascade policies (`CASCADE` on versions, `RESTRICT` on formal decisions).
> - Domain `CHECK` constraints enforcing 1-to-10 integer scores and valid time durations.
> - Candidate `UNIQUE` constraints preventing duplicate review assignments and ensuring 1:1 decisions."

---

### Slide 4: Realistic Sample Dataset (35 seconds)
> **What to Say:**  
> "We populated realistic test data simulating the IEEE ICDSAI 2026 conference:
> - 4 research tracks and 6 multi-author papers with initial drafts and camera-ready copies.
> - 6 active reviewers with capped workloads and declared conflicts of interest.
> - Live evaluation data demonstrates multiple real-world scenarios: high-scoring papers accepted with average scores above 8.3, a low-scoring paper rejected at 4.67, and an active paper currently under review."

---

### Slide 5: Advanced SQL: Multi-Table JOINs & Aggregates (35 seconds)
> **What to Say:**  
> "On this slide, we demonstrate two advanced SQL queries:
> - **Query 1** executes a 4-table join connecting Papers, Tracks, Primary Authors, Users, and Paper Versions to audit manuscript drafts in a single view.
> - **Query 2** aggregates multi-criteria ratings using `GROUP BY` and a `HAVING` clause requiring `COUNT >= 3` and `AVG(score) >= 8.0`, immediately isolating papers qualified for acceptance."

---

### Slide 6: Advanced SQL: Subqueries & Complex Logic (35 seconds)
> **What to Say:**  
> "Here we demonstrate nested subquery logic:
> - **Query 3** uses a correlated subquery with `NOT EXISTS` to pinpoint bottleneck manuscripts that are under review without a final decision, preventing premature deliberations.
> - **Query 4** uses a scalar subquery to find the highest-scoring paper within each track, automating candidate selection for track-level 'Best Paper Awards'."

---

### Slide 7: Views & Reports: Review Monitoring (35 seconds)
> **What to Say:**  
> "This slide highlights our first 3 analytical views:
> - **View 1 (`vw_pending_reviews`):** Filters unsubmitted assignments, showing paper titles, reviewer names, and deadlines.
> - **View 2 (`vw_reviewer_workload`):** Aggregates assigned papers, completed reviews, and remaining workload capacity.
> - **View 3 (`vw_paper_scores`):** Computes multi-criteria averages, minimums, maximums, and score spreads across originality, soundness, and clarity."

---

### Slide 8: Views & Reports: Decisions & Schedule (35 seconds)
> **What to Say:**  
> "Our remaining 4 views cover the final conference stages:
> - **View 4 (`vw_decisions_summary`):** Logs chair verdicts with aggregated scores and feedback summaries.
> - **View 5 (`vw_accepted_papers`):** Audits camera-ready PDF uploads and author registration payment clearance.
> - **View 6 (`vw_programme_schedule`):** Generates the master conference timetable joining sessions, rooms, slots, papers, and presenters.
> - **View 7 (`vw_track_statistics`):** Computes track-level acceptance rates and submission volumes."

---

### Slide 9: Business Rules & Triggers (30 seconds)
> **What to Say:**  
> "We implemented three active database triggers:
> 1. **COI Prevention Trigger:** Aborts paper assignments if the reviewer has a declared conflict with any author.
> 2. **Review Quota Trigger:** Blocks chair decisions if fewer than 3 completed reviews exist.
> 3. **Presentation Overlap Trigger:** Prevents an author or room from being double-booked into simultaneous time slots."

---

### Slide 10: Indexing & ACID Transactions (30 seconds)
> **What to Say:**  
> "To guarantee production performance:
> - We created B-Tree indexes on `track_id`, `paper_id`, `reviewer_id`, and `status`, reducing search complexity from $O(N)$ full table scans down to $O(\log N)$ index lookups.
> - We demonstrated ACID transactions where assigning multiple reviewers executes atomically; if any reviewer triggers a conflict, the entire transaction rolls back to preserve data consistency."

---

### Slide 11: Summary & Next Steps (15 seconds)
> **What to Say:**  
> "In summary, all Review 2 deliverables—physical DDL, realistic dataset, advanced queries, 7 analytical views, indexing, and triggers—are 100% completed and verified. In Review 3, we will integrate our front-end web interface for end-to-end demonstrations. Thank you, and we look forward to your questions!"

---

## Part 2: Top 15 Review 2 Viva Questions & Model Answers

### 1. What is the difference between `WHERE` and `HAVING` in your SQL queries?
> **Model Answer:**  
> "`WHERE` filters individual rows *before* any grouping or aggregation takes place (e.g., filtering `pa.status = 'COMPLETED'`). `HAVING` filters aggregated groups *after* the `GROUP BY` clause has been computed (e.g., filtering `HAVING AVG(r.overall_score) >= 8.0` and `COUNT(r.review_id) >= 3`)."

### 2. How does your `NOT EXISTS` query help the Program Chair?
> **Model Answer:**  
> "It identifies papers currently marked as `UNDER_REVIEW` where no corresponding record exists in the `Decisions` table. This allows the chair to immediately find bottleneck papers that are waiting on pending reviews, preventing them from making incomplete or biased editorial decisions."

### 3. Why did you use `LEFT JOIN` instead of `INNER JOIN` in `vw_reviewer_workload`?
> **Model Answer:**  
> "If we used an `INNER JOIN` between `Reviewers` and `Paper_Assignments`, reviewers who have not yet been assigned any papers would be completely omitted from the report. A `LEFT JOIN` guarantees that every active reviewer appears in the report with a total assigned count of 0 and full remaining capacity."

### 4. Explain how your Conflict of Interest (COI) trigger works.
> **Model Answer:**  
> "It is a `BEFORE INSERT` trigger on `Paper_Assignments`. When a chair attempts to assign a reviewer to a paper, the trigger queries `Reviewer_Conflicts` joined with `Paper_Authors` for that paper. If an active conflict record exists between that reviewer and *any* co-author of the paper, the trigger raises a SQL exception and rolls back the insertion."

### 5. Why did you create indexes on `track_id` and `reviewer_id`?
> **Model Answer:**  
> "In relational databases, foreign keys and filtering columns without indexes require $O(N)$ sequential table scans. By building B-Tree indexes on `Papers(track_id)` and `Paper_Assignments(reviewer_id)`, the database performs $O(\log N)$ index lookups, accelerating join operations and dashboard views by orders of magnitude."

### 6. What does `EXPLAIN QUERY PLAN` show for your indexed queries?
> **Model Answer:**  
> "It demonstrates that the query optimizer chooses `SEARCH TABLE Papers USING INDEX idx_papers_track` instead of `SCAN TABLE Papers`. This proves that the query engine uses our B-Tree index rather than scanning every row in the table."

### 7. How do you calculate the acceptance rate percentage in `vw_track_statistics`?
> **Model Answer:**  
> "We use a conditional aggregation expression:  
> `ROUND((SUM(CASE WHEN status = 'ACCEPTED' THEN 1.0 ELSE 0.0 END) / COUNT(paper_id)) * 100, 1)`.  
> Multiplying by `1.0` avoids integer division truncation, yielding an exact percentage like 50.0% or 100.0%."

### 8. How does your database enforce that an accepted paper must have at least 3 reviews before decision?
> **Model Answer:**  
> "Via our `BEFORE INSERT` trigger on `Decisions`. Before the chair's verdict can be inserted, the trigger counts submitted reviews for that paper in `Reviews` linked through `Paper_Assignments`. If the count is $< 3$, the trigger aborts the operation."

### 9. How do you prevent presentation slot time collisions?
> **Model Answer:**  
> "First, `paper_id` is defined as `UNIQUE` in `Presentation_Slots`, so a paper cannot be scheduled twice. Second, a trigger checks whether any co-author of that paper is already scheduled in an overlapping time interval ($[\text{start}_1, \text{end}_1] \cap [\text{start}_2, \text{end}_2] \neq \emptyset$) on that date in any room."

### 10. How does ACID transaction awareness apply to reviewer assignment?
> **Model Answer:**  
> "Assigning 3 reviewers to a paper must be atomic. By wrapping the three `INSERT` statements inside `BEGIN TRANSACTION...COMMIT`, if the third assignment violates a COI rule or exceeds reviewer workload, the entire transaction rolls back via `ROLLBACK`, leaving the database in a clean, consistent state."

### 11. How do you separate constructive author feedback from confidential chair remarks?
> **Model Answer:**  
> "In the `Reviews` table, we store two distinct text columns: `comments_for_author` and `confidential_chair_comments`. When authors view their feedback, the application queries a view that strictly selects `comments_for_author` and hides the confidential remarks."

### 12. Why did you use `COALESCE` in `vw_accepted_papers`?
> **Model Answer:**  
> "`COALESCE(reg.payment_status, 'UNREGISTERED')` handles papers that have not yet registered. If an accepted paper has no corresponding row in `Registrations`, a `LEFT JOIN` produces `NULL`. `COALESCE` replaces that `NULL` with the human-readable string `'UNREGISTERED'`."

### 13. What is the difference between 2NF and 3NF as verified on your live data?
> **Model Answer:**  
> "2NF requires that in composite-key tables like `Paper_Authors(paper_id, author_id)`, attributes like `author_order` depend on both keys. 3NF requires that no non-key attribute depends transitively on another non-key attribute. In our data, track names are stored only in `Tracks`, preventing update anomalies when track metadata changes."

### 14. What are the 7 views implemented in your database?
> **Model Answer:**  
> "The 7 views are:  
> 1. `vw_pending_reviews`  
> 2. `vw_reviewer_workload`  
> 3. `vw_paper_scores`  
> 4. `vw_decisions_summary`  
> 5. `vw_accepted_papers`  
> 6. `vw_programme_schedule`  
> 7. `vw_track_statistics`."

### 15. What will you deliver in Review 3?
> **Model Answer:**  
> "In Review 3 (Final Review - 15 Marks), we will deliver a front-end web application (Python Flask / Java Spring Boot) connecting to this database, providing role-based user interfaces for Authors, Reviewers, and Program Chairs to demonstrate the complete paper lifecycle live."

---
*Ready for Review 2 Evaluation.*
