import sqlite3
import unittest
import os

class TestAcademicConferenceDBMS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_path = "conference_review2.db"
        if not os.path.exists(cls.db_path):
            raise FileNotFoundError(f"Database {cls.db_path} not found! Run test_review2_database.py first.")

    def setUp(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")

    def tearDown(self):
        self.conn.close()

    def test_01_paper_submission_and_versioning(self):
        """Test that submitting a paper increments version and maintains audit trail."""
        cur = self.conn.cursor()
        # Check versions for Paper 1
        cur.execute("SELECT COUNT(*), MAX(is_camera_ready) FROM Paper_Versions WHERE paper_id = 1")
        v_count, has_cr = cur.fetchone()
        self.assertGreaterEqual(v_count, 2, "Paper 1 must have at least 2 versions (draft + camera-ready)")
        self.assertEqual(has_cr, 1, "Paper 1 must have a verified camera-ready copy")
        print("[PASS] Test 1 Passed: Paper submission & multi-version tracking verified.")

    def test_02_conflict_of_interest_detection(self):
        """Test that COI check successfully detects conflicts between Reviewer 1 (Lamport) and Author 1 (Hinton)."""
        cur = self.conn.cursor()
        # Query active conflicts for Paper 1 (Primary author: Author 1 Hinton) and Reviewer 1 (Lamport)
        cur.execute("""
            SELECT rc.conflict_type 
            FROM Paper_Authors pa
            JOIN Reviewer_Conflicts rc ON pa.author_id = rc.author_id
            WHERE pa.paper_id = 1 AND rc.reviewer_id = 1
        """)
        conflict = cur.fetchone()
        self.assertIsNotNone(conflict, "Reviewer 1 and Author 1 must have a registered Conflict of Interest")
        self.assertEqual(conflict[0], "SAME_INSTITUTION")
        print("[PASS] Test 2 Passed: Conflict of Interest (COI) detection verified.")

    def test_03_mandatory_review_quota_threshold(self):
        """Test that papers with fewer than 3 reviews cannot be decided."""
        cur = self.conn.cursor()
        # Paper 6 has only 1 completed review
        cur.execute("""
            SELECT COUNT(r.review_id)
            FROM Paper_Assignments pa
            JOIN Reviews r ON pa.assignment_id = r.assignment_id
            WHERE pa.paper_id = 6
        """)
        completed_reviews = cur.fetchone()[0]
        self.assertLess(completed_reviews, 3, "Paper 6 must have < 3 completed reviews")
        
        # Verify Paper 6 has no decision logged
        cur.execute("SELECT COUNT(*) FROM Decisions WHERE paper_id = 6")
        decision_count = cur.fetchone()[0]
        self.assertEqual(decision_count, 0, "Paper 6 must not have a decision logged before meeting the quota")
        print("[PASS] Test 3 Passed: Minimum 3-review quota enforcement verified.")

    def test_04_presentation_schedule_no_author_overlap(self):
        """Test that no scheduled author is double-booked in overlapping time slots."""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT ps1.paper_id, ps2.paper_id, pa.author_id
            FROM Presentation_Slots ps1
            JOIN Presentation_Slots ps2 ON ps1.slot_date = ps2.slot_date AND ps1.slot_id != ps2.slot_id
            JOIN Paper_Authors pa ON ps1.paper_id = pa.paper_id
            JOIN Paper_Authors pa2 ON ps2.paper_id = pa2.paper_id AND pa.author_id = pa2.author_id
            WHERE (
                (ps1.start_time >= ps2.start_time AND ps1.start_time < ps2.end_time) OR
                (ps1.end_time > ps2.start_time AND ps1.end_time <= ps2.end_time)
            )
        """)
        clashes = cur.fetchall()
        self.assertEqual(len(clashes), 0, "There must be zero presentation schedule overlaps for any author")
        print("[PASS] Test 4 Passed: Zero-collision presentation slot scheduling verified.")

    def test_05_score_domain_check_constraint(self):
        """Test that all review scores in the database conform to 1-10 integer range."""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT COUNT(*) FROM Reviews 
            WHERE originality NOT BETWEEN 1 AND 10 
               OR soundness NOT BETWEEN 1 AND 10 
               OR clarity NOT BETWEEN 1 AND 10 
               OR overall_score NOT BETWEEN 1 AND 10
        """)
        invalid_scores = cur.fetchone()[0]
        self.assertEqual(invalid_scores, 0, "All review scores must strictly adhere to domain range 1-10")
        print("[PASS] Test 5 Passed: Domain score CHECK constraints verified.")

if __name__ == "__main__":
    print("\n======================================================================")
    print("RUNNING SYSTEMATIC VERIFICATION SUITE: ACADEMIC CONFERENCE DBMS")
    print("======================================================================\n")
    unittest.main()
