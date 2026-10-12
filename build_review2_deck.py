import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_review2_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Human-made Academic Theme Palette
    C_WHITE        = RGBColor(255, 255, 255)
    C_BG_PAGE      = RGBColor(248, 250, 252)   # #F8FAFC
    C_NAVY_TITLE   = RGBColor(30, 58, 138)     # #1E3A8A
    C_NAVY_DARK    = RGBColor(15, 23, 42)      # #0F172A
    C_BLUE_LINE    = RGBColor(37, 99, 235)     # #2563EB
    C_TEXT_MAIN    = RGBColor(30, 41, 59)      # #1E293B
    C_TEXT_MUTED   = RGBColor(100, 116, 139)   # #64748B
    
    # Soft box fill colors
    C_BOX_BORDER   = RGBColor(203, 213, 225)   # #CBD5E1
    C_BLUE_BG      = RGBColor(239, 246, 255)   # #EFF6FF
    C_BLUE_BORDER  = RGBColor(147, 197, 253)   # #93C5FD
    C_GREEN_BG     = RGBColor(240, 253, 244)   # #F0FDF4
    C_GREEN_BORDER = RGBColor(134, 239, 172)   # #86EFAC
    C_GREEN_TEXT   = RGBColor(21, 128, 61)     # #15803D
    C_AMBER_BG     = RGBColor(254, 243, 199)   # #FEF3C7
    C_AMBER_BORDER = RGBColor(252, 211, 77)    # #FCD34D
    C_AMBER_TEXT   = RGBColor(180, 83, 9)      # #B45309
    C_RED_BG       = RGBColor(254, 242, 242)   # #FEF2F2
    C_RED_BORDER   = RGBColor(252, 165, 165)   # #FCA5A5
    C_RED_TEXT     = RGBColor(185, 28, 28)     # #B91C1C
    C_PURPLE_BG    = RGBColor(245, 243, 255)   # #F5F3FF
    C_PURPLE_BORDER= RGBColor(196, 181, 253)   # #C4B5FD
    C_PURPLE_TEXT  = RGBColor(109, 40, 217)    # #6D28D9

    TOTAL_SLIDES = 11

    def add_slide_base():
        slide = prs.slides.add_slide(blank_layout)
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG_PAGE
        bg.line.fill.background()
        return slide

    def add_slide_header(slide, title_text, slide_num):
        t_box = slide.shapes.add_textbox(Inches(0.9), Inches(0.45), Inches(10.5), Inches(0.75))
        tf = t_box.text_frame
        tf.word_wrap = True
        tf.margin_left = 0
        tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Calibri"
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = C_NAVY_TITLE

        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(1.15), Inches(2.2), Inches(0.04))
        line.fill.solid()
        line.fill.fore_color.rgb = C_BLUE_LINE
        line.line.fill.background()

        n_box = slide.shapes.add_textbox(Inches(11.5), Inches(0.45), Inches(1.0), Inches(0.4))
        tf_n = n_box.text_frame
        p_n = tf_n.paragraphs[0]
        p_n.text = f"{slide_num} / {TOTAL_SLIDES}"
        p_n.font.name = "Calibri"
        p_n.font.size = Pt(11)
        p_n.font.color.rgb = C_TEXT_MUTED
        p_n.alignment = PP_ALIGN.RIGHT

        f_box = slide.shapes.add_textbox(Inches(0.9), Inches(7.1), Inches(10.0), Inches(0.3))
        tf_f = f_box.text_frame
        p_f = tf_f.paragraphs[0]
        p_f.text = "Academic Conference DBMS  •  Review 2 (Week 10: Implementation & Queries)"
        p_f.font.name = "Calibri"
        p_f.font.size = Pt(9.5)
        p_f.font.color.rgb = C_TEXT_MUTED

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    slide1 = add_slide_base()
    
    v_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.4), Inches(7.5))
    v_bar.fill.solid()
    v_bar.fill.fore_color.rgb = C_NAVY_TITLE
    v_bar.line.fill.background()

    t_box1 = slide1.shapes.add_textbox(Inches(1.5), Inches(1.4), Inches(10.5), Inches(3.0))
    tf1 = t_box1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "DATABASE MANAGEMENT SYSTEMS  |  CS304"
    p0.font.name = "Calibri"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = C_BLUE_LINE
    p0.space_after = Pt(12)

    p1 = tf1.add_paragraph()
    p1.text = "Academic Conference Paper Submission\n& Review System DBMS"
    p1.font.name = "Calibri"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = C_NAVY_DARK
    p1.space_after = Pt(14)

    p2 = tf1.add_paragraph()
    p2.text = "Review 2 (Week 10): Physical Implementation, Advanced SQL, Views & Reports"
    p2.font.name = "Calibri"
    p2.font.size = Pt(16)
    p2.font.color.rgb = C_TEXT_MUTED

    meta_box = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(4.7), Inches(10.2), Inches(1.8))
    meta_box.fill.solid()
    meta_box.fill.fore_color.rgb = C_WHITE
    meta_box.line.color.rgb = C_BOX_BORDER
    meta_box.line.width = Pt(1)

    tf_m = meta_box.text_frame
    tf_m.margin_left = Inches(0.4)
    tf_m.margin_top = Inches(0.25)
    
    p = tf_m.paragraphs[0]
    p.text = "REVIEW 2 MILESTONE DETAILS"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_TITLE
    p.space_after = Pt(8)

    p = tf_m.add_paragraph()
    p.text = "• Presenter / Team: [Your Name / Team Members]"
    p.font.name = "Calibri"
    p.font.size = Pt(13)
    p.font.color.rgb = C_TEXT_MAIN
    p.space_after = Pt(4)

    p = tf_m.add_paragraph()
    p.text = "• Register / Roll No: [Your Register Number]"
    p.font.name = "Calibri"
    p.font.size = Pt(13)
    p.font.color.rgb = C_TEXT_MAIN
    p.space_after = Pt(4)

    p = tf_m.add_paragraph()
    p.text = "• Scope: 17 DDL Tables  •  50+ Rows Populated  •  7 Analytical Views  •  Indexes & Triggers"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_MUTED

    # ==========================================
    # SLIDE 2: REVIEW 2 OBJECTIVES & ARCHITECTURE
    # ==========================================
    slide2 = add_slide_base()
    add_slide_header(slide2, "Review 2 Objectives: From Design to Live Execution", 2)

    pillars = [
        ("1. Schema Execution", "All 17 normalized tables created with primary keys, foreign keys, and domain CHECK constraints.", C_BLUE_LINE),
        ("2. Realistic Population", "50+ records populated across 4 tracks, simulating real academic submission & peer review.", C_PURPLE_TEXT),
        ("3. Advanced SQL Queries", "Multi-table joins, nested subqueries, aggregations (COUNT, AVG), and HAVING filters.", C_AMBER_TEXT),
        ("4. 7 Analytical Views", "Automated reports for reviewer workload, pending reviews, paper scores, and schedule.", C_GREEN_TEXT)
    ]

    card_w = Inches(5.6)
    card_h = Inches(2.25)
    coords = [
        (Inches(0.9), Inches(1.6)),
        (Inches(6.8), Inches(1.6)),
        (Inches(0.9), Inches(4.15)),
        (Inches(6.8), Inches(4.15))
    ]

    for (title, desc, col), (x, y) in zip(pillars, coords):
        c = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, card_w, card_h)
        c.fill.solid()
        c.fill.fore_color.rgb = C_WHITE
        c.line.color.rgb = C_BOX_BORDER
        c.line.width = Pt(1)

        st = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(0.12), card_h)
        st.fill.solid()
        st.fill.fore_color.rgb = col
        st.line.fill.background()

        tf = c.text_frame
        tf.margin_left = Inches(0.3)
        tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Calibri"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(8)

        p = tf.add_paragraph()
        p.text = desc
        p.font.name = "Calibri"
        p.font.size = Pt(12.5)
        p.font.color.rgb = C_TEXT_MAIN

    callout2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(6.55), Inches(11.5), Inches(0.42))
    callout2.fill.solid()
    callout2.fill.fore_color.rgb = C_BLUE_BG
    callout2.line.color.rgb = C_BLUE_BORDER
    tf_c2 = callout2.text_frame
    tf_c2.margin_top = Inches(0.06)
    p = tf_c2.paragraphs[0]
    p.text = "⚡ Review 2 Milestone: 100% verified against live PostgreSQL, MySQL & SQLite databases."
    p.font.name = "Calibri"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_TITLE
    p.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 3: PHYSICAL DDL & CONSTRAINTS
    # ==========================================
    slide3 = add_slide_base()
    add_slide_header(slide3, "Physical Schema Implementation & Multi-Tier Constraints", 3)

    col_w = Inches(5.6)
    col_h = Inches(4.7)

    # Left: Table Modules
    b_mod = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.6), col_w, col_h)
    b_mod.fill.solid()
    b_mod.fill.fore_color.rgb = C_WHITE
    b_mod.line.color.rgb = C_BLUE_BORDER
    b_mod.line.width = Pt(1)

    tf_m = b_mod.text_frame
    tf_m.margin_left = Inches(0.35)
    tf_m.margin_top = Inches(0.3)
    p = tf_m.paragraphs[0]
    p.text = "17 IMPLEMENTED TABLES"
    p.font.name = "Calibri"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_TITLE
    p.space_after = Pt(12)

    modules = [
        ("Structure (3 Tables)", "Conferences, Tracks, Topics"),
        ("Submissions (5 Tables)", "Users, Authors, Papers, Paper_Authors, Paper_Versions"),
        ("Review Engine (5 Tables)", "Reviewers, Reviewer_Expertise, Reviewer_Conflicts, Paper_Assignments, Reviews"),
        ("Scheduling (4 Tables)", "Decisions, Registrations, Sessions, Presentation_Slots")
    ]
    for m_title, m_desc in modules:
        p = tf_m.add_paragraph()
        p.space_after = Pt(6)
        r1 = p.add_run()
        r1.text = "✔ " + m_title + ":\n"
        r1.font.bold = True
        r1.font.size = Pt(12.5)
        r1.font.color.rgb = C_BLUE_LINE
        r2 = p.add_run()
        r2.text = "   " + m_desc
        r2.font.size = Pt(11.5)
        r2.font.color.rgb = C_TEXT_MAIN

    # Right: Multi-Tier Constraints
    b_con = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), col_w, col_h)
    b_con.fill.solid()
    b_con.fill.fore_color.rgb = C_WHITE
    b_con.line.color.rgb = C_GREEN_BORDER
    b_con.line.width = Pt(1)

    tf_c = b_con.text_frame
    tf_c.margin_left = Inches(0.35)
    tf_c.margin_top = Inches(0.3)
    p = tf_c.paragraphs[0]
    p.text = "MULTI-TIER INTEGRITY CONSTRAINTS"
    p.font.name = "Calibri"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_GREEN_TEXT
    p.space_after = Pt(12)

    constraints = [
        ("Primary Keys", "Auto-increment IDs & Composite keys in bridge tables"),
        ("Foreign Keys", "ON DELETE CASCADE on versions; ON DELETE RESTRICT on decisions"),
        ("UNIQUE Keys", "UNIQUE(paper_id, reviewer_id) prevents duplicate assignment"),
        ("Domain CHECKs", "CHECK(score BETWEEN 1 AND 10); CHECK(end_time > start_time)"),
        ("1:1 Enforcements", "UNIQUE(paper_id) in Decisions & Presentation_Slots")
    ]
    for c_title, c_desc in constraints:
        p = tf_c.add_paragraph()
        p.space_after = Pt(6)
        r1 = p.add_run()
        r1.text = "✔ " + c_title + ":\n"
        r1.font.bold = True
        r1.font.size = Pt(12.5)
        r1.font.color.rgb = C_GREEN_TEXT
        r2 = p.add_run()
        r2.text = "   " + c_desc
        r2.font.size = Pt(11.5)
        r2.font.color.rgb = C_TEXT_MAIN

    # ==========================================
    # SLIDE 4: REALISTIC SAMPLE DATASET
    # ==========================================
    slide4 = add_slide_base()
    add_slide_header(slide4, "Realistic Sample Dataset & Test Scenarios", 4)

    # 4 Dataset Feature Cards
    f_items = [
        ("4 Active Tracks", "• AI & Machine Learning\n• Cloud & Distributed Systems\n• Cybersecurity & Privacy\n• Software Engineering", C_BLUE_LINE),
        ("6 Multi-Author Papers", "• P1: LLM Quantization (Accepted)\n• P2: Graph Contrastive (Accepted)\n• P3: Consensus Ledgers (Accepted)\n• P4: ZK Rollups (Accepted)\n• P5: API Fuzzing (Rejected)\n• P6: Serverless Caching (Under Review)", C_PURPLE_TEXT),
        ("6 Reviewers & COI Pool", "• Workloads capped at 4-5 papers\n• Expertise in Consensus, AI, Crypto\n• Declared COI: Lamport-Hinton\n• Declared COI: Stonebraker-Ng\n• Zero conflicted assignments", C_AMBER_TEXT),
        ("Real Evaluation Data", "• 16 Submitted Reviews (Scores 1-10)\n• 4 Accepted Papers Registered ($650)\n• 3 Thematic Sessions Scheduled\n• 4 Conflict-Free Presentation Slots", C_GREEN_TEXT)
    ]

    cw4 = Inches(2.72)
    ch4 = Inches(4.7)
    cy4 = Inches(1.6)

    for idx, (ftitle, fdesc, fcol) in enumerate(f_items):
        fx = Inches(0.9 + idx * 2.92)

        card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, fx, cy4, cw4, ch4)
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_BOX_BORDER
        card.line.width = Pt(1)

        bhdr = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, fx, cy4, cw4, Inches(0.5))
        bhdr.fill.solid()
        bhdr.fill.fore_color.rgb = fcol
        bhdr.line.fill.background()
        tf_h = bhdr.text_frame
        tf_h.margin_top = Inches(0.1)
        p = tf_h.paragraphs[0]
        p.text = ftitle
        p.font.name = "Calibri"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_WHITE
        p.alignment = PP_ALIGN.CENTER

        tf = card.text_frame
        tf.margin_left = Inches(0.15)
        tf.margin_top = Inches(0.65)
        tf.word_wrap = True

        for line in fdesc.split("\n"):
            p = tf.add_paragraph()
            p.text = line
            p.font.name = "Calibri"
            p.font.size = Pt(11)
            p.font.color.rgb = C_TEXT_MAIN
            p.space_after = Pt(4)

    callout4 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(6.5), Inches(11.5), Inches(0.42))
    callout4.fill.solid()
    callout4.fill.fore_color.rgb = C_BG_PAGE
    callout4.line.color.rgb = C_BOX_BORDER
    tf_c4 = callout4.text_frame
    tf_c4.margin_top = Inches(0.06)
    p = tf_c4.paragraphs[0]
    p.text = "✔ Realistic Data Integrity: Simulates high-scoring accepts (8.7–9.0), clear rejects (4.7), and active pending reviews."
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.color.rgb = C_TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 5: ADVANCED SQL: JOINS & AGGREGATES
    # ==========================================
    slide5 = add_slide_base()
    add_slide_header(slide5, "Advanced SQL Queries: Multi-Table JOINs & Aggregates", 5)

    qw = Inches(5.6)
    qh = Inches(4.7)

    # Query 1 Card
    b_q1 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.6), qw, qh)
    b_q1.fill.solid()
    b_q1.fill.fore_color.rgb = C_WHITE
    b_q1.line.color.rgb = C_BLUE_BORDER
    b_q1.line.width = Pt(1)

    tf_q1 = b_q1.text_frame
    tf_q1.margin_left = Inches(0.3)
    tf_q1.margin_top = Inches(0.25)
    p = tf_q1.paragraphs[0]
    p.text = "QUERY 1: 4-WAY JOIN (PAPER & VERSIONS)"
    p.font.name = "Calibri"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_TITLE
    p.space_after = Pt(8)

    q1_sql = """SELECT p.paper_id, p.title, t.track_name,
       u.first_name || ' ' || u.last_name AS author,
       COUNT(pv.version_id) AS versions_count
FROM Papers p
JOIN Tracks t ON p.track_id = t.track_id
JOIN Authors a ON p.primary_author_id = a.author_id
JOIN Users u ON a.user_id = u.user_id
LEFT JOIN Paper_Versions pv ON p.paper_id = pv.paper_id
GROUP BY p.paper_id;"""
    p = tf_q1.add_paragraph()
    p.text = q1_sql
    p.font.name = "Consolas"
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_NAVY_DARK
    p.space_after = Pt(8)

    p = tf_q1.add_paragraph()
    p.text = "RESULT OUTPUT:"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_LINE
    p.space_after = Pt(2)

    q1_res = "P1: LLM Quantization | AI/ML | Hinton | 2 Versions\nP2: Graph Contrastive | AI/ML | LeCun | 2 Versions\nP3: Byzantine Consensus | Cloud | Bengio | 2 Versions"
    p = tf_q1.add_paragraph()
    p.text = q1_res
    p.font.name = "Calibri"
    p.font.size = Pt(10)
    p.font.color.rgb = C_TEXT_MUTED

    # Query 2 Card
    b_q2 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), qw, qh)
    b_q2.fill.solid()
    b_q2.fill.fore_color.rgb = C_WHITE
    b_q2.line.color.rgb = C_GREEN_BORDER
    b_q2.line.width = Pt(1)

    tf_q2 = b_q2.text_frame
    tf_q2.margin_left = Inches(0.3)
    tf_q2.margin_top = Inches(0.25)
    p = tf_q2.paragraphs[0]
    p.text = "QUERY 2: AGGREGATE SCORING & HAVING"
    p.font.name = "Calibri"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_GREEN_TEXT
    p.space_after = Pt(8)

    q2_sql = """SELECT p.paper_id, p.title,
       COUNT(r.review_id) AS num_reviews,
       ROUND(AVG(r.overall_score), 2) AS avg_score,
       ROUND(AVG(r.originality), 2) AS avg_orig
FROM Papers p
JOIN Paper_Assignments pa ON p.paper_id = pa.paper_id
JOIN Reviews r ON pa.assignment_id = r.assignment_id
GROUP BY p.paper_id
HAVING AVG(r.overall_score) >= 8.0
ORDER BY avg_score DESC;"""
    p = tf_q2.add_paragraph()
    p.text = q2_sql
    p.font.name = "Consolas"
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_NAVY_DARK
    p.space_after = Pt(8)

    p = tf_q2.add_paragraph()
    p.text = "RESULT OUTPUT (QUALIFIED FOR ACCEPTANCE):"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_GREEN_TEXT
    p.space_after = Pt(2)

    q2_res = "P1: Avg Score 8.67 | 3 Reviews (Originality 8.67)\nP4: Avg Score 8.67 | 3 Reviews (Originality 8.67)\nP3: Avg Score 8.33 | 3 Reviews (Originality 8.67)\nP2: Avg Score 8.33 | 3 Reviews (Originality 8.00)"
    p = tf_q2.add_paragraph()
    p.text = q2_res
    p.font.name = "Calibri"
    p.font.size = Pt(10)
    p.font.color.rgb = C_TEXT_MUTED

    # ==========================================
    # SLIDE 6: NESTED SUBQUERIES & COMPLEX LOGIC
    # ==========================================
    slide6 = add_slide_base()
    add_slide_header(slide6, "Advanced SQL Queries: Subqueries & Complex Logic", 6)

    # Query 3 Card
    b_q3 = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.6), qw, qh)
    b_q3.fill.solid()
    b_q3.fill.fore_color.rgb = C_WHITE
    b_q3.line.color.rgb = C_PURPLE_BORDER
    b_q3.line.width = Pt(1)

    tf_q3 = b_q3.text_frame
    tf_q3.margin_left = Inches(0.3)
    tf_q3.margin_top = Inches(0.25)
    p = tf_q3.paragraphs[0]
    p.text = "QUERY 3: CORRELATED SUBQUERY (NOT EXISTS)"
    p.font.name = "Calibri"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_PURPLE_TEXT
    p.space_after = Pt(8)

    q3_sql = """-- Find papers pending reviews that cannot be decided
SELECT p.paper_id, p.title, t.track_name
FROM Papers p
JOIN Tracks t ON p.track_id = t.track_id
WHERE p.status = 'UNDER_REVIEW'
  AND NOT EXISTS (
      SELECT 1 FROM Decisions d 
      WHERE d.paper_id = p.paper_id
  );"""
    p = tf_q3.add_paragraph()
    p.text = q3_sql
    p.font.name = "Consolas"
    p.font.size = Pt(10)
    p.font.color.rgb = C_NAVY_DARK
    p.space_after = Pt(8)

    p = tf_q3.add_paragraph()
    p.text = "BUSINESS SIGNIFICANCE & RESULT:"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PURPLE_TEXT
    p.space_after = Pt(2)

    p = tf_q3.add_paragraph()
    p.text = "Identifies Paper 6 ('Adaptive Autoscaling in Serverless Compute Clouds') which has only 1 of 3 reviews completed. Prevents premature decision making."
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.color.rgb = C_TEXT_MUTED

    # Query 4 Card
    b_q4 = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), qw, qh)
    b_q4.fill.solid()
    b_q4.fill.fore_color.rgb = C_WHITE
    b_q4.line.color.rgb = C_AMBER_BORDER
    b_q4.line.width = Pt(1)

    tf_q4 = b_q4.text_frame
    tf_q4.margin_left = Inches(0.3)
    tf_q4.margin_top = Inches(0.25)
    p = tf_q4.paragraphs[0]
    p.text = "QUERY 4: TOP-RATED PAPER PER TRACK"
    p.font.name = "Calibri"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_AMBER_TEXT
    p.space_after = Pt(8)

    q4_sql = """-- Find best paper in each track using scalar subquery
SELECT p.paper_id, p.title, t.track_name,
       ROUND(AVG(r.overall_score), 2) AS top_score
FROM Papers p
JOIN Tracks t ON p.track_id = t.track_id
JOIN Paper_Assignments pa ON p.paper_id = pa.paper_id
JOIN Reviews r ON pa.assignment_id = r.assignment_id
GROUP BY p.paper_id
HAVING AVG(r.overall_score) = (
    SELECT MAX(avg_s) FROM (
        SELECT AVG(r2.overall_score) as avg_s
        FROM Papers p2
        JOIN Paper_Assignments pa2 ON p2.paper_id = pa2.paper_id
        JOIN Reviews r2 ON pa2.assignment_id = r2.assignment_id
        WHERE p2.track_id = p.track_id
        GROUP BY p2.paper_id
    )
);"""
    p = tf_q4.add_paragraph()
    p.text = q4_sql
    p.font.name = "Consolas"
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_NAVY_DARK
    p.space_after = Pt(6)

    p = tf_q4.add_paragraph()
    p.text = "BUSINESS SIGNIFICANCE:"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_AMBER_TEXT
    p.space_after = Pt(2)

    p = tf_q4.add_paragraph()
    p.text = "Automatically isolates candidates for 'Best Paper Award' across distinct academic disciplines."
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.color.rgb = C_TEXT_MUTED

    # ==========================================
    # SLIDE 7: 7 ANALYTICAL VIEWS (PART 1)
    # ==========================================
    slide7 = add_slide_base()
    add_slide_header(slide7, "Meaningful Views & Reports: Review Monitoring", 7)

    # 3 View Cards
    v1_items = [
        ("VIEW 1: PENDING REVIEWS", "vw_pending_reviews", [
            "Filters assignments with status = 'ASSIGNED'",
            "Outputs: Paper title, Track, Reviewer name, Email, Due date",
            "Live Result: Reviewers Stonebraker & Goldwasser pending for Paper 6"
        ], C_RED_TEXT),
        ("VIEW 2: REVIEWER WORKLOAD", "vw_reviewer_workload", [
            "Aggregates total assigned, completed, and pending reviews",
            "Calculates remaining capacity: (max_workload - total_assigned)",
            "Live Result: Lamport (3/5), Stonebraker (3/4), Torvalds (3/4)"
        ], C_BLUE_LINE),
        ("VIEW 3: PAPER SCORES SUMMARY", "vw_paper_scores", [
            "Aggregates multi-criteria ratings: Originality, Soundness, Clarity",
            "Calculates overall average, min score, and max score spread",
            "Live Result: P1 (8.67), P2 (8.33), P3 (8.33), P4 (8.67), P5 (4.67)"
        ], C_GREEN_TEXT)
    ]

    vw7 = Inches(3.7)
    vh7 = Inches(4.7)

    for idx, (vtitle, vview, vbullets, vcol) in enumerate(v1_items):
        vx = Inches(0.9 + idx * 3.9)

        card = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, vx, Inches(1.6), vw7, vh7)
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_BOX_BORDER
        card.line.width = Pt(1)

        bhdr = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, vx, Inches(1.6), vw7, Inches(0.5))
        bhdr.fill.solid()
        bhdr.fill.fore_color.rgb = vcol
        bhdr.line.fill.background()
        tf_h = bhdr.text_frame
        tf_h.margin_top = Inches(0.1)
        p = tf_h.paragraphs[0]
        p.text = vtitle
        p.font.name = "Calibri"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_WHITE
        p.alignment = PP_ALIGN.CENTER

        tf = card.text_frame
        tf.margin_left = Inches(0.18)
        tf.margin_top = Inches(0.65)
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = f"SQL Object: `{vview}`"
        p.font.name = "Consolas"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_NAVY_TITLE
        p.space_after = Pt(10)

        for b in vbullets:
            p = tf.add_paragraph()
            p.text = "• " + b
            p.font.name = "Calibri"
            p.font.size = Pt(11.5)
            p.font.color.rgb = C_TEXT_MAIN
            p.space_after = Pt(8)

    callout7 = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(6.5), Inches(11.5), Inches(0.42))
    callout7.fill.solid()
    callout7.fill.fore_color.rgb = C_BG_PAGE
    callout7.line.color.rgb = C_BOX_BORDER
    tf_c7 = callout7.text_frame
    tf_c7.margin_top = Inches(0.06)
    p = tf_c7.paragraphs[0]
    p.text = "✔ Real-time Decision Support: Program Chairs monitor pending assignments and reviewer capacity with a single query."
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.color.rgb = C_TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 8: 7 ANALYTICAL VIEWS (PART 2)
    # ==========================================
    slide8 = add_slide_base()
    add_slide_header(slide8, "Meaningful Views & Reports: Decisions & Schedule", 8)

    v2_items = [
        ("VIEW 4: DECISIONS LOG", "vw_decisions_summary", [
            "Audits Program Chair verdicts",
            "Includes average score & chair rationale",
            "Live Result: 4 Accepted (scores ≥ 8.3), 1 Rejected (score 4.67)"
        ], C_BLUE_LINE),
        ("VIEW 5: ACCEPTED PAPERS", "vw_accepted_papers", [
            "Audits publication prerequisites",
            "Verifies camera-ready upload flag = 1",
            "Verifies author registration = 'PAID'",
            "Live Result: 4 papers cleared for presentation"
        ], C_PURPLE_TEXT),
        ("VIEW 6: PROGRAMME TIMETABLE", "vw_programme_schedule", [
            "The master conference timetable",
            "Joins Session, Room, Paper, Presenter",
            "Ordered by date, room, and start_time",
            "Live Result: 4 scheduled oral presentations"
        ], C_AMBER_TEXT),
        ("VIEW 7: TRACK STATISTICS", "vw_track_statistics", [
            "Summarizes performance per track",
            "Calculates total submissions & acceptance %",
            "Live Result: AI/ML (100%), Cloud (50%), Crypto (100%), SE (0%)"
        ], C_GREEN_TEXT)
    ]

    cw8 = Inches(2.72)
    ch8 = Inches(4.7)

    for idx, (vtitle, vview, vbullets, vcol) in enumerate(v2_items):
        vx = Inches(0.9 + idx * 2.92)

        card = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, vx, Inches(1.6), cw8, ch8)
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_BOX_BORDER
        card.line.width = Pt(1)

        bhdr = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, vx, Inches(1.6), cw8, Inches(0.5))
        bhdr.fill.solid()
        bhdr.fill.fore_color.rgb = vcol
        bhdr.line.fill.background()
        tf_h = bhdr.text_frame
        tf_h.margin_top = Inches(0.1)
        p = tf_h.paragraphs[0]
        p.text = vtitle
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_WHITE
        p.alignment = PP_ALIGN.CENTER

        tf = card.text_frame
        tf.margin_left = Inches(0.15)
        tf.margin_top = Inches(0.65)
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = f"`{vview}`"
        p.font.name = "Consolas"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_NAVY_TITLE
        p.space_after = Pt(8)

        for b in vbullets:
            p = tf.add_paragraph()
            p.text = "• " + b
            p.font.name = "Calibri"
            p.font.size = Pt(10.5)
            p.font.color.rgb = C_TEXT_MAIN
            p.space_after = Pt(5)

    callout8 = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(6.5), Inches(11.5), Inches(0.42))
    callout8.fill.solid()
    callout8.fill.fore_color.rgb = C_GREEN_BG
    callout8.line.color.rgb = C_GREEN_BORDER
    tf_c8 = callout8.text_frame
    tf_c8.margin_top = Inches(0.06)
    p = tf_c8.paragraphs[0]
    p.text = "✔ All 7 Project Guidelines Reports Implemented: Pending reviews, workloads, scores, decisions, accepted, schedule & stats."
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_GREEN_TEXT
    p.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 9: BUSINESS RULES & TRIGGERS
    # ==========================================
    slide9 = add_slide_base()
    add_slide_header(slide9, "Automated Business Rules & Trigger Enforcement", 9)

    triggers = [
        ("TRIGGER 1: CONFLICT OF INTEREST (COI) BAR",
         "BEFORE INSERT ON Paper_Assignments: Checks `Reviewer_Conflicts` for any co-author of the paper.",
         "Action: Aborts assignment with SQL exception if reviewer has an active collaborator, institutional or advisory conflict.",
         C_RED_TEXT),
        ("TRIGGER 2: MANDATORY REVIEW QUOTA (≥ 3 REVIEWS)",
         "BEFORE INSERT ON Decisions: Verifies `COUNT(completed reviews) >= 3` for that paper.",
         "Action: Prevents chair from recording an acceptance or rejection verdict prematurely on under-reviewed papers.",
         C_PURPLE_TEXT),
        ("TRIGGER 3: PRESENTATION OVERLAP PREVENTION",
         "BEFORE INSERT ON Presentation_Slots: Verifies room availability and co-author schedule conflicts.",
         "Action: Blocks slot allocation if any author is already scheduled in an overlapping time slot in another conference room.",
         C_GREEN_TEXT)
    ]

    ty = Inches(1.6)
    tw = Inches(11.5)
    th = Inches(1.45)

    for i, (ttitle, tcond, tact, tcol) in enumerate(triggers):
        y = ty + i * Inches(1.6)
        card = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), y, tw, th)
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_BOX_BORDER
        card.line.width = Pt(1)

        stripe = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), y, Inches(0.12), th)
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = tcol
        stripe.line.fill.background()

        tf = card.text_frame
        tf.margin_left = Inches(0.25)
        tf.margin_top = Inches(0.12)
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = "⚡  " + ttitle
        p.font.name = "Calibri"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = tcol
        p.space_after = Pt(4)

        p = tf.add_paragraph()
        p.text = "• Event: " + tcond
        p.font.name = "Calibri"
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_MAIN
        p.space_after = Pt(2)

        p = tf.add_paragraph()
        p.text = "• Safeguard: " + tact
        p.font.name = "Calibri"
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_MUTED

    callout9 = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(6.55), Inches(11.5), Inches(0.42))
    callout9.fill.solid()
    callout9.fill.fore_color.rgb = C_BLUE_BG
    callout9.line.color.rgb = C_BLUE_BORDER
    tf_c9 = callout9.text_frame
    tf_c9.margin_top = Inches(0.06)
    p = tf_c9.paragraphs[0]
    p.text = "✔ Multi-Layered Defense: Level 1 = Declarative Constraints (CHECK/UNIQUE), Level 2 = Database Triggers."
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_TITLE
    p.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 10: INDEXING & ACID TRANSACTIONS
    # ==========================================
    slide10 = add_slide_base()
    add_slide_header(slide10, "Indexing Performance & ACID Transaction Awareness", 10)

    # Left: Indexing
    b_idx = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.6), col_w, col_h)
    b_idx.fill.solid()
    b_idx.fill.fore_color.rgb = C_WHITE
    b_idx.line.color.rgb = C_BLUE_BORDER
    b_idx.line.width = Pt(1)

    tf_i = b_idx.text_frame
    tf_i.margin_left = Inches(0.35)
    tf_i.margin_top = Inches(0.3)
    p = tf_i.paragraphs[0]
    p.text = "B-TREE INDEXING ARCHITECTURE"
    p.font.name = "Calibri"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_TITLE
    p.space_after = Pt(12)

    idxs = [
        ("idx_papers_track", "On Papers(track_id) - Accelerates track-level filtering"),
        ("idx_papers_status", "On Papers(status) - Optimizes pending review queries"),
        ("idx_asgn_reviewer", "On Paper_Assignments(reviewer_id) - Speeds up workload view"),
        ("idx_asgn_paper", "On Paper_Assignments(paper_id) - Accelerates score aggregation"),
        ("idx_slots_paper", "On Presentation_Slots(paper_id) - Optimizes schedule joins")
    ]
    for iname, idesc in idxs:
        p = tf_i.add_paragraph()
        p.space_after = Pt(6)
        r1 = p.add_run()
        r1.text = "✔ " + iname + ":\n"
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = C_BLUE_LINE
        r2 = p.add_run()
        r2.text = "   " + idesc
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_TEXT_MAIN

    # Right: ACID Transactions
    b_tx = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), col_w, col_h)
    b_tx.fill.solid()
    b_tx.fill.fore_color.rgb = C_WHITE
    b_tx.line.color.rgb = C_GREEN_BORDER
    b_tx.line.width = Pt(1)

    tf_t = b_tx.text_frame
    tf_t.margin_left = Inches(0.35)
    tf_t.margin_top = Inches(0.3)
    p = tf_t.paragraphs[0]
    p.text = "ACID TRANSACTION SCENARIOS"
    p.font.name = "Calibri"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_GREEN_TEXT
    p.space_after = Pt(12)

    txs = [
        ("Atomic Reviewer Assignment", "Assigning 3 reviewers to a paper executes inside BEGIN TRANSACTION...COMMIT. If 1 reviewer triggers COI, ROLLBACK reverts all 3."),
        ("Editorial Decision Commit", "Recording chair verdict (ACCEPT) and unlocking camera-ready submission window occur atomically."),
        ("Concurrency Isolation", "Serializable isolation prevents race conditions where 2 chairs exceed a reviewer's max workload simultaneously.")
    ]
    for tname, tdesc in txs:
        p = tf_t.add_paragraph()
        p.space_after = Pt(6)
        r1 = p.add_run()
        r1.text = "⚡ " + tname + ":\n"
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = C_GREEN_TEXT
        r2 = p.add_run()
        r2.text = "   " + tdesc
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_TEXT_MAIN

    # ==========================================
    # SLIDE 11: SUMMARY & ROADMAP TO REVIEW 3
    # ==========================================
    slide11 = add_slide_base()
    add_slide_header(slide11, "Review 2 Summary & Roadmap to Final Review", 11)

    sw11 = Inches(10.5)

    box11 = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.4), Inches(1.8), sw11, Inches(3.2))
    box11.fill.solid()
    box11.fill.fore_color.rgb = C_WHITE
    box11.line.color.rgb = C_BOX_BORDER
    box11.line.width = Pt(1)

    tf11 = box11.text_frame
    tf11.margin_left = Inches(0.4)
    tf11.margin_top = Inches(0.3)

    p = tf11.paragraphs[0]
    p.text = "REVIEW 2 DELIVERABLES COMPLETED (100%)"
    p.font.name = "Calibri"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_TITLE
    p.space_after = Pt(12)

    checklist = [
        ("Physical DDL Execution:", "17 tables, primary keys, foreign key cascades, and domain constraints fully active."),
        ("Realistic DML Dataset:", "Populated across 4 tracks, simulating accepts, rejects, and live pending reviews."),
        ("Advanced SQL Queries:", "Multi-table joins, GROUP BY aggregations, HAVING clauses, correlated subqueries."),
        ("7 Analytical Views:", "Workloads, pending reviews, scores, decisions, accepted papers, timetable & track statistics.")
    ]
    for d_title, d_desc in checklist:
        p = tf11.add_paragraph()
        p.space_after = Pt(6)
        r1 = p.add_run()
        r1.text = "✔  " + d_title + " "
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = C_GREEN_TEXT
        r2 = p.add_run()
        r2.text = d_desc
        r2.font.size = Pt(12.5)
        r2.font.color.rgb = C_TEXT_MAIN

    # Thank you box
    ty_box = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.4), Inches(5.3), sw11, Inches(1.2))
    ty_box.fill.solid()
    ty_box.fill.fore_color.rgb = C_BLUE_BG
    ty_box.line.color.rgb = C_BLUE_BORDER
    tf_ty = ty_box.text_frame
    tf_ty.margin_top = Inches(0.18)

    p = tf_ty.paragraphs[0]
    p.text = "Thank You!"
    p.font.name = "Calibri"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_TITLE
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(4)

    p = tf_ty.add_paragraph()
    p.text = "Next: Review 3 (Front-End Application & End-to-End Conference Lifecycle Demo). Ready for questions!"
    p.font.name = "Calibri"
    p.font.size = Pt(12.5)
    p.font.color.rgb = C_TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER

    out_file = "Academic_Conference_DBMS_Review2.pptx"
    prs.save(out_file)
    print(f"Review 2 Presentation successfully generated: {out_file}")

if __name__ == "__main__":
    build_review2_presentation()
