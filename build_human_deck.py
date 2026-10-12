import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_human_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Human-made Corporate / Academic Theme Colors
    C_WHITE        = RGBColor(255, 255, 255)
    C_BG_PAGE      = RGBColor(248, 250, 252)   # #F8FAFC (clean light background)
    C_NAVY_TITLE   = RGBColor(30, 58, 138)     # #1E3A8A (classic navy)
    C_NAVY_DARK    = RGBColor(15, 23, 42)      # #0F172A
    C_BLUE_LINE    = RGBColor(37, 99, 235)     # #2563EB (accent blue)
    C_TEXT_MAIN    = RGBColor(30, 41, 59)      # #1E293B (charcoal)
    C_TEXT_MUTED   = RGBColor(100, 116, 139)   # #64748B (slate grey)
    
    # Soft box fill colors (pastel, professional, human-like)
    C_BOX_BG       = RGBColor(255, 255, 255)
    C_BOX_BORDER   = RGBColor(203, 213, 225)   # #CBD5E1
    C_BLUE_BG      = RGBColor(239, 246, 255)   # #EFF6FF
    C_BLUE_BORDER  = RGBColor(147, 197, 253)   # #93C5FD
    C_RED_BG       = RGBColor(254, 242, 242)   # #FEF2F2
    C_RED_BORDER   = RGBColor(252, 165, 165)   # #FCA5A5
    C_RED_TEXT     = RGBColor(185, 28, 28)     # #B91C1C
    C_GREEN_BG     = RGBColor(240, 253, 244)   # #F0FDF4
    C_GREEN_BORDER = RGBColor(134, 239, 172)   # #86EFAC
    C_GREEN_TEXT   = RGBColor(21, 128, 61)     # #15803D
    C_AMBER_BG     = RGBColor(254, 243, 199)   # #FEF3C7
    C_AMBER_BORDER = RGBColor(252, 211, 77)    # #FCD34D
    C_AMBER_TEXT   = RGBColor(180, 83, 9)      # #B45309
    C_PURPLE_BG    = RGBColor(245, 243, 255)   # #F5F3FF
    C_PURPLE_BORDER= RGBColor(196, 181, 253)   # #C4B5FD
    C_PURPLE_TEXT  = RGBColor(109, 40, 217)    # #6D28D9

    TOTAL_SLIDES = 10

    def add_slide_base():
        slide = prs.slides.add_slide(blank_layout)
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG_PAGE
        bg.line.fill.background()
        return slide

    def add_slide_header(slide, title_text, slide_num):
        # Clean Human Header (Left Title + Accent Underline)
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

        # Clean Accent Line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(1.15), Inches(2.2), Inches(0.04))
        line.fill.solid()
        line.fill.fore_color.rgb = C_BLUE_LINE
        line.line.fill.background()

        # Simple Slide Number
        n_box = slide.shapes.add_textbox(Inches(11.5), Inches(0.45), Inches(1.0), Inches(0.4))
        tf_n = n_box.text_frame
        p_n = tf_n.paragraphs[0]
        p_n.text = f"{slide_num} / {TOTAL_SLIDES}"
        p_n.font.name = "Calibri"
        p_n.font.size = Pt(11)
        p_n.font.color.rgb = C_TEXT_MUTED
        p_n.alignment = PP_ALIGN.RIGHT

        # Simple Footer
        f_box = slide.shapes.add_textbox(Inches(0.9), Inches(7.1), Inches(10.0), Inches(0.3))
        tf_f = f_box.text_frame
        p_f = tf_f.paragraphs[0]
        p_f.text = "Academic Conference DBMS  •  Review 1 (Week 7)"
        p_f.font.name = "Calibri"
        p_f.font.size = Pt(9.5)
        p_f.font.color.rgb = C_TEXT_MUTED

    # ==========================================
    # SLIDE 1: TITLE SLIDE (Clean Academic Style)
    # ==========================================
    slide1 = add_slide_base()
    
    # Left accent vertical bar
    v_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.4), Inches(7.5))
    v_bar.fill.solid()
    v_bar.fill.fore_color.rgb = C_NAVY_TITLE
    v_bar.line.fill.background()

    # Title Container
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
    p2.text = "Review 1 (Week 7): Scope, Conceptual ER Design & Relational Schema"
    p2.font.name = "Calibri"
    p2.font.size = Pt(16)
    p2.font.color.rgb = C_TEXT_MUTED

    # Student metadata card (Clean white box with soft border)
    meta_box = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(4.7), Inches(10.2), Inches(1.8))
    meta_box.fill.solid()
    meta_box.fill.fore_color.rgb = C_WHITE
    meta_box.line.color.rgb = C_BOX_BORDER
    meta_box.line.width = Pt(1)

    tf_m = meta_box.text_frame
    tf_m.margin_left = Inches(0.4)
    tf_m.margin_top = Inches(0.25)
    
    p = tf_m.paragraphs[0]
    p.text = "PROJECT METADATA & TEAM"
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
    p.text = "• Target Database: PostgreSQL / MySQL  |  Evaluation Weightage: 5 Marks"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_MUTED

    # ==========================================
    # SLIDE 2: PROBLEM STATEMENT (Visual Comparison)
    # ==========================================
    slide2 = add_slide_base()
    add_slide_header(slide2, "Problem Statement: Why Email & Spreadsheets Fail", 2)

    # 4 Human-style Problem Tiles
    card_w = Inches(5.6)
    card_h = Inches(2.25)
    
    problems = [
        ("📁 Version Confusion", "Authors email updated PDFs; reviewers evaluate old drafts.", "Loss of camera-ready final files."),
        ("⚖ Conflict of Interest (COI)", "Reviewers assigned papers written by close collaborators.", "Ethical breach & biased evaluation."),
        ("⏳ Workload Imbalance", "Some reviewers get 10 papers, others get none.", "Missed deadlines & missing 3-review quota."),
        ("📅 Schedule Collisions", "Authors with multiple papers booked in two halls at once.", "Overlapping presentation slots.")
    ]

    coords = [
        (Inches(0.9), Inches(1.6)),
        (Inches(6.8), Inches(1.6)),
        (Inches(0.9), Inches(4.15)),
        (Inches(6.8), Inches(4.15))
    ]

    for (title, line1, line2), (x, y) in zip(problems, coords):
        c = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, card_w, card_h)
        c.fill.solid()
        c.fill.fore_color.rgb = C_WHITE
        c.line.color.rgb = C_RED_BORDER
        c.line.width = Pt(1)

        # Left stripe
        st = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(0.12), card_h)
        st.fill.solid()
        st.fill.fore_color.rgb = C_RED_TEXT
        st.line.fill.background()

        tf = c.text_frame
        tf.margin_left = Inches(0.3)
        tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Calibri"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = C_RED_TEXT
        p.space_after = Pt(8)

        p = tf.add_paragraph()
        p.text = "• " + line1
        p.font.name = "Calibri"
        p.font.size = Pt(13)
        p.font.color.rgb = C_TEXT_MAIN
        p.space_after = Pt(4)

        p = tf.add_paragraph()
        p.text = "• " + line2
        p.font.name = "Calibri"
        p.font.size = Pt(13)
        p.font.color.rgb = C_TEXT_MUTED

    callout2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(6.55), Inches(11.5), Inches(0.42))
    callout2.fill.solid()
    callout2.fill.fore_color.rgb = C_GREEN_BG
    callout2.line.color.rgb = C_GREEN_BORDER
    tf_c2 = callout2.text_frame
    tf_c2.margin_top = Inches(0.06)
    p = tf_c2.paragraphs[0]
    p.text = "✔ Solution: A 3NF relational database enforcing versioning, automated COI blocking, and slot validation."
    p.font.name = "Calibri"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_GREEN_TEXT
    p.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 3: OBJECTIVES & SCOPE
    # ==========================================
    slide3 = add_slide_base()
    add_slide_header(slide3, "Project Scope & Core Objectives", 3)

    col_w = Inches(5.6)
    col_h = Inches(4.7)

    # Left: Objectives
    b_obj = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.6), col_w, col_h)
    b_obj.fill.solid()
    b_obj.fill.fore_color.rgb = C_WHITE
    b_obj.line.color.rgb = C_BLUE_BORDER
    b_obj.line.width = Pt(1)

    tf_o = b_obj.text_frame
    tf_o.margin_left = Inches(0.35)
    tf_o.margin_top = Inches(0.3)
    
    p = tf_o.paragraphs[0]
    p.text = "🎯 CORE OBJECTIVES"
    p.font.name = "Calibri"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_TITLE
    p.space_after = Pt(14)

    obj_list = [
        ("3NF Database Design", "Eliminate data redundancy & anomalies."),
        ("Double-Blind Peer Review", "Conceal author identity from reviewers."),
        ("Automated COI Prevention", "Block biased reviewer assignments."),
        ("Multi-Version Tracking", "Preserve initial drafts & camera-ready PDFs."),
        ("Conflict-Free Scheduling", "No author or hall presentation clashes.")
    ]
    for title, sub in obj_list:
        p = tf_o.add_paragraph()
        p.space_after = Pt(8)
        r1 = p.add_run()
        r1.text = "✔ " + title + ": "
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = C_BLUE_LINE
        r2 = p.add_run()
        r2.text = sub
        r2.font.size = Pt(12)
        r2.font.color.rgb = C_TEXT_MAIN

    # Right: Scope & Users
    b_scp = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), col_w, col_h)
    b_scp.fill.solid()
    b_scp.fill.fore_color.rgb = C_WHITE
    b_scp.line.color.rgb = C_BOX_BORDER
    b_scp.line.width = Pt(1)

    tf_s = b_scp.text_frame
    tf_s.margin_left = Inches(0.35)
    tf_s.margin_top = Inches(0.3)

    p = tf_s.paragraphs[0]
    p.text = "📦 SYSTEM SCOPE & USERS"
    p.font.name = "Calibri"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_TITLE
    p.space_after = Pt(14)

    p = tf_s.add_paragraph()
    p.text = "IN-SCOPE FOR REVIEW 1:"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_MUTED
    p.space_after = Pt(4)

    for item in [
        "14 Principal Entities & ER Diagram",
        "Initial Relational Schema in 3NF",
        "Primary Keys, Foreign Keys, CHECK constraints"
    ]:
        p = tf_s.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(12.5)
        p.font.color.rgb = C_TEXT_MAIN
        p.space_after = Pt(4)

    p = tf_s.add_paragraph()
    p.text = "USER ROLES (RBAC):"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_MUTED
    p.space_before = Pt(8)
    p.space_after = Pt(4)

    for role in [
        "Program Chair & Track Chairs",
        "Authors & Co-Authors",
        "Reviewers & Attendees"
    ]:
        p = tf_s.add_paragraph()
        p.text = "• " + role
        p.font.size = Pt(12.5)
        p.font.color.rgb = C_TEXT_MAIN
        p.space_after = Pt(4)

    # ==========================================
    # SLIDE 4: THE CONFERENCE LIFECYCLE WORKFLOW
    # ==========================================
    slide4 = add_slide_base()
    add_slide_header(slide4, "System Workflow: From Submission to Presentation", 4)

    steps = [
        ("Step 1", "Submission", "• Author uploads paper\n• Co-authors assigned\n• Blinded PDF (V1)", C_BLUE_LINE),
        ("Step 2", "Reviewer Match", "• Topic expertise set\n• Conflicts declared\n• Zero-COI assignment", C_PURPLE_TEXT),
        ("Step 3", "Peer Review", "• ≥ 3 Reviews/paper\n• Scores 1 to 10\n• Dual comments", C_AMBER_TEXT),
        ("Step 4", "Decision", "• Chair records verdict\n• Accept / Reject\n• Camera-ready PDF", C_RED_TEXT),
        ("Step 5", "Scheduling", "• Author registers\n• Hall & slot assigned\n• No time overlaps", C_GREEN_TEXT)
    ]

    sw = Inches(2.15)
    sh = Inches(4.3)
    sy = Inches(1.8)

    for idx, (s_num, s_title, s_text, col) in enumerate(steps):
        sx = Inches(0.9 + idx * 2.38)
        
        box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, sy, sw, sh)
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BOX_BORDER
        box.line.width = Pt(1)

        # Top Badge
        badge = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, sy, sw, Inches(0.55))
        badge.fill.solid()
        badge.fill.fore_color.rgb = col
        badge.line.fill.background()
        tf_b = badge.text_frame
        tf_b.margin_top = Inches(0.1)
        p = tf_b.paragraphs[0]
        p.text = s_num.upper()
        p.font.name = "Calibri"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_WHITE
        p.alignment = PP_ALIGN.CENTER

        tf = box.text_frame
        tf.margin_left = Inches(0.15)
        tf.margin_top = Inches(0.7)
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = s_title
        p.font.name = "Calibri"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = col
        p.alignment = PP_ALIGN.CENTER
        p.space_after = Pt(10)

        for line in s_text.split("\n"):
            p = tf.add_paragraph()
            p.text = line
            p.font.name = "Calibri"
            p.font.size = Pt(11.5)
            p.font.color.rgb = C_TEXT_MAIN
            p.space_after = Pt(5)

        # Arrow
        if idx < len(steps) - 1:
            arr = slide4.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, sx + sw + Inches(0.05), sy + Inches(1.8), Inches(0.15), Inches(0.25))
            arr.fill.solid()
            arr.fill.fore_color.rgb = C_TEXT_MUTED
            arr.line.fill.background()

    callout4 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(6.35), Inches(11.5), Inches(0.45))
    callout4.fill.solid()
    callout4.fill.fore_color.rgb = C_BLUE_BG
    callout4.line.color.rgb = C_BLUE_BORDER
    tf_c4 = callout4.text_frame
    tf_c4.margin_top = Inches(0.08)
    p = tf_c4.paragraphs[0]
    p.text = "⚡ Automated Progression: Each stage is strictly gated by database integrity constraints."
    p.font.name = "Calibri"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_TITLE
    p.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 5: FUNCTIONAL REQUIREMENTS (6 Simple Cards)
    # ==========================================
    slide5 = add_slide_base()
    add_slide_header(slide5, "Key Functional Requirements", 5)

    fr_items = [
        ("1. Paper & Versioning", "• Unique auto-increment paper_id\n• Blinded manuscript upload\n• Multi-version tracking (V1, V2, Camera-ready)"),
        ("2. Expertise & COI", "• Reviewers set topic competence\n• Explicit conflict declaration\n• Automated conflict barring"),
        ("3. Reviewer Assignment", "• Max workload limit per reviewer\n• Minimum 3 reviews required per paper\n• Workload balance tracking"),
        ("4. Review Scoring", "• 1 to 10 scale (Originality, Soundness, Clarity)\n• Public comments to author\n• Confidential remarks to Chair"),
        ("5. Editorial Decisions", "• Formal verdict: Accept / Reject / Revise\n• Only decided after ≥ 3 reviews\n• Author notification logging"),
        ("6. Presentation Scheduling", "• Verification of paid author registration\n• Hall & time slot allocation\n• Zero author schedule overlap")
    ]

    fw = Inches(3.7)
    fh = Inches(2.25)

    for i, (title, text) in enumerate(fr_items):
        col_idx = i % 3
        row_idx = i // 3
        x = Inches(0.9 + col_idx * 3.9)
        y = Inches(1.6 + row_idx * 2.5)

        card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, fw, fh)
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_BOX_BORDER
        card.line.width = Pt(1)

        # Header bar
        bar = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, fw, Inches(0.45))
        bar.fill.solid()
        bar.fill.fore_color.rgb = C_BLUE_BG
        bar.line.fill.background()
        tf_b = bar.text_frame
        tf_b.margin_left = Inches(0.15)
        tf_b.margin_top = Inches(0.08)
        p = tf_b.paragraphs[0]
        p.text = title
        p.font.name = "Calibri"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_NAVY_TITLE

        tf = card.text_frame
        tf.margin_left = Inches(0.18)
        tf.margin_top = Inches(0.55)
        tf.word_wrap = True

        for idx_l, line in enumerate(text.split("\n")):
            p = tf.paragraphs[0] if idx_l == 0 else tf.add_paragraph()
            p.text = line
            p.font.name = "Calibri"
            p.font.size = Pt(11.5)
            p.font.color.rgb = C_TEXT_MAIN
            p.space_after = Pt(4)

    # ==========================================
    # SLIDE 6: THE 14 PRINCIPAL ENTITIES
    # ==========================================
    slide6 = add_slide_base()
    add_slide_header(slide6, "Conceptual Design: The 14 Principal Entities", 6)

    ent_clusters = [
        ("1. STRUCTURE", [
            ("Conferences", "Root event, dates, deadline"),
            ("Tracks", "Conference research domains"),
            ("Topics", "Keywords for paper matching")
        ], C_BLUE_LINE),
        ("2. SUBMISSION", [
            ("Authors", "Researcher profile, ORCID"),
            ("Papers", "Master submission record"),
            ("Versions", "Drafts & camera-ready PDFs")
        ], C_PURPLE_TEXT),
        ("3. REVIEW ENGINE", [
            ("Reviewers", "Evaluator profile & capacity"),
            ("Expertise", "Topic competence level"),
            ("Conflicts", "COI declaration records"),
            ("Assignments", "Paper-to-reviewer link"),
            ("Reviews", "1-10 scores & feedback")
        ], C_AMBER_TEXT),
        ("4. SCHEDULING", [
            ("Decisions", "Official Accept/Reject log"),
            ("Registrations", "Author fee & clearance"),
            ("Presentation_Slots", "Hall & session time slot")
        ], C_GREEN_TEXT)
    ]

    ew = Inches(2.72)
    eh = Inches(4.7)
    ey = Inches(1.6)

    for idx, (grp_name, items, col) in enumerate(ent_clusters):
        ex = Inches(0.9 + idx * 2.92)

        c = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, ex, ey, ew, eh)
        c.fill.solid()
        c.fill.fore_color.rgb = C_WHITE
        c.line.color.rgb = C_BOX_BORDER
        c.line.width = Pt(1)

        # Header
        chdr = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, ex, ey, ew, Inches(0.5))
        chdr.fill.solid()
        chdr.fill.fore_color.rgb = col
        chdr.line.fill.background()
        tf_h = chdr.text_frame
        tf_h.margin_top = Inches(0.1)
        p = tf_h.paragraphs[0]
        p.text = grp_name
        p.font.name = "Calibri"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_WHITE
        p.alignment = PP_ALIGN.CENTER

        tf = c.text_frame
        tf.margin_left = Inches(0.15)
        tf.margin_top = Inches(0.65)
        tf.word_wrap = True

        for idx_e, (ename, edesc) in enumerate(items):
            p = tf.paragraphs[0] if idx_e == 0 else tf.add_paragraph()
            p.space_after = Pt(2)
            r1 = p.add_run()
            r1.text = ename + "\n"
            r1.font.bold = True
            r1.font.size = Pt(12)
            r1.font.color.rgb = C_TEXT_MAIN
            r2 = p.add_run()
            r2.text = edesc + "\n"
            r2.font.size = Pt(10)
            r2.font.color.rgb = C_TEXT_MUTED

    callout6 = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(6.5), Inches(11.5), Inches(0.42))
    callout6.fill.solid()
    callout6.fill.fore_color.rgb = C_BG_PAGE
    callout6.line.color.rgb = C_BOX_BORDER
    tf_c6 = callout6.text_frame
    tf_c6.margin_top = Inches(0.06)
    p = tf_c6.paragraphs[0]
    p.text = "✔ Plus supporting entities: Users (central accounts) and Paper_Authors (multi-author bridge)."
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.color.rgb = C_TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 7: CONCEPTUAL ER DIAGRAM (Image)
    # ==========================================
    slide7 = add_slide_base()
    add_slide_header(slide7, "Conceptual Entity-Relationship (ER) Diagram", 7)

    # Embed High-Resolution ER Diagram Image
    er_img_path = "er_diagram.png"
    if os.path.exists(er_img_path):
        # Frame box behind the picture
        frame = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.3), Inches(11.533), Inches(5.65))
        frame.fill.solid()
        frame.fill.fore_color.rgb = C_WHITE
        frame.line.color.rgb = C_BOX_BORDER
        frame.line.width = Pt(1)

        slide7.shapes.add_picture(er_img_path, Inches(0.95), Inches(1.35), width=Inches(11.433), height=Inches(5.55))
    else:
        # Fallback if image not found
        f_box = slide7.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(10.0), Inches(2.0))
        f_tf = f_box.text_frame
        p = f_tf.paragraphs[0]
        p.text = "ER Diagram Image will be placed here."

    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_TITLE
    p.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 8: RELATIONAL SCHEMA SUMMARY (Clean Table)
    # ==========================================
    slide8 = add_slide_base()
    add_slide_header(slide8, "Initial Relational Schema: Tables & Keys", 8)

    tbl_headers = ["Table Name", "Primary Key", "Foreign Keys", "Key Constraints"]
    tbl_data = [
        ["Conferences", "conference_id", "None", "UNIQUE(acronym, year), end_date >= start_date"],
        ["Tracks", "track_id", "conference_id", "UNIQUE(conference_id, track_name)"],
        ["Topics", "topic_id", "track_id", "UNIQUE(track_id, topic_name)"],
        ["Users", "user_id", "None", "UNIQUE(email), role IN ('CHAIR','AUTHOR','REVIEWER')"],
        ["Authors", "author_id", "user_id", "1:1 with Users; stores ORCID & bio"],
        ["Papers", "paper_id", "track_id, primary_author", "status IN ('SUBMITTED','UNDER_REVIEW','ACCEPTED','REJECTED')"],
        ["Paper_Versions", "version_id", "paper_id", "UNIQUE(paper_id, version_num), version_num >= 1"],
        ["Reviewers", "reviewer_id", "user_id", "1:1 with Users; max_workload > 0 (DEFAULT 5)"],
        ["Reviewer_Conflicts", "conflict_id", "reviewer_id, author_id", "UNIQUE(reviewer_id, author_id); blocks COI assignments"],
        ["Paper_Assignments", "assignment_id", "paper_id, reviewer_id", "UNIQUE(paper_id, reviewer_id), status IN ('ASSIGNED','COMPLETED')"],
        ["Reviews", "review_id", "assignment_id (UNIQUE)", "CHECK scores BETWEEN 1 AND 10 for all 3 criteria"],
        ["Decisions", "decision_id", "paper_id (UNIQUE)", "decision_type IN ('ACCEPT','REJECT','REVISE')"],
        ["Presentation_Slots", "slot_id", "session_id, paper_id (UK)", "CHECK(end_time > start_time), no room or author overlaps"]
    ]

    rows = len(tbl_data) + 1
    cols = 4
    tbl_shape = slide8.shapes.add_table(rows, cols, Inches(0.9), Inches(1.5), Inches(11.5), Inches(5.2))
    tbl = tbl_shape.table
    col_widths = [Inches(2.2), Inches(1.8), Inches(2.6), Inches(4.9)]
    for c_idx, w in enumerate(col_widths):
        tbl.columns[c_idx].width = w

    # Header row
    for c_idx, h_text in enumerate(tbl_headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_TITLE
        tf = cell.text_frame
        tf.margin_left = Inches(0.12)
        p = tf.paragraphs[0]
        p.text = h_text
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    # Data rows
    for r_idx, row in enumerate(tbl_data):
        bg = C_WHITE if (r_idx % 2 == 0) else C_BG_PAGE
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            tf = cell.text_frame
            tf.margin_left = Inches(0.12)
            p = tf.paragraphs[0]
            p.text = val
            p.font.name = "Calibri"
            p.font.size = Pt(9.5)
            if c_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_TEXT_MAIN
            elif c_idx == 1:
                p.font.color.rgb = C_RED_TEXT
            elif c_idx == 2:
                p.font.color.rgb = C_BLUE_LINE
            else:
                p.font.color.rgb = C_TEXT_MAIN

    # ==========================================
    # SLIDE 9: NORMALIZATION & BUSINESS RULES
    # ==========================================
    slide9 = add_slide_base()
    add_slide_header(slide9, "Normalization (1NF → 3NF) & Business Rules", 9)

    col_w = Inches(5.6)
    col_h = Inches(4.7)

    # Left: Normalization
    b_norm = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.6), col_w, col_h)
    b_norm.fill.solid()
    b_norm.fill.fore_color.rgb = C_WHITE
    b_norm.line.color.rgb = C_BLUE_BORDER
    b_norm.line.width = Pt(1)

    tf_n = b_norm.text_frame
    tf_n.margin_left = Inches(0.3)
    tf_n.margin_top = Inches(0.25)

    p = tf_n.paragraphs[0]
    p.text = "NORMALIZATION STRATEGY"
    p.font.name = "Calibri"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_TITLE
    p.space_after = Pt(12)

    norm_steps = [
        ("First Normal Form (1NF)", "All attributes are atomic scalar values.", "• Co-authors split into Paper_Authors table\n• Multi-version files split into Paper_Versions"),
        ("Second Normal Form (2NF)", "No partial functional dependencies on composite PK.", "• In Paper_Authors(paper_id, author_id), order depends on both keys\n• Author bio moved to Authors table"),
        ("Third Normal Form (3NF)", "No transitive functional dependencies.", "• Track names decoupled from Papers (stored in Tracks)\n• User details centralized in Users table")
    ]
    for n_title, n_cond, n_proof in norm_steps:
        p = tf_n.add_paragraph()
        p.text = "✔ " + n_title
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = C_BLUE_LINE
        p.space_after = Pt(2)

        p = tf_n.add_paragraph()
        p.text = n_cond
        p.font.size = Pt(11)
        p.font.color.rgb = C_TEXT_MAIN
        p.space_after = Pt(2)

        for line in n_proof.split("\n"):
            p = tf_n.add_paragraph()
            p.text = line
            p.font.size = Pt(10)
            p.font.color.rgb = C_TEXT_MUTED
            p.space_after = Pt(2)
        p.space_after = Pt(6)

    # Right: 5 Business Rules
    b_rule = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), col_w, col_h)
    b_rule.fill.solid()
    b_rule.fill.fore_color.rgb = C_WHITE
    b_rule.line.color.rgb = C_GREEN_BORDER
    b_rule.line.width = Pt(1)

    tf_r = b_rule.text_frame
    tf_r.margin_left = Inches(0.3)
    tf_r.margin_top = Inches(0.25)

    p = tf_r.paragraphs[0]
    p.text = "5 ENFORCED BUSINESS RULES"
    p.font.name = "Calibri"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_GREEN_TEXT
    p.space_after = Pt(12)

    br_list = [
        ("1. Unique Submission ID", "Every paper receives an auto-increment PK."),
        ("2. Strict Conflict Barring", "Reviewers cannot evaluate collaborator papers."),
        ("3. Minimum Review Quota", "≥ 3 completed reviews required before decision."),
        ("4. Standardized Scores", "CHECK (score BETWEEN 1 AND 10)."),
        ("5. No Schedule Overlap", "Authors cannot present in two rooms at once.")
    ]
    for r_title, r_desc in br_list:
        p = tf_r.add_paragraph()
        p.space_after = Pt(6)
        r1 = p.add_run()
        r1.text = "✔ " + r_title + "\n"
        r1.font.bold = True
        r1.font.size = Pt(12.5)
        r1.font.color.rgb = C_GREEN_TEXT
        r2 = p.add_run()
        r2.text = "   " + r_desc
        r2.font.size = Pt(11.5)
        r2.font.color.rgb = C_TEXT_MAIN

    # ==========================================
    # SLIDE 10: CONCLUSION & DISCUSSION
    # ==========================================
    slide10 = add_slide_base()
    add_slide_header(slide10, "Summary & Evaluator Discussion", 10)

    sw10 = Inches(10.5)
    
    # Checkbox card
    box10 = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.4), Inches(1.8), sw10, Inches(3.2))
    box10.fill.solid()
    box10.fill.fore_color.rgb = C_WHITE
    box10.line.color.rgb = C_BOX_BORDER
    box10.line.width = Pt(1)

    tf10 = box10.text_frame
    tf10.margin_left = Inches(0.4)
    tf10.margin_top = Inches(0.3)

    p = tf10.paragraphs[0]
    p.text = "REVIEW 1 DELIVERABLES COMPLETED"
    p.font.name = "Calibri"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_TITLE
    p.space_after = Pt(12)

    checklist = [
        ("Deliverable 1:", "Problem identification, scope, SMART objectives, 6 user roles, functional requirements."),
        ("Deliverable 2:", "Conceptual design & ER diagram covering all 14 principal entities + relationships."),
        ("Deliverable 3:", "Initial 3NF relational schema, primary/foreign keys, domain CHECK constraints & business rules.")
    ]
    for d_title, d_desc in checklist:
        p = tf10.add_paragraph()
        p.space_after = Pt(8)
        r1 = p.add_run()
        r1.text = "✔  " + d_title + " "
        r1.font.bold = True
        r1.font.size = Pt(13.5)
        r1.font.color.rgb = C_GREEN_TEXT
        r2 = p.add_run()
        r2.text = d_desc
        r2.font.size = Pt(13)
        r2.font.color.rgb = C_TEXT_MAIN

    # Thank you box
    ty_box = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.4), Inches(5.3), sw10, Inches(1.2))
    ty_box.fill.solid()
    ty_box.fill.fore_color.rgb = C_BLUE_BG
    ty_box.line.color.rgb = C_BLUE_BORDER
    tf_ty = ty_box.text_frame
    tf_ty.margin_top = Inches(0.2)

    p = tf_ty.paragraphs[0]
    p.text = "Thank You!"
    p.font.name = "Calibri"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_TITLE
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(4)

    p = tf_ty.add_paragraph()
    p.text = "We are ready for questions and suggestions from the evaluators."
    p.font.name = "Calibri"
    p.font.size = Pt(13)
    p.font.color.rgb = C_TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER

    out_file = "Academic_Conference_DBMS_Review1_Human.pptx"
    prs.save(out_file)
    print(f"Human-styled 10-slide presentation saved to: {out_file}")

if __name__ == "__main__":
    create_human_deck()
