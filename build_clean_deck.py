import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_visual_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    # Palette
    C_NAVY_DARK    = RGBColor(11, 25, 44)      # #0B192C
    C_BLUE_PRIMARY = RGBColor(30, 58, 138)     # #1E3A8A
    C_BLUE_ACCENT  = RGBColor(37, 99, 235)     # #2563EB
    C_CYAN_ACCENT  = RGBColor(14, 165, 233)    # #0EA5E9
    C_TEAL         = RGBColor(13, 148, 136)    # #0D9488
    C_EMERALD      = RGBColor(16, 185, 129)    # #10B981
    C_AMBER        = RGBColor(217, 119, 6)     # #D97706
    C_CORAL_RED    = RGBColor(225, 29, 72)     # #E11D48
    C_PURPLE       = RGBColor(124, 58, 237)    # #7C3AED
    
    C_BG_LIGHT     = RGBColor(248, 250, 252)   # #F8FAFC
    C_CARD_BG      = RGBColor(255, 255, 255)   # #FFFFFF
    C_CARD_BORDER  = RGBColor(226, 232, 240)   # #E2E8F0
    
    C_TEXT_DARK    = RGBColor(15, 23, 42)      # #0F172A
    C_TEXT_MUTED   = RGBColor(71, 85, 105)     # #475569
    C_TEXT_LIGHT   = RGBColor(241, 245, 249)   # #F1F5F9
    C_TEXT_WHITE   = RGBColor(255, 255, 255)
    
    TOTAL_SLIDES = 11

    def add_blank_slide(bg_color=C_BG_LIGHT):
        slide = prs.slides.add_slide(blank_layout)
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = bg_color
        bg.line.fill.background()
        return slide

    def add_header(slide, title_text, category_text):
        # Header banner
        hdr = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.95))
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = C_CARD_BG
        hdr.line.color.rgb = C_CARD_BORDER
        hdr.line.width = Pt(1)

        # Left accent stripe
        stripe = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(0.14), Inches(0.95))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = C_BLUE_ACCENT
        stripe.line.fill.background()

        tf = hdr.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.35)
        tf.margin_top = Inches(0.12)

        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = C_BLUE_ACCENT

        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(20)
        p1.font.bold = True
        p1.font.color.rgb = C_TEXT_DARK

    def add_footer(slide, slide_num):
        box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.35))
        tf = box.text_frame
        p = tf.paragraphs[0]
        p.text = f"Academic Conference DBMS  |  Review 1 (Week 7)  |  Slide {slide_num} of {TOTAL_SLIDES}"
        p.font.size = Pt(9)
        p.font.color.rgb = C_TEXT_MUTED

    # ==========================================
    # SLIDE 1: TITLE SLIDE (Dark Executive Theme)
    # ==========================================
    slide1 = add_blank_slide(C_NAVY_DARK)
    
    top_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.15))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = C_CYAN_ACCENT
    top_bar.line.fill.background()

    # Title box
    tbox = slide1.shapes.add_textbox(Inches(1.0), Inches(1.1), Inches(11.333), Inches(2.3))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "DATABASE MANAGEMENT SYSTEMS  •  REVIEW 1 (WEEK 7)"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = C_CYAN_ACCENT
    p0.space_after = Pt(10)

    p1 = tf1.add_paragraph()
    p1.text = "Academic Conference Paper Submission &\nReview System DBMS"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = C_TEXT_WHITE
    p1.space_after = Pt(12)

    p2 = tf1.add_paragraph()
    p2.text = "Conceptual ER Modeling  |  14 Principal Entities  |  3NF Relational Schema  |  Constraint Logic"
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(148, 163, 184)

    # 3 Summary Cards
    cards_y = Inches(3.9)
    cw = Inches(3.55)
    ch = Inches(2.5)

    # Card 1
    c1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), cards_y, cw, ch)
    c1.fill.solid()
    c1.fill.fore_color.rgb = RGBColor(15, 34, 64)
    c1.line.color.rgb = RGBColor(30, 58, 138)
    tf_c1 = c1.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_left = Inches(0.25)
    tf_c1.margin_top = Inches(0.25)
    p = tf_c1.paragraphs[0]
    p.text = "🎯 REVIEW 1 FOCUS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT
    p.space_after = Pt(8)
    for b in [
        "Problem Identification & Scope",
        "User Roles & Functional Requirements",
        "Conceptual ER Model (14 Entities)",
        "3NF Relational Schema & Constraints"
    ]:
        p = tf_c1.add_paragraph()
        p.text = "✔  " + b
        p.font.size = Pt(11)
        p.font.color.rgb = C_TEXT_LIGHT
        p.space_after = Pt(4)

    # Card 2
    c2 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.88), cards_y, cw, ch)
    c2.fill.solid()
    c2.fill.fore_color.rgb = RGBColor(15, 34, 64)
    c2.line.color.rgb = RGBColor(30, 58, 138)
    tf_c2 = c2.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_left = Inches(0.25)
    tf_c2.margin_top = Inches(0.25)
    p = tf_c2.paragraphs[0]
    p.text = "⚙ KEY CAPABILITIES"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT
    p.space_after = Pt(8)
    for b in [
        "Multi-Version Paper Tracking",
        "Zero Conflict-of-Interest Assignment",
        "Double-Blind Peer Review Support",
        "Non-Overlapping Session Scheduling"
    ]:
        p = tf_c2.add_paragraph()
        p.text = "⚡  " + b
        p.font.size = Pt(11)
        p.font.color.rgb = C_TEXT_LIGHT
        p.space_after = Pt(4)

    # Card 3
    c3 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.76), cards_y, cw, ch)
    c3.fill.solid()
    c3.fill.fore_color.rgb = RGBColor(15, 34, 64)
    c3.line.color.rgb = RGBColor(30, 58, 138)
    tf_c3 = c3.text_frame
    tf_c3.word_wrap = True
    tf_c3.margin_left = Inches(0.25)
    tf_c3.margin_top = Inches(0.25)
    p = tf_c3.paragraphs[0]
    p.text = "👥 PRESENTATION DETAILS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT
    p.space_after = Pt(8)
    for b in [
        "Course: CS304 - DBMS",
        "Milestone: Review 1 (Week 7)",
        "Presenter: [Student Name / Team]",
        "Target DBMS: PostgreSQL / MySQL"
    ]:
        p = tf_c3.add_paragraph()
        p.text = "•  " + b
        p.font.size = Pt(11)
        p.font.color.rgb = C_TEXT_LIGHT
        p.space_after = Pt(4)

    # ==========================================
    # SLIDE 2: PROBLEM VS SOLUTION (Visual Side-by-Side)
    # ==========================================
    slide2 = add_blank_slide()
    add_header(slide2, "Why We Need a Dedicated DBMS", "Problem Identification & Motivation")
    add_footer(slide2, 2)

    pw = Inches(5.65)
    ph = Inches(5.0)

    # Left Card: The Problem (Red Accent)
    card_prob = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), pw, ph)
    card_prob.fill.solid()
    card_prob.fill.fore_color.rgb = C_CARD_BG
    card_prob.line.color.rgb = RGBColor(254, 205, 211)
    card_prob.line.width = Pt(1.5)

    hdr_prob = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), pw, Inches(0.65))
    hdr_prob.fill.solid()
    hdr_prob.fill.fore_color.rgb = C_CORAL_RED
    hdr_prob.line.fill.background()
    tf_hp = hdr_prob.text_frame
    tf_hp.margin_left = Inches(0.25)
    tf_hp.margin_top = Inches(0.15)
    p = tf_hp.paragraphs[0]
    p.text = "❌  TRADITIONAL EMAIL & SPREADSHEET FLAWS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_WHITE

    tb_prob = slide2.shapes.add_textbox(Inches(1.05), Inches(2.4), pw - Inches(0.5), ph - Inches(0.9))
    tf_pb = tb_prob.text_frame
    tf_pb.word_wrap = True
    issues = [
        ("Lost Versions:", "Authors email revised PDFs; reviewers end up scoring obsolete drafts."),
        ("Conflict of Interest (COI):", "Reviewers accidentally assigned papers by co-authors or colleagues, causing bias."),
        ("Workload Chaos:", "Some reviewers get 10+ papers while others get zero; no deadline tracking."),
        ("Opaque Scores:", "Unstructured feedback with no separation of confidential chair notes."),
        ("Schedule Clashes:", "Authors with multiple papers double-booked across simultaneous halls.")
    ]
    for idx, (title, desc) in enumerate(issues):
        p = tf_pb.paragraphs[0] if idx == 0 else tf_pb.add_paragraph()
        p.space_after = Pt(8)
        r1 = p.add_run()
        r1.text = "•  " + title + " "
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = C_CORAL_RED
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(11.5)
        r2.font.color.rgb = C_TEXT_DARK

    # Right Card: The Solution (Emerald/Teal Accent)
    card_sol = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.85), Inches(1.6), pw, ph)
    card_sol.fill.solid()
    card_sol.fill.fore_color.rgb = C_CARD_BG
    card_sol.line.color.rgb = RGBColor(167, 243, 208)
    card_sol.line.width = Pt(1.5)

    hdr_sol = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.85), Inches(1.6), pw, Inches(0.65))
    hdr_sol.fill.solid()
    hdr_sol.fill.fore_color.rgb = C_TEAL
    hdr_sol.line.fill.background()
    tf_hs = hdr_sol.text_frame
    tf_hs.margin_left = Inches(0.25)
    tf_hs.margin_top = Inches(0.15)
    p = tf_hs.paragraphs[0]
    p.text = "✔  OUR RELATIONAL DBMS SOLUTION"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_WHITE

    tb_sol = slide2.shapes.add_textbox(Inches(7.1), Inches(2.4), pw - Inches(0.5), ph - Inches(0.9))
    tf_sb = tb_sol.text_frame
    tf_sb.word_wrap = True
    solutions = [
        ("Multi-Version Store:", "Dedicated table tracks V1, V2, and verified camera-ready files cleanly."),
        ("Automated COI Bar:", "System blocks assigning reviewers with declared author conflicts."),
        ("Capacity Control:", "Enforces max workload (default 5) and requires ≥3 reviews per paper."),
        ("Multi-Criteria Rubric:", "1-10 scores for Originality, Soundness, Clarity + Private Chair comments."),
        ("Collision-Free Scheduling:", "Validates presentation slots so no author or room overlaps.")
    ]
    for idx, (title, desc) in enumerate(solutions):
        p = tf_sb.paragraphs[0] if idx == 0 else tf_sb.add_paragraph()
        p.space_after = Pt(8)
        r1 = p.add_run()
        r1.text = "•  " + title + " "
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = C_TEAL
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(11.5)
        r2.font.color.rgb = C_TEXT_DARK

    # ==========================================
    # SLIDE 3: OBJECTIVES, SCOPE & USER ROLES
    # ==========================================
    slide3 = add_blank_slide()
    add_header(slide3, "Project Scope, Objectives & User Roles", "Scope & Requirements Overview")
    add_footer(slide3, 3)

    # 4 Top Objective Cards
    ow = Inches(2.78)
    oh = Inches(1.5)
    oy = Inches(1.6)

    objs = [
        ("1. 3NF Integrity", "Normalized schema eliminating insertion, deletion, and update anomalies.", C_BLUE_PRIMARY),
        ("2. Double-Blind Peer Review", "Zero author-reviewer conflict bias via automated constraint checking.", C_TEAL),
        ("3. Multi-Version Audit", "Immutable history separating initial review drafts from camera-ready files.", C_AMBER),
        ("4. Conflict-Free Timetable", "Strict constraints preventing room double-booking and author slot overlaps.", C_PURPLE)
    ]
    for i, (title, desc, color) in enumerate(objs):
        x = Inches(0.8 + i * 2.98)
        card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, oy, ow, oh)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = color
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.15)
        tf.margin_top = Inches(0.15)
        p0 = tf.paragraphs[0]
        p0.text = "🎯 " + title
        p0.font.size = Pt(11.5)
        p0.font.bold = True
        p0.font.color.rgb = color
        p0.space_after = Pt(4)
        p1 = tf.add_paragraph()
        p1.text = desc
        p1.font.size = Pt(9.5)
        p1.font.color.rgb = C_TEXT_DARK

    # Bottom Left: Scope
    sc_w = Inches(5.65)
    sc_h = Inches(3.4)
    sc_y = Inches(3.35)

    card_sc = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), sc_y, sc_w, sc_h)
    card_sc.fill.solid()
    card_sc.fill.fore_color.rgb = C_CARD_BG
    card_sc.line.color.rgb = C_CARD_BORDER
    tf_sc = card_sc.text_frame
    tf_sc.word_wrap = True
    tf_sc.margin_left = Inches(0.25)
    tf_sc.margin_top = Inches(0.2)
    p = tf_sc.paragraphs[0]
    p.text = "📦 PROJECT SCOPE (IN-SCOPE VS OUT-OF-SCOPE)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_PRIMARY
    p.space_after = Pt(6)

    sc_items = [
        ("In-Scope (Review 1):", "14 principal entities, normalized schema, primary/foreign keys, domain constraints."),
        ("In-Scope (Submission):", "Multi-author, multi-track, multi-version tracking with blind manuscript storage."),
        ("In-Scope (Review Engine):", "Expertise matching, explicit conflict registration, quota tracking, 1-10 scoring."),
        ("In-Scope (Scheduling):", "Oral session allocation, non-overlapping hall time slots."),
        ("Delimited / Out-of-Scope:", "Live banking payment gateway (simulated via transaction IDs) & live WebRTC video.")
    ]
    for title, desc in sc_items:
        p = tf_sc.add_paragraph()
        p.space_after = Pt(3)
        r1 = p.add_run()
        r1.text = "• " + title + " "
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = C_TEXT_DARK
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_TEXT_MUTED

    # Bottom Right: User Roles
    card_ur = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.85), sc_y, sc_w, sc_h)
    card_ur.fill.solid()
    card_ur.fill.fore_color.rgb = C_CARD_BG
    card_ur.line.color.rgb = C_CARD_BORDER
    tf_ur = card_ur.text_frame
    tf_ur.word_wrap = True
    tf_ur.margin_left = Inches(0.25)
    tf_ur.margin_top = Inches(0.2)
    p = tf_ur.paragraphs[0]
    p.text = "👥 USER ROLES & ACCESS CONTROL (RBAC)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p.space_after = Pt(6)

    roles = [
        ("Program Chair:", "Overall conference management, final acceptance/rejection decisions, timetable approval."),
        ("Track Chair:", "Manages papers and reviewers within a specific track (e.g. AI/ML, Networks)."),
        ("Author:", "Submits papers, uploads revisions, views final review feedback, registers for conference."),
        ("Reviewer:", "Declares expertise & conflicts, downloads blinded papers, submits 1-10 evaluation scores."),
        ("Attendee / Presenter:", "Registers, pays conference fee, presents paper, accesses conference program.")
    ]
    for title, desc in roles:
        p = tf_ur.add_paragraph()
        p.space_after = Pt(3)
        r1 = p.add_run()
        r1.text = "• " + title + " "
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = C_TEXT_DARK
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_TEXT_MUTED

    # ==========================================
    # SLIDE 4: THE CONFERENCE LIFECYCLE WORKFLOW (Visual Pipeline)
    # ==========================================
    slide4 = add_blank_slide()
    add_header(slide4, "End-to-End Conference Lifecycle Pipeline", "System Workflow & Data Flow")
    add_footer(slide4, 4)

    steps = [
        ("1. SUBMISSION", "Author submits paper\n• Title & Abstract\n• Co-author ordering\n• Blind PDF uploaded\n• Initial Version (V1)", C_BLUE_PRIMARY),
        ("2. COI & MATCH", "Reviewer Profiling\n• Topic expertise setup\n• COI declared\n• System matches papers\n• Zero-conflict check", C_PURPLE),
        ("3. PEER REVIEW", "Evaluation Stage\n• Min 3 reviews/paper\n• Scores 1-10 (4 metrics)\n• Author comments\n• Chair private notes", C_AMBER),
        ("4. DECISION", "Program Chair\n• Aggregates scores\n• Accept / Reject / Revise\n• Camera-ready upload\n• Feedback dispatched", C_CORAL_RED),
        ("5. SCHEDULING", "Conference Program\n• Author registration\n• Hall & session booking\n• Zero room overlap\n• Zero author overlap", C_TEAL)
    ]

    bw = Inches(2.15)
    bh = Inches(4.3)
    by = Inches(1.8)

    for idx, (title, content, col) in enumerate(steps):
        bx = Inches(0.8 + idx * 2.4)
        
        # Step Box
        box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, bw, bh)
        box.fill.solid()
        box.fill.fore_color.rgb = C_CARD_BG
        box.line.color.rgb = col
        box.line.width = Pt(2)

        # Header of box
        bhdr = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, bw, Inches(0.6))
        bhdr.fill.solid()
        bhdr.fill.fore_color.rgb = col
        bhdr.line.fill.background()
        tf_h = bhdr.text_frame
        tf_h.margin_top = Inches(0.12)
        p = tf_h.paragraphs[0]
        p.text = title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_WHITE
        p.alignment = PP_ALIGN.CENTER

        # Body of box
        tb = slide4.shapes.add_textbox(bx + Inches(0.12), by + Inches(0.7), bw - Inches(0.24), bh - Inches(0.8))
        tf_b = tb.text_frame
        tf_b.word_wrap = True
        for line_idx, line in enumerate(content.split("\n")):
            p = tf_b.paragraphs[0] if line_idx == 0 else tf_b.add_paragraph()
            p.text = line
            if line_idx == 0:
                p.font.bold = True
                p.font.size = Pt(11)
                p.font.color.rgb = col
                p.space_after = Pt(8)
            else:
                p.font.size = Pt(10)
                p.font.color.rgb = C_TEXT_DARK
                p.space_after = Pt(4)

        # Arrow between boxes
        if idx < len(steps) - 1:
            arr = slide4.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, bx + bw + Inches(0.05), by + Inches(1.8), Inches(0.15), Inches(0.25))
            arr.fill.solid()
            arr.fill.fore_color.rgb = C_BLUE_ACCENT
            arr.line.fill.background()

    callout4 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.25), Inches(11.733), Inches(0.65))
    callout4.fill.solid()
    callout4.fill.fore_color.rgb = RGBColor(238, 242, 255)
    callout4.line.color.rgb = C_BLUE_ACCENT
    tf_c4 = callout4.text_frame
    tf_c4.margin_left = Inches(0.25)
    tf_c4.margin_top = Inches(0.1)
    p = tf_c4.paragraphs[0]
    p.text = "⚡ Automated Business Pipeline: Each stage is strictly validated by database constraints before advancing to the next."
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_PRIMARY

    # ==========================================
    # SLIDE 5: FUNCTIONAL REQUIREMENTS (6 Visual Cards)
    # ==========================================
    slide5 = add_blank_slide()
    add_header(slide5, "Functional Requirements: 6 Core Modules", "System Functional Specifications")
    add_footer(slide5, 5)

    fr_cards = [
        ("FR1: Paper & Version Lifecycle", [
            "Unique submission ID auto-generated",
            "Multi-author association & sequence",
            "Discrete versions (V1, V2, Camera-ready)",
            "Blinded manuscripts for peer review"
        ], C_BLUE_PRIMARY),
        ("FR2: Expertise & Conflict Bar", [
            "Reviewers set topic ratings (Expert/Informed)",
            "Explicit COI declaration (Co-author, Institution)",
            "Automated assignment blocking on COI",
            "Prevents self-review & collaborator bias"
        ], C_PURPLE),
        ("FR3: Assignment Engine", [
            "Reviewer capacity cap (Max workload = 5)",
            "Mandatory quota: ≥3 reviews per paper",
            "Topic matching algorithm support",
            "Real-time pending review monitoring"
        ], C_BLUE_ACCENT),
        ("FR4: Multi-Criteria Review Scoring", [
            "Numerical evaluation [1-10] for 4 criteria",
            "Originality, Technical Soundness, Clarity",
            "Overall acceptance recommendation score",
            "Separation: Public comments vs Private notes"
        ], C_AMBER),
        ("FR5: Editorial Decisions", [
            "Program Chair records binding verdict",
            "Accept, Reject, Major / Minor Revision",
            "Gated by completed review count",
            "Enables camera-ready upload upon Accept"
        ], C_CORAL_RED),
        ("FR6: Registration & Scheduling", [
            "Verifies paid registration for accepted papers",
            "Thematic session & room allocation",
            "Prevents room double-booking",
            "Zero overlapping time slots for same author"
        ], C_TEAL)
    ]

    cw5 = Inches(3.7)
    ch5 = Inches(2.3)

    for i, (title, bullets, col) in enumerate(fr_cards):
        col_idx = i % 3
        row_idx = i // 3
        x = Inches(0.8 + col_idx * 4.01)
        y = Inches(1.7 + row_idx * 2.55)

        card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, cw5, ch5)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = col
        card.line.width = Pt(1.5)

        # Header
        chdr = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, cw5, Inches(0.48))
        chdr.fill.solid()
        chdr.fill.fore_color.rgb = col
        chdr.line.fill.background()
        tf_h = chdr.text_frame
        tf_h.margin_left = Inches(0.18)
        tf_h.margin_top = Inches(0.1)
        p = tf_h.paragraphs[0]
        p.text = title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_WHITE

        # Body
        tb = slide5.shapes.add_textbox(x + Inches(0.15), y + Inches(0.55), cw5 - Inches(0.3), ch5 - Inches(0.6))
        tf_b = tb.text_frame
        tf_b.word_wrap = True
        for b_idx, b in enumerate(bullets):
            p = tf_b.paragraphs[0] if b_idx == 0 else tf_b.add_paragraph()
            p.text = "✔ " + b
            p.font.size = Pt(10.5)
            p.font.color.rgb = C_TEXT_DARK
            p.space_after = Pt(2.5)

    # ==========================================
    # SLIDE 6: THE 14 PRINCIPAL ENTITIES (4 Thematic Clusters)
    # ==========================================
    slide6 = add_blank_slide()
    add_header(slide6, "Conceptual Design: The 14 Principal Entities", "Core Conceptual Data Model")
    add_footer(slide6, 6)

    clusters = [
        ("CLUSTER 1: CONFERENCE STRUCTURE", [
            ("1. Conferences", "Root event, acronym, year, dates, submission deadline"),
            ("2. Tracks", "Conference subdivisions (e.g., AI/ML, Networks, Security)"),
            ("3. Topics", "Granular scientific keywords for paper & expertise matching")
        ], C_BLUE_PRIMARY),
        ("CLUSTER 2: SUBMISSIONS & VERSIONS", [
            ("4. Authors", "Researcher profiles (ORCID, bio) linked to base Users"),
            ("5. Papers", "Master submission tracking title, abstract, and status"),
            ("6. Versions", "Document revisions (V1, V2, Camera-ready PDFs, changelogs)")
        ], C_PURPLE),
        ("CLUSTER 3: REVIEW ENGINE", [
            ("7. Reviewers", "Peer evaluator profiles with max workload limits"),
            ("8. Expertise", "Reviewer competence mapping (Expert, Knowledgeable)"),
            ("9. Conflicts", "Explicit COI declarations barring biased assignments"),
            ("10. Assignments", "Dispatches papers to eligible, non-conflicted reviewers"),
            ("11. Reviews", "1-10 scores (Originality, Soundness, Clarity) + comments")
        ], C_AMBER),
        ("CLUSTER 4: DECISIONS & SCHEDULING", [
            ("12. Decisions", "Chair's binding verdict (Accept, Reject, Major/Minor Revise)"),
            ("13. Registrations", "Author & attendee conference fees and clearance"),
            ("14. Presentation_Slots", "Hall, session, and time interval allocated to paper")
        ], C_TEAL)
    ]

    cw6 = Inches(5.65)
    ch6 = Inches(2.4)

    positions = [
        (Inches(0.8), Inches(1.6)),
        (Inches(6.85), Inches(1.6)),
        (Inches(0.8), Inches(4.2)),
        (Inches(6.85), Inches(4.2))
    ]

    for idx, ((c_title, entities, col), (x, y)) in enumerate(zip(clusters, positions)):
        card = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, cw6, ch6)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = col
        card.line.width = Pt(1.5)

        chdr = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, cw6, Inches(0.45))
        chdr.fill.solid()
        chdr.fill.fore_color.rgb = col
        chdr.line.fill.background()
        tf_h = chdr.text_frame
        tf_h.margin_left = Inches(0.2)
        tf_h.margin_top = Inches(0.08)
        p = tf_h.paragraphs[0]
        p.text = c_title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_WHITE

        tb = slide6.shapes.add_textbox(x + Inches(0.18), y + Inches(0.5), cw6 - Inches(0.36), ch6 - Inches(0.55))
        tf_b = tb.text_frame
        tf_b.word_wrap = True
        for e_idx, (e_name, e_desc) in enumerate(entities):
            p = tf_b.paragraphs[0] if e_idx == 0 else tf_b.add_paragraph()
            p.space_after = Pt(2)
            r1 = p.add_run()
            r1.text = e_name + ": "
            r1.font.bold = True
            r1.font.size = Pt(10.5)
            r1.font.color.rgb = col
            r2 = p.add_run()
            r2.text = e_desc
            r2.font.size = Pt(10)
            r2.font.color.rgb = C_TEXT_DARK

    callout6 = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.75), Inches(11.733), Inches(0.35))
    callout6.fill.solid()
    callout6.fill.fore_color.rgb = RGBColor(241, 245, 249)
    callout6.line.fill.background()
    tf_c6 = callout6.text_frame
    tf_c6.margin_top = Inches(0.05)
    p = tf_c6.paragraphs[0]
    p.text = "✔ All 14 Principal Entities from university syllabus explicitly modeled with primary keys, foreign keys & relationships."
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_PRIMARY
    p.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 7: CONCEPTUAL ER DIAGRAM (Visual Flow)
    # ==========================================
    slide7 = add_blank_slide()
    add_header(slide7, "Conceptual ER Diagram: Relationship Architecture", "Entity Relationships & Cardinalities")
    add_footer(slide7, 7)

    # Visual ER Flow Boxes
    er_nodes = [
        # Col 1: Conferences & Structure
        ("Conferences", Inches(0.8), Inches(1.7), Inches(2.2), Inches(0.9), C_BLUE_PRIMARY),
        ("Tracks", Inches(0.8), Inches(3.2), Inches(2.2), Inches(0.9), C_BLUE_PRIMARY),
        ("Topics", Inches(0.8), Inches(4.7), Inches(2.2), Inches(0.9), C_BLUE_PRIMARY),
        
        # Col 2: Users, Authors, Papers
        ("Users", Inches(3.8), Inches(1.7), Inches(2.2), Inches(0.9), C_PURPLE),
        ("Authors", Inches(3.8), Inches(3.2), Inches(2.2), Inches(0.9), C_PURPLE),
        ("Papers", Inches(3.8), Inches(4.7), Inches(2.2), Inches(0.9), C_PURPLE),
        ("Versions", Inches(3.8), Inches(6.0), Inches(2.2), Inches(0.7), C_PURPLE),

        # Col 3: Review Engine
        ("Reviewers", Inches(6.8), Inches(1.7), Inches(2.2), Inches(0.9), C_AMBER),
        ("Conflicts", Inches(6.8), Inches(3.2), Inches(2.2), Inches(0.9), C_CORAL_RED),
        ("Assignments", Inches(6.8), Inches(4.7), Inches(2.2), Inches(0.9), C_AMBER),
        ("Reviews", Inches(6.8), Inches(6.0), Inches(2.2), Inches(0.7), C_AMBER),

        # Col 4: Decisions & Presentation
        ("Decisions", Inches(9.8), Inches(2.4), Inches(2.6), Inches(0.9), C_TEAL),
        ("Registrations", Inches(9.8), Inches(3.8), Inches(2.6), Inches(0.9), C_TEAL),
        ("Sessions", Inches(9.8), Inches(5.1), Inches(2.6), Inches(0.8), C_TEAL),
        ("Presentation Slots", Inches(9.8), Inches(6.1), Inches(2.6), Inches(0.7), C_TEAL)
    ]

    for name, nx, ny, nw, nh, ncol in er_nodes:
        box = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, nx, ny, nw, nh)
        box.fill.solid()
        box.fill.fore_color.rgb = C_CARD_BG
        box.line.color.rgb = ncol
        box.line.width = Pt(2)
        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = name
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = ncol
        p.alignment = PP_ALIGN.CENTER

    # Cardinality description panel
    desc_panel = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.9), Inches(2.5), Inches(1.0))
    desc_panel.fill.solid()
    desc_panel.fill.fore_color.rgb = RGBColor(238, 242, 255)
    desc_panel.line.color.rgb = C_BLUE_ACCENT
    tf_dp = desc_panel.text_frame
    tf_dp.margin_top = Inches(0.1)
    tf_dp.margin_left = Inches(0.15)
    p0 = tf_dp.paragraphs[0]
    p0.text = "KEY CARDINALITIES:"
    p0.font.bold = True
    p0.font.size = Pt(9.5)
    p0.font.color.rgb = C_BLUE_PRIMARY
    for c_text in ["• Conf 1:N Tracks 1:N Topics", "• Authors M:N Papers (Bridge)", "• Paper M:N Reviewer → 1:1 Review"]:
        p = tf_dp.add_paragraph()
        p.text = c_text
        p.font.size = Pt(8.5)
        p.font.color.rgb = C_TEXT_DARK

    # ==========================================
    # SLIDE 8: RELATIONAL SCHEMA SUMMARY (Clean Table)
    # ==========================================
    slide8 = add_blank_slide()
    add_header(slide8, "Initial Relational Schema: Tables & Key Constraints", "Relational Model Specifications")
    add_footer(slide8, 8)

    schema_headers = ["Table Name", "Primary Key", "Foreign Keys", "Key Enforced Constraints & Rules"]
    schema_data = [
        ["Conferences", "conference_id", "None", "UNIQUE(acronym, year), CHECK(end_date >= start_date)"],
        ["Tracks", "track_id", "conference_id", "UNIQUE(conference_id, track_name)"],
        ["Topics", "topic_id", "track_id", "UNIQUE(track_id, topic_name)"],
        ["Users", "user_id", "None", "UNIQUE(email), role IN ('CHAIR','AUTHOR','REVIEWER',...)"],
        ["Authors", "author_id", "user_id", "1:1 with Users; holds ORCID, bio"],
        ["Papers", "paper_id", "track_id, primary_author_id", "status IN ('SUBMITTED','UNDER_REVIEW','ACCEPTED','REJECTED')"],
        ["Paper_Authors", "(paper_id, author_id)", "paper_id, author_id", "UNIQUE(paper_id, author_order), author_order >= 1"],
        ["Paper_Versions", "version_id", "paper_id", "UNIQUE(paper_id, version_num), version_num >= 1"],
        ["Reviewers", "reviewer_id", "user_id", "1:1 with Users; max_workload > 0 (DEFAULT 5)"],
        ["Reviewer_Conflicts", "conflict_id", "reviewer_id, author_id", "UNIQUE(reviewer_id, author_id); bars biased assignments"],
        ["Paper_Assignments", "assignment_id", "paper_id, reviewer_id", "UNIQUE(paper_id, reviewer_id), status IN ('ASSIGNED','COMPLETED')"],
        ["Reviews", "review_id", "assignment_id (UNIQUE)", "CHECK scores BETWEEN 1 AND 10 for Originality, Soundness, Clarity"],
        ["Decisions", "decision_id", "paper_id (UNIQUE), chair_id", "decision_type IN ('ACCEPT','REJECT','REVISE')"],
        ["Presentation_Slots", "slot_id", "session_id, paper_id (UNIQUE)", "CHECK(end_time > start_time), zero author slot overlaps"]
    ]

    # Create table
    rows = len(schema_data) + 1
    cols = 4
    tbl_shape = slide8.shapes.add_table(rows, cols, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.2))
    tbl = tbl_shape.table
    col_widths = [Inches(2.0), Inches(1.8), Inches(2.6), Inches(5.333)]
    for c_idx, w in enumerate(col_widths):
        tbl.columns[c_idx].width = w

    # Header row
    for c_idx, h_text in enumerate(schema_headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_BLUE_PRIMARY
        tf = cell.text_frame
        tf.margin_left = Inches(0.12)
        p = tf.paragraphs[0]
        p.text = h_text
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_WHITE

    # Data rows
    for r_idx, row in enumerate(schema_data):
        bg = C_CARD_BG if (r_idx % 2 == 0) else RGBColor(241, 245, 249)
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            tf = cell.text_frame
            tf.margin_left = Inches(0.12)
            p = tf.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            if c_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_TEXT_DARK
            elif c_idx == 1:
                p.font.color.rgb = C_CORAL_RED
            elif c_idx == 2:
                p.font.color.rgb = C_BLUE_ACCENT
            else:
                p.font.color.rgb = C_TEXT_DARK

    # ==========================================
    # SLIDE 9: NORMALIZATION (1NF, 2NF, 3NF Made Simple)
    # ==========================================
    slide9 = add_blank_slide()
    add_header(slide9, "Normalization Strategy: 1NF → 2NF → 3NF", "Relational Normalization Proof")
    add_footer(slide9, 9)

    nw = Inches(3.7)
    nh = Inches(4.4)
    ny = Inches(1.6)

    # 1NF Card
    c_1nf = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), ny, nw, nh)
    c_1nf.fill.solid()
    c_1nf.fill.fore_color.rgb = C_CARD_BG
    c_1nf.line.color.rgb = C_BLUE_PRIMARY
    c_1nf.line.width = Pt(1.5)
    tf1 = c_1nf.text_frame
    tf1.word_wrap = True
    tf1.margin_left = Inches(0.2)
    tf1.margin_top = Inches(0.2)
    p = tf1.paragraphs[0]
    p.text = "1NF: ATOMIC VALUES"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_PRIMARY
    p.space_after = Pt(8)
    for title, desc in [
        ("Condition:", "All attributes contain atomic (indivisible) scalar values; no repeating groups or arrays."),
        ("Design Proof 1:", "Co-authors previously stored in CSV string decomposed into `Paper_Authors` table."),
        ("Design Proof 2:", "Multi-version files decomposed into `Paper_Versions` rather than arrays."),
        ("Result:", "Zero repeating groups; every attribute is strictly scalar.")
    ]:
        p = tf1.add_paragraph()
        p.space_after = Pt(6)
        r1 = p.add_run()
        r1.text = title + " "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = C_BLUE_PRIMARY
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = C_TEXT_DARK

    # 2NF Card
    c_2nf = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.88), ny, nw, nh)
    c_2nf.fill.solid()
    c_2nf.fill.fore_color.rgb = C_CARD_BG
    c_2nf.line.color.rgb = C_TEAL
    c_2nf.line.width = Pt(1.5)
    tf2 = c_2nf.text_frame
    tf2.word_wrap = True
    tf2.margin_left = Inches(0.2)
    tf2.margin_top = Inches(0.2)
    p = tf2.paragraphs[0]
    p.text = "2NF: NO PARTIAL KEYS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p.space_after = Pt(8)
    for title, desc in [
        ("Condition:", "1NF + no non-prime attribute depends on part of a composite primary key."),
        ("Design Proof 1:", "In `Paper_Authors(paper_id, author_id)`, `author_order` depends on BOTH keys."),
        ("Design Proof 2:", "Author names/bio are NOT in bridge table; they stay in `Authors` dependent on `author_id`."),
        ("Result:", "Zero partial key dependencies across all bridge entities.")
    ]:
        p = tf2.add_paragraph()
        p.space_after = Pt(6)
        r1 = p.add_run()
        r1.text = title + " "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = C_TEAL
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = C_TEXT_DARK

    # 3NF Card
    c_3nf = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.76), ny, nw, nh)
    c_3nf.fill.solid()
    c_3nf.fill.fore_color.rgb = C_CARD_BG
    c_3nf.line.color.rgb = C_AMBER
    c_3nf.line.width = Pt(1.5)
    tf3 = c_3nf.text_frame
    tf3.word_wrap = True
    tf3.margin_left = Inches(0.2)
    tf3.margin_top = Inches(0.2)
    p = tf3.paragraphs[0]
    p.text = "3NF: NO TRANSITIVE KEYS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p.space_after = Pt(8)
    for title, desc in [
        ("Condition:", "2NF + no transitive dependencies (X → Y where Y is non-prime)."),
        ("Design Proof 1:", "In `Papers`, track name is NOT stored; only `track_id` is referenced."),
        ("Design Proof 2:", "Authors and Reviewers link to `user_id`; personal data is never duplicated."),
        ("Result:", "Every non-key attribute depends ONLY on the Primary Key.")
    ]:
        p = tf3.add_paragraph()
        p.space_after = Pt(6)
        r1 = p.add_run()
        r1.text = title + " "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = C_AMBER
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = C_TEXT_DARK

    callout9 = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.25), Inches(11.733), Inches(0.65))
    callout9.fill.solid()
    callout9.fill.fore_color.rgb = RGBColor(238, 242, 255)
    callout9.line.color.rgb = C_BLUE_ACCENT
    tf_c9 = callout9.text_frame
    tf_c9.margin_left = Inches(0.25)
    tf_c9.margin_top = Inches(0.1)
    p = tf_c9.paragraphs[0]
    p.text = "✔ Anomaly Elimination: Insertion anomalies (tracks without papers), Deletion anomalies (papers deleted without losing authors), and Update anomalies (email updated in 1 row) are completely solved."
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_PRIMARY

    # ==========================================
    # SLIDE 10: 5 ESSENTIAL BUSINESS RULES ENFORCED
    # ==========================================
    slide10 = add_blank_slide()
    add_header(slide10, "Integrity Constraints & Business Rules Enforced", "System Business Logic")
    add_footer(slide10, 10)

    rules = [
        ("RULE 1: UNIQUE SUBMISSION IDENTIFIER",
         "Every manuscript receives an auto-increment Primary Key `paper_id` ensuring non-repeatable, immutable tracking across its lifecycle.",
         "Enforced via: PRIMARY KEY on Papers(paper_id)", C_BLUE_PRIMARY),
        ("RULE 2: STRICT CONFLICT OF INTEREST (COI) BAR",
         "No reviewer may evaluate a paper authored by their collaborator, advisor, or same-institution peer.",
         "Enforced via: UNIQUE(paper_id, reviewer_id) + BEFORE INSERT Trigger on Reviewer_Conflicts", C_CORAL_RED),
        ("RULE 3: MANDATORY REVIEW QUOTA THRESHOLD",
         "A paper cannot enter final decision evaluation until at least 3 completed peer reviews are submitted.",
         "Enforced via: BEFORE INSERT Trigger on Decisions validating review count ≥ 3", C_PURPLE),
        ("RULE 4: STANDARDIZED SCORE VALIDATION",
         "Reviewers must submit integer ratings strictly between 1 and 10 across all 4 evaluation criteria.",
         "Enforced via: Table CHECK (score BETWEEN 1 AND 10) on Reviews", C_AMBER),
        ("RULE 5: NON-OVERLAPPING PRESENTATION SLOTS",
         "An author cannot be scheduled to present in simultaneous time slots across different conference halls.",
         "Enforced via: UNIQUE(paper_id) + BEFORE INSERT Trigger checking room & author time overlap", C_TEAL)
    ]

    ry = Inches(1.6)
    rw = Inches(11.733)
    rh = Inches(0.9)

    for i, (rtitle, rdesc, rtech, rcol) in enumerate(rules):
        y = ry + i * Inches(1.0)
        card = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, rw, rh)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = rcol
        card.line.width = Pt(1.5)

        # Left stripe
        stripe = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(0.12), rh)
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = rcol
        stripe.line.fill.background()

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.3)
        tf.margin_top = Inches(0.1)

        p0 = tf.paragraphs[0]
        p0.text = "✔  " + rtitle
        p0.font.size = Pt(11.5)
        p0.font.bold = True
        p0.font.color.rgb = rcol

        p1 = tf.add_paragraph()
        r1 = p1.add_run()
        r1.text = rdesc + "  "
        r1.font.size = Pt(10)
        r1.font.color.rgb = C_TEXT_DARK
        r2 = p1.add_run()
        r2.text = "[" + rtech + "]"
        r2.font.size = Pt(9.5)
        r2.font.bold = True
        r2.font.color.rgb = C_TEXT_MUTED

    # ==========================================
    # SLIDE 11: SUMMARY & CONCLUSION (Dark Theme)
    # ==========================================
    slide11 = add_blank_slide(C_NAVY_DARK)

    top_bar11 = slide11.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.15))
    top_bar11.fill.solid()
    top_bar11.fill.fore_color.rgb = C_CYAN_ACCENT
    top_bar11.line.fill.background()

    tbox11 = slide11.shapes.add_textbox(Inches(1.0), Inches(1.0), Inches(11.333), Inches(1.5))
    tf11 = tbox11.text_frame
    tf11.word_wrap = True

    p0 = tf11.paragraphs[0]
    p0.text = "REVIEW 1 CONCLUSION"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = C_CYAN_ACCENT
    p0.space_after = Pt(6)

    p1 = tf11.add_paragraph()
    p1.text = "All Review 1 Milestones Successfully Formulated"
    p1.font.size = Pt(26)
    p1.font.bold = True
    p1.font.color.rgb = C_TEXT_WHITE

    # 3 Summary Cards
    sc_w = Inches(3.55)
    sc_h = Inches(3.3)
    sc_y = Inches(2.7)

    sc1 = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), sc_y, sc_w, sc_h)
    sc1.fill.solid()
    sc1.fill.fore_color.rgb = RGBColor(15, 34, 64)
    sc1.line.color.rgb = RGBColor(30, 58, 138)
    tf_sc1 = sc1.text_frame
    tf_sc1.word_wrap = True
    tf_sc1.margin_left = Inches(0.2)
    tf_sc1.margin_top = Inches(0.2)
    p = tf_sc1.paragraphs[0]
    p.text = "1. Deliverable 1 Complete"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT
    p.space_after = Pt(8)
    for b in [
        "Clear problem definition based on email failure points",
        "Demarcated in-scope vs out-of-scope boundaries",
        "Role-Based Access Control matrix for 6 user roles",
        "Detailed functional requirements for all 6 modules"
    ]:
        p = tf_sc1.add_paragraph()
        p.text = "✔  " + b
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_TEXT_LIGHT
        p.space_after = Pt(4)

    sc2 = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.88), sc_y, sc_w, sc_h)
    sc2.fill.solid()
    sc2.fill.fore_color.rgb = RGBColor(15, 34, 64)
    sc2.line.color.rgb = RGBColor(30, 58, 138)
    tf_sc2 = sc2.text_frame
    tf_sc2.word_wrap = True
    tf_sc2.margin_left = Inches(0.2)
    tf_sc2.margin_top = Inches(0.2)
    p = tf_sc2.paragraphs[0]
    p.text = "2. Deliverable 2 Complete"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT
    p.space_after = Pt(8)
    for b in [
        "All 14 principal entities explicitly cataloged",
        "Associative tables resolve M:N relationships",
        "Clear cardinalities (1:1, 1:N, M:N) mapped",
        "Conceptual ER Diagram fully structured"
    ]:
        p = tf_sc2.add_paragraph()
        p.text = "✔  " + b
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_TEXT_LIGHT
        p.space_after = Pt(4)

    sc3 = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.76), sc_y, sc_w, sc_h)
    sc3.fill.solid()
    sc3.fill.fore_color.rgb = RGBColor(15, 34, 64)
    sc3.line.color.rgb = RGBColor(30, 58, 138)
    tf_sc3 = sc3.text_frame
    tf_sc3.word_wrap = True
    tf_sc3.margin_left = Inches(0.2)
    tf_sc3.margin_top = Inches(0.2)
    p = tf_sc3.paragraphs[0]
    p.text = "3. Deliverable 3 Complete"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT
    p.space_after = Pt(8)
    for b in [
        "1NF, 2NF, and 3NF normalization mathematically proven",
        "Eliminated insertion, update & deletion anomalies",
        "PK, FK, UNIQUE, CHECK & triggers defined",
        "Executable schema.sql ready for immediate testing"
    ]:
        p = tf_sc3.add_paragraph()
        p.text = "✔  " + b
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_TEXT_LIGHT
        p.space_after = Pt(4)

    # Q&A Banner
    qbox = slide11.shapes.add_textbox(Inches(1.0), Inches(6.3), Inches(11.333), Inches(0.7))
    tf_q = qbox.text_frame
    p = tf_q.paragraphs[0]
    p.text = "Thank You! We are ready for your questions and feedback."
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT
    p.alignment = PP_ALIGN.CENTER

    output_path = "Academic_Conference_DBMS_Review1_Visual.pptx"
    prs.save(output_path)
    print(f"Clean visual 11-slide presentation successfully saved to: {output_path}")

if __name__ == "__main__":
    build_visual_presentation()
