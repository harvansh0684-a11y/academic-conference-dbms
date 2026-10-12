import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    # Palette
    C_NAVY_DARK = RGBColor(11, 25, 44)      # #0B192C
    C_NAVY_DEEP = RGBColor(15, 23, 42)      # #0F172A
    C_BLUE_PRIMARY = RGBColor(30, 58, 138)  # #1E3A8A
    C_BLUE_ACCENT = RGBColor(37, 99, 235)   # #2563EB
    C_CYAN_ACCENT = RGBColor(14, 165, 233)  # #0EA5E9
    C_TEAL = RGBColor(13, 148, 136)         # #0D9488
    C_AMBER = RGBColor(217, 119, 6)         # #D97706
    C_RED_ACCENT = RGBColor(225, 29, 72)    # #E11D48
    
    C_BG_LIGHT = RGBColor(248, 250, 252)    # #F8FAFC
    C_CARD_BG = RGBColor(255, 255, 255)     # #FFFFFF
    C_CARD_BORDER = RGBColor(226, 232, 240) # #E2E8F0
    
    C_TEXT_DARK = RGBColor(15, 23, 42)      # #0F172A
    C_TEXT_MUTED = RGBColor(71, 85, 105)    # #475569
    C_TEXT_LIGHT = RGBColor(241, 245, 249)  # #F1F5F9
    C_TEXT_WHITE = RGBColor(255, 255, 255)
    
    TOTAL_SLIDES = 18

    def add_blank_slide(bg_color=C_BG_LIGHT):
        slide = prs.slides.add_slide(blank_layout)
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = bg_color
        bg.line.fill.background()
        return slide

    def add_header(slide, title_text, category_text):
        hdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.35), Inches(11.733), Inches(0.95))
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = C_CARD_BG
        hdr.line.color.rgb = C_CARD_BORDER
        hdr.line.width = Pt(1)

        stripe = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.35), Inches(0.12), Inches(0.95))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = C_BLUE_ACCENT
        stripe.line.fill.background()

        tf = hdr.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.35)
        tf.margin_top = Inches(0.12)
        tf.margin_bottom = Inches(0.1)

        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = Pt(9.5)
        p0.font.bold = True
        p0.font.color.rgb = C_BLUE_ACCENT

        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(19)
        p1.font.bold = True
        p1.font.color.rgb = C_TEXT_DARK

    def add_footer(slide, slide_num):
        box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.35))
        tf = box.text_frame
        p = tf.paragraphs[0]
        p.text = f"DBMS Course Project: Conference Submission & Review System  |  Review 1 (Week 7)  |  Slide {slide_num} of {TOTAL_SLIDES}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = C_TEXT_MUTED

    def add_card(slide, left, top, width, height, title, items, header_bg=C_BLUE_PRIMARY, tag=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_CARD_BORDER
        card.line.width = Pt(1)

        hdr_h = Inches(0.48)
        card_hdr = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, hdr_h)
        card_hdr.fill.solid()
        card_hdr.fill.fore_color.rgb = header_bg
        card_hdr.line.fill.background()

        tf_h = card_hdr.text_frame
        tf_h.margin_left = Inches(0.2)
        tf_h.margin_top = Inches(0.08)
        p_h = tf_h.paragraphs[0]
        p_h.text = title
        p_h.font.size = Pt(12)
        p_h.font.bold = True
        p_h.font.color.rgb = C_TEXT_WHITE

        if tag:
            p_tag = tf_h.add_paragraph()
            p_tag.text = tag
            p_tag.font.size = Pt(8)
            p_tag.font.color.rgb = C_CYAN_ACCENT

        tb = slide.shapes.add_textbox(left + Inches(0.15), top + hdr_h + Inches(0.08), width - Inches(0.3), height - hdr_h - Inches(0.15))
        tf_b = tb.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = 0
        tf_b.margin_top = 0
        tf_b.margin_right = 0
        tf_b.margin_bottom = 0

        first = True
        for item in items:
            if first:
                p = tf_b.paragraphs[0]
                first = False
            else:
                p = tf_b.add_paragraph()
            
            p.font.size = Pt(10)
            p.font.color.rgb = C_TEXT_DARK
            p.space_after = Pt(4)

            if isinstance(item, tuple):
                bold_part, reg_part = item
                r_bold = p.add_run()
                r_bold.text = bold_part + " "
                r_bold.font.bold = True
                r_bold.font.color.rgb = C_TEXT_DARK
                r_reg = p.add_run()
                r_reg.text = reg_part
                r_reg.font.bold = False
                r_reg.font.color.rgb = C_TEXT_MUTED
            else:
                p.text = "• " + item

    def add_callout(slide, left, top, width, height, title, text, bg_color=RGBColor(238, 242, 255), border_color=C_BLUE_ACCENT):
        callout = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        callout.fill.solid()
        callout.fill.fore_color.rgb = bg_color
        callout.line.color.rgb = border_color
        callout.line.width = Pt(1.5)

        tf = callout.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.12)
        tf.margin_right = Inches(0.2)
        tf.margin_bottom = Inches(0.1)

        p0 = tf.paragraphs[0]
        p0.text = "⚡ " + title
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = border_color
        p0.space_after = Pt(2)

        p1 = tf.add_paragraph()
        p1.text = text
        p1.font.size = Pt(9.5)
        p1.font.color.rgb = C_TEXT_DARK

    def create_styled_table(slide, left, top, width, height, headers, data, col_widths=None):
        rows = len(data) + 1
        cols = len(headers)
        table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
        table = table_shape.table

        if col_widths and len(col_widths) == cols:
            for c_idx, w in enumerate(col_widths):
                table.columns[c_idx].width = w

        for c_idx, h_text in enumerate(headers):
            cell = table.cell(0, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_BLUE_PRIMARY
            tf = cell.text_frame
            tf.word_wrap = True
            tf.margin_left = Inches(0.1)
            tf.margin_right = Inches(0.1)
            p = tf.paragraphs[0]
            p.text = h_text
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = C_TEXT_WHITE
            p.alignment = PP_ALIGN.CENTER

        for r_idx, row_data in enumerate(data):
            row_num = r_idx + 1
            bg_c = C_CARD_BG if (r_idx % 2 == 0) else RGBColor(241, 245, 249)
            for c_idx, val in enumerate(row_data):
                cell = table.cell(row_num, c_idx)
                cell.fill.solid()
                cell.fill.fore_color.rgb = bg_c
                tf = cell.text_frame
                tf.word_wrap = True
                tf.margin_left = Inches(0.1)
                tf.margin_right = Inches(0.1)
                p = tf.paragraphs[0]
                p.text = str(val)
                p.font.size = Pt(9)
                p.font.color.rgb = C_TEXT_DARK

    # ==========================================
    # SLIDE 1: TITLE SLIDE (Dark Navy Theme)
    # ==========================================
    slide1 = add_blank_slide(C_NAVY_DARK)
    accent_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.15))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = C_CYAN_ACCENT
    accent_bar.line.fill.background()

    title_box = slide1.shapes.add_textbox(Inches(1.0), Inches(1.1), Inches(11.333), Inches(2.4))
    tf1 = title_box.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "DATABASE MANAGEMENT SYSTEMS PROJECT  |  REVIEW 1 (WEEK 7 - 5 MARKS)"
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = C_CYAN_ACCENT
    p0.space_after = Pt(8)

    p1 = tf1.add_paragraph()
    p1.text = "Design & Implementation of a DBMS for Academic Conference Paper Submission & Review System"
    p1.font.size = Pt(25)
    p1.font.bold = True
    p1.font.color.rgb = C_TEXT_WHITE
    p1.space_after = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "Problem Formulation  •  14 Principal Entities  •  Conceptual ER Model  •  3NF Relational Schema"
    p2.font.size = Pt(13)
    p2.font.color.rgb = RGBColor(148, 163, 184)

    c_w = Inches(3.5)
    c_h = Inches(2.5)
    y_pos = Inches(3.8)

    card1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), y_pos, c_w, c_h)
    card1.fill.solid()
    card1.fill.fore_color.rgb = RGBColor(15, 34, 64)
    card1.line.color.rgb = RGBColor(30, 58, 138)
    tf_c1 = card1.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_left = Inches(0.25)
    tf_c1.margin_top = Inches(0.2)
    p = tf_c1.paragraphs[0]
    p.text = "🎯 REVIEW 1 DELIVERABLES"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT
    p.space_after = Pt(6)
    for bullet in [
        "Problem Identification & Objectives",
        "User Roles & Functional Requirements",
        "Conceptual Design (ER Model)",
        "14 Principal Entities & Cardinality",
        "Initial Relational Schema in 3NF"
    ]:
        p = tf_c1.add_paragraph()
        p.text = "✔ " + bullet
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_TEXT_LIGHT
        p.space_after = Pt(3)

    card2 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.9), y_pos, c_w, c_h)
    card2.fill.solid()
    card2.fill.fore_color.rgb = RGBColor(15, 34, 64)
    card2.line.color.rgb = RGBColor(30, 58, 138)
    tf_c2 = card2.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_left = Inches(0.25)
    tf_c2.margin_top = Inches(0.2)
    p = tf_c2.paragraphs[0]
    p.text = "⚙ SYSTEM ARCHITECTURE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT
    p.space_after = Pt(6)
    for bullet in [
        "Target DBMS: PostgreSQL / MySQL",
        "Normalization: Up to Third Normal Form (3NF)",
        "Integrity: PK, FK, UNIQUE, CHECK, NOT NULL",
        "Enforcement: COI Prevention, Review Quotas",
        "Front-End: Python / Java (Review 2/3)"
    ]:
        p = tf_c2.add_paragraph()
        p.text = "⚡ " + bullet
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_TEXT_LIGHT
        p.space_after = Pt(3)

    card3 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), y_pos, c_w, c_h)
    card3.fill.solid()
    card3.fill.fore_color.rgb = RGBColor(15, 34, 64)
    card3.line.color.rgb = RGBColor(30, 58, 138)
    tf_c3 = card3.text_frame
    tf_c3.word_wrap = True
    tf_c3.margin_left = Inches(0.25)
    tf_c3.margin_top = Inches(0.2)
    p = tf_c3.paragraphs[0]
    p.text = "👥 PROJECT METADATA"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT
    p.space_after = Pt(6)
    for bullet in [
        "Course: Database Management Systems",
        "Evaluation: Review 1 - Week 7",
        "Weightage: 5 Marks",
        "Presenter: [Student Name / Team]",
        "Register No / Roll No: [Roll Number]",
        "Academic Year: 2026 - 2027"
    ]:
        p = tf_c3.add_paragraph()
        p.text = "• " + bullet
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_TEXT_LIGHT
        p.space_after = Pt(2)

    footer_t1 = slide1.shapes.add_textbox(Inches(1.0), Inches(6.8), Inches(11.333), Inches(0.4))
    tf_f1 = footer_t1.text_frame
    p = tf_f1.paragraphs[0]
    p.text = "DBMS Engineering Project  |  Department of Computer Science & Engineering"
    p.font.size = Pt(8.5)
    p.font.color.rgb = RGBColor(100, 116, 139)

    # ==========================================
    # SLIDE 2: PROJECT OVERVIEW & BACKGROUND
    # ==========================================
    slide2 = add_blank_slide()
    add_header(slide2, "Project Overview & Academic Context", "Deliverable 1: Context & Problem Identification")
    add_footer(slide2, 2)

    add_card(slide2, Inches(0.8), Inches(1.5), Inches(5.6), Inches(4.3), "The Academic Conference Ecosystem", [
        ("High-Stakes Peer Review:", "Conferences receive hundreds of technical papers across multidisciplinary tracks requiring rigorous blind evaluation."),
        ("Multi-Stage Lifecycle:", "Papers traverse sequential phases: Initial Submission → Blind Screening → Reviewer Assignment → Peer Scoring → Program Committee Decision → Camera-Ready Resubmission → Registration & Presentation Scheduling."),
        ("Complex Constraints:", "Demands strict isolation between authors and reviewers, expertise alignment, quota balancing, and zero-conflict presentation slot generation."),
        ("Core Need:", "A formal, high-integrity relational database management system capable of replacing error-prone manual spreadsheets and emails.")
    ], C_BLUE_PRIMARY)

    add_card(slide2, Inches(6.8), Inches(1.5), Inches(5.7), Inches(4.3), "System Vision & Core Value Proposition", [
        ("Single Source of Truth:", "Centralized relational repository capturing conferences, tracks, papers, versions, reviews, decisions, and session timetables."),
        ("Automated Compliance:", "Programmatic enforcement of review fairness—preventing co-authors and institutional colleagues from evaluating each other's research."),
        ("Immutable Version History:", "Decoupling submissions into master papers and discrete versions to preserve camera-ready integrity and auditability."),
        ("End-to-End Governance:", "Equipping Program Chairs with live visibility into pending reviews, reviewer workloads, score distributions, and hall scheduling.")
    ], C_TEAL)

    add_callout(slide2, Inches(0.8), Inches(6.0), Inches(11.7), Inches(0.85),
                "Key Engineering Takeaway for Review 1",
                "Review 1 establishes the mathematical and structural bedrock of the system: defining the 14 core entities, formalizing constraints, resolving M:N relationships through associative tables, and guaranteeing 3NF normalization.")

    # ==========================================
    # SLIDE 3: PROBLEM IDENTIFICATION (5 CRITICAL FAILURES)
    # ==========================================
    slide3 = add_blank_slide()
    add_header(slide3, "Problem Identification: Failures in Email/Manual Workflows", "Deliverable 1: Problem Identification")
    add_footer(slide3, 3)

    col_w = Inches(3.65)
    h_top = Inches(2.3)

    add_card(slide3, Inches(0.8), Inches(1.5), col_w, h_top, "1. Version Loss & Overwrite", [
        ("Email Attachment Chaos:", "Authors submit updated manuscripts via email; reviewers evaluate outdated drafts."),
        ("Camera-Ready Confusion:", "Chairs struggle to determine which PDF represents the final verified camera-ready copy."),
        ("Anonymity Leaks:", "Uncontrolled file transfers leak author metadata in double-blind conferences.")
    ], C_RED_ACCENT)

    add_card(slide3, Inches(4.8), Inches(1.5), col_w, h_top, "2. Conflict of Interest (COI) Bias", [
        ("Unchecked Assignments:", "Reviewers assigned papers authored by current collaborators, advisors, or same-institution peers."),
        ("Ethical Compromise:", "Lack of automated COI detection leads to biased scoring, inflated ratings, or sabotaged reviews."),
        ("Reputational Risk:", "Conference integrity compromised by subjective, non-blinded assignments.")
    ], C_RED_ACCENT)

    add_card(slide3, Inches(8.8), Inches(1.5), col_w, h_top, "3. Workload Imbalance & Bottlenecks", [
        ("Reviewer Overload:", "Certain reviewers receive 10+ papers while others receive zero, causing reviewer fatigue."),
        ("Pending Review Blackholes:", "No automated alerts or tracking for overdue evaluations, delaying decisions."),
        ("Insufficient Reviews:", "Papers end up with <3 reviews, resulting in statistically invalid decisions.")
    ], C_RED_ACCENT)

    h_bot = Inches(2.0)
    y_bot = Inches(4.0)

    add_card(slide3, Inches(0.8), y_bot, Inches(5.6), h_bot, "4. Fragmented Scoring & Opaque Decisions", [
        ("Inconsistent Rubrics:", "Reviewers submit unstructured comments without standard criteria (originality, soundness, clarity)."),
        ("Chair Deliberation Gaps:", "Chairs cannot aggregate scores, view standard deviations, or separate confidential chair notes from author feedback.")
    ], C_NAVY_DEEP)

    add_card(slide3, Inches(6.8), y_bot, Inches(5.7), h_bot, "5. Presentation Slot Clashes & Scheduling Chaos", [
        ("Double-Booked Authors:", "Authors with multiple accepted papers scheduled in overlapping time slots across different halls."),
        ("Unregistered Presentations:", "Papers scheduled whose authors have not registered, leading to empty conference slots.")
    ], C_NAVY_DEEP)

    add_callout(slide3, Inches(0.8), Inches(6.15), Inches(11.7), Inches(0.75),
                "Database Remedy",
                "Our relational schema resolves all 5 failures via composite UNIQUE keys, CHECK constraints, multi-version tables, foreign key cascades, and COI verification rules.")

    # ==========================================
    # SLIDE 4: PROJECT SCOPE & BOUNDARIES
    # ==========================================
    slide4 = add_blank_slide()
    add_header(slide4, "Project Scope: Functional Boundaries & Delimitation", "Deliverable 1: Scope Definition")
    add_footer(slide4, 4)

    add_card(slide4, Inches(0.8), Inches(1.5), Inches(5.6), Inches(4.4), "IN-SCOPE: Core DBMS Modules", [
        ("Multi-Track Conference Configuration:", "Hosting conferences with tracks, topic taxonomies, and strict key deadlines."),
        ("Multi-Author & Multi-Version Lifecycle:", "Full audit trail of manuscript drafts, revisions, and camera-ready uploads with co-author order."),
        ("Expertise & Conflict Management:", "Reviewer topic ratings and explicit author-reviewer conflict matrices."),
        ("Constrained Reviewer Assignment Engine:", "Quota enforcement (max papers per reviewer), topic matching, and strict COI barring."),
        ("Multi-Criteria Scoring & Chair Decisions:", "Granular scores (1-10) for originality, soundness, clarity + confidential chair remarks."),
        ("Author Registration & Slot Scheduling:", "Verification of paid registration before assigning conflict-free hall & session slots."),
        ("Comprehensive Analytical Views:", "SQL queries for reviewer workloads, track acceptance rates, and full conference timetables.")
    ], C_TEAL)

    add_card(slide4, Inches(6.8), Inches(1.5), Inches(5.7), Inches(4.4), "OUT-OF-SCOPE (Delimitations)", [
        ("Live Banking Payment Gateway:", "Monetary transactions are simulated via payment transaction reference IDs, timestamp, and status ('PAID', 'PENDING', 'WAIVED')."),
        ("Full-Text NLP Plagiarism Engine:", "Automated manuscript similarity indexing is handled by external tools (Turnitin/iThenticate); our DBMS stores similarity index percentages."),
        ("Live Video Streaming / Virtual Conferencing:", "DBMS manages physical room numbers and meeting URLs, but does not host real-time WebRTC streams."),
        ("Multi-Conference Multi-Tenancy:", "Optimized for single/multi-track academic conferences with scalable schema support.")
    ], C_AMBER)

    add_callout(slide4, Inches(0.8), Inches(6.05), Inches(11.7), Inches(0.8),
                "Scope Feasibility",
                "The defined scope directly addresses all 14 principal entities and business rules specified in the project guidelines, ensuring full compliance for Review 1, 2, and 3.")

    # ==========================================
    # SLIDE 5: PROJECT OBJECTIVES (SMART GOALS)
    # ==========================================
    slide5 = add_blank_slide()
    add_header(slide5, "Project Objectives: Engineering Pillars", "Deliverable 1: Objectives")
    add_footer(slide5, 5)

    o_w = Inches(2.75)
    o_h = Inches(4.3)

    add_card(slide5, Inches(0.8), Inches(1.5), o_w, o_h, "1. Normalization & Integrity", [
        ("Goal:", "Develop a relational schema in Third Normal Form (3NF)."),
        ("Eliminate Anomalies:", "Prevent insertion, deletion, and update anomalies across submissions and reviews."),
        ("Referential Rigor:", "Enforce foreign keys, ON DELETE RESTRICT on audit trails, and strict domain CHECK constraints.")
    ], C_BLUE_PRIMARY)

    add_card(slide5, Inches(3.8), Inches(1.5), o_w, o_h, "2. Ethical Peer Review", [
        ("Goal:", "Enforce double-blind integrity and zero conflict of interest."),
        ("Automated Barring:", "Reviewers cannot be assigned papers where an explicit or institutional conflict exists."),
        ("Blind Metadata:", "Logical isolation of author identity from reviewers during evaluation.")
    ], C_TEAL)

    add_card(slide5, Inches(6.8), Inches(1.5), o_w, o_h, "3. Version & Decision Trace", [
        ("Goal:", "Provide an immutable audit trail for paper evolution."),
        ("Version Tracking:", "Distinguish between initial review submissions and final camera-ready manuscripts."),
        ("Chair Decision Log:", "Record chair identity, rationale, score summaries, and timestamps.")
    ], C_AMBER)

    add_card(slide5, Inches(9.8), Inches(1.5), o_w, o_h, "4. Conflict-Free Timetable", [
        ("Goal:", "Automate presentation slot allocation without collisions."),
        ("Constraint Checking:", "Prevent room double-booking and ensure no author is scheduled in simultaneous sessions."),
        ("Prerequisite:", "Only registered authors with accepted papers are allocated presentation slots.")
    ], C_BLUE_ACCENT)

    add_callout(slide5, Inches(0.8), Inches(6.0), Inches(11.7), Inches(0.85),
                "Alignment with Evaluation Rubric",
                "These objectives establish measurable benchmarks for Review 1 (schema & conceptual model), Review 2 (queries, views, normalization), and Review 3 (UI, transactions, and live demo).")

    # ==========================================
    # SLIDE 6: USER ROLES & PRIVILEGE MATRIX
    # ==========================================
    slide6 = add_blank_slide()
    add_header(slide6, "User Roles & Access Privilege Matrix", "Deliverable 1: Stakeholders & Roles")
    add_footer(slide6, 6)

    role_headers = ["User Role", "Primary Responsibilities", "System Privileges & Permissions", "Constraints & Restrictions"]
    role_data = [
        ["Program Chair", "Overall conference governance, track management, final acceptance/rejection decisions", "Full CRUD on tracks, paper decisions, session timetable generation, reviewer reassignments", "Cannot alter submitted reviewer scores directly; decisions must cite review basis."],
        ["Track Chair", "Supervises topic-specific tracks (e.g., AI/ML, Networks, Security)", "Assigns reviewers within track, monitors pending reviews, recommends decisions to Program Chair", "Restricted to papers and reviewers within their assigned track_id."],
        ["Author", "Submits research papers, co-author details, revisions, and camera-ready copies", "Creates paper submissions, uploads versions, views finalized review feedback, registers for conference", "Cannot view reviewer identities (Double-Blind); cannot edit papers past submission deadline."],
        ["Reviewer", "Evaluates assigned papers, declares expertise and conflicts of interest", "Sets expertise levels, submits multi-criteria scores (1-10) and qualitative comments", "Cannot review papers with declared COI; cannot view co-reviewers' scores until submission."],
        ["Attendee / Presenter", "Participates in conference sessions, delivers presentations", "Views published accepted papers, accesses schedule, completes registration payment", "Cannot access submission, review, or decision management back-end."],
        ["System Administrator", "Database maintenance, user account provisioning, system backups", "Manages user credentials, database indexes, transaction log audits, table archiving", "Separated from editorial decisions; cannot alter scientific review scores."]
    ]

    create_styled_table(slide6, Inches(0.8), Inches(1.5), Inches(11.733), Inches(4.3),
                        role_headers, role_data,
                        [Inches(1.8), Inches(3.4), Inches(3.8), Inches(2.733)])

    add_callout(slide6, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.8),
                "Architectural Implementation: Role-Based Access Control (RBAC)",
                "Implemented via a unified 'Users' entity linked to specialized role profiles ('Authors', 'Reviewers', 'Chairs') avoiding data duplication while ensuring strict role-based data segregation.")

    # ==========================================
    # SLIDE 7: FUNCTIONAL REQUIREMENTS BREAKDOWN
    # ==========================================
    slide7 = add_blank_slide()
    add_header(slide7, "Functional Requirements: 6 Core Modules", "Deliverable 1: Functional Specifications")
    add_footer(slide7, 7)

    f_w = Inches(3.7)
    f_h = Inches(2.2)

    add_card(slide7, Inches(0.8), Inches(1.5), f_w, f_h, "FR1: Submission & Versioning", [
        ("Paper Registration:", "Unique paper ID, title, abstract, track, primary & co-authors."),
        ("Multi-Version Store:", "Upload discrete versions (V1, V2, Camera-ready) with timestamp and changelog."),
        ("Blind Manuscript:", "Store blinded PDF filepath without author names.")
    ], C_BLUE_PRIMARY)

    add_card(slide7, Inches(4.8), Inches(1.5), f_w, f_h, "FR2: Expertise & Conflict Profiling", [
        ("Topic Expertise:", "Reviewers classify expertise per topic (Expert, Knowledgeable, Informed)."),
        ("Conflict Declaration:", "Explicit declaration of co-author, institutional, or personal conflicts."),
        ("Automated Matching:", "System pairs papers with matching high-expertise reviewers.")
    ], C_BLUE_PRIMARY)

    add_card(slide7, Inches(8.8), Inches(1.5), f_w, f_h, "FR3: Assignment Engine", [
        ("Workload Quota:", "Reviewers cannot exceed defined paper capacity (e.g., max 5)."),
        ("Review Threshold:", "Enforce required minimum review count (default: 3 reviews per paper)."),
        ("Zero COI:", "Hard block on assigning any reviewer with a declared conflict.")
    ], C_BLUE_PRIMARY)

    add_card(slide7, Inches(0.8), Inches(3.85), f_w, f_h, "FR4: Review Scoring & Feedback", [
        ("Multi-Criteria Scores:", "Numerical evaluation [1-10] for Originality, Technical Soundness, and Clarity."),
        ("Overall Recommendation:", "Strong Accept, Weak Accept, Borderline, Reject."),
        ("Dual Feedback:", "Public constructive comments to author + Private remarks to Chair.")
    ], C_TEAL)

    add_card(slide7, Inches(4.8), Inches(3.85), f_w, f_h, "FR5: Decision Management", [
        ("Formal Verdict:", "Program Chair records Accept, Reject, Major Revision, or Minor Revision."),
        ("Decision Notification:", "Automated status update with aggregated review feedback."),
        ("Camera-Ready Flag:", "Triggers final camera-ready version upload for accepted papers.")
    ], C_TEAL)

    add_card(slide7, Inches(8.8), Inches(3.85), f_w, f_h, "FR6: Registration & Scheduling", [
        ("Author Registration:", "Validates registration and fee payment for at least one author per paper."),
        ("Session Allocation:", "Assigns accepted papers to thematic conference tracks & halls."),
        ("Overlap Prevention:", "Validates that authors and rooms have zero overlapping time slots.")
    ], C_TEAL)

    add_callout(slide7, Inches(0.8), Inches(6.15), Inches(11.7), Inches(0.75),
                "Module Synergy",
                "These 6 modules form an unbroken pipeline where output of one stage (e.g., Decisions) strictly gates the next stage (e.g., Registration & Presentation Scheduling).")

    # ==========================================
    # SLIDE 8: NON-FUNCTIONAL REQUIREMENTS & BUSINESS RULES
    # ==========================================
    slide8 = add_blank_slide()
    add_header(slide8, "Non-Functional Requirements & Core Business Rules", "Deliverable 1: System Constraints")
    add_footer(slide8, 8)

    add_card(slide8, Inches(0.8), Inches(1.5), Inches(5.6), Inches(4.3), "Non-Functional Requirements (NFR)", [
        ("Data Integrity & ACID:", "Foreign key cascades, atomic transactions for multi-reviewer assignments, and rollback on assignment failures."),
        ("Double-Blind Security:", "Database views hide author identities from reviewers and reviewer identities from authors during review phase."),
        ("Performance & Indexing:", "B-Tree indexes on frequently filtered fields (track_id, status, reviewer_id, submission_date) to optimize queries."),
        ("Scalability:", "Normalized schema capable of handling 1,000+ papers, 3,000+ reviews, and 50+ concurrent sessions."),
        ("Auditability:", "Audit columns (created_at, updated_at, decision_by) on all operational tables.")
    ], C_NAVY_DEEP)

    add_card(slide8, Inches(6.8), Inches(1.5), Inches(5.7), Inches(4.3), "Enforced Business Rules (BR)", [
        ("BR1: Unique Submission Identifier:", "Every paper has an immutable system-generated Primary Key `paper_id`."),
        ("BR2: Strict Conflict of Interest Bar:", "A reviewer cannot be assigned a paper if an entry exists in `Reviewer_Conflicts` for any co-author."),
        ("BR3: Mandatory Review Quota:", "A paper cannot enter Decision state until at least 3 valid reviews are submitted."),
        ("BR4: Valid Score Ranges:", "CHECK constraints enforce integer scores between 1 and 10 for all evaluation criteria."),
        ("BR5: Non-Overlapping Author Schedules:", "An author cannot have two papers scheduled in presentation slots that overlap in date and time.")
    ], C_AMBER)

    add_callout(slide8, Inches(0.8), Inches(6.0), Inches(11.7), Inches(0.85),
                "Faculty Review Expectation",
                "Reviewers test whether business rules are merely theoretical or encoded in the schema. In our system, BR1-BR4 are enforced via DDL constraints, while BR2 and BR5 are secured via triggers.")

    # ==========================================
    # SLIDE 9: CONCEPTUAL DESIGN - THE 14 PRINCIPAL ENTITIES
    # ==========================================
    slide9 = add_blank_slide()
    add_header(slide9, "Conceptual Design: The 14 Principal Entities", "Deliverable 2: Conceptual Design")
    add_footer(slide9, 9)

    e_headers = ["#", "Entity Name", "Primary Key", "Core Attributes", "Role in Conference Lifecycle"]
    e_data = [
        ["1", "Conference", "conference_id", "title, acronym, year, start_date, end_date, location, submission_deadline", "Root entity defining event metadata and timeline."],
        ["2", "Track", "track_id", "conference_id (FK), track_name, description", "Divides conference into thematic areas (AI, Security, Systems)."],
        ["3", "Topic", "topic_id", "track_id (FK), topic_name, keywords", "Granular scientific keywords used for reviewer expertise matching."],
        ["4", "Author", "author_id", "user_id (FK), affiliation, country, bio", "Profile of researcher submitting manuscripts."],
        ["5", "Paper", "paper_id", "track_id (FK), primary_author_id (FK), title, abstract, status", "Master submission record tracking lifecycle state."],
        ["6", "Version", "version_id", "paper_id (FK), version_no, file_path, upload_date, is_camera_ready", "Maintains file revisions (drafts, revisions, camera-ready)."],
        ["7", "Reviewer", "reviewer_id", "user_id (FK), max_workload, is_active", "Peer reviewer profile with capacity limits."],
        ["8", "Expertise", "(reviewer_id, topic_id)", "expertise_level (Expert, Knowledgeable, Informed)", "M:N link mapping reviewer competence to topics."],
        ["9", "Conflict", "conflict_id", "reviewer_id (FK), author_id (FK), conflict_type, declared_at", "Explicit conflict declaration barring biased assignments."],
        ["10", "Assignment", "assignment_id", "paper_id (FK), reviewer_id (FK), assigned_date, due_date, status", "M:N link dispatching a paper to an eligible reviewer."],
        ["11", "Review", "review_id", "assignment_id (FK), originality, soundness, clarity, overall_score", "Evaluation scores [1-10] and qualitative feedback."],
        ["12", "Decision", "decision_id", "paper_id (FK), chair_id (FK), decision_type, decision_date", "Chair's final verdict (Accept, Reject, Revise)."],
        ["13", "Registration", "registration_id", "conference_id (FK), user_id (FK), paper_id (FK), payment_status", "Author/attendee registration and fee tracking."],
        ["14", "Presentation_Slot", "slot_id", "session_id (FK), paper_id (FK), start_time, end_time, room_no", "Final timetable slot allocated to accepted papers."]
    ]

    create_styled_table(slide9, Inches(0.8), Inches(1.5), Inches(11.733), Inches(4.35),
                        e_headers, e_data,
                        [Inches(0.5), Inches(1.8), Inches(1.8), Inches(4.5), Inches(3.133)])

    add_callout(slide9, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.8),
                "Complete Deliverable Alignment",
                "All 14 entities specified in the university problem statement are explicitly defined with primary keys, foreign references, and distinct lifecycle duties.")

    # ==========================================
    # SLIDE 10: ER ARCHITECTURE & CARDINALITY MAPPING
    # ==========================================
    slide10 = add_blank_slide()
    add_header(slide10, "ER Architecture & Cardinality Mapping", "Deliverable 2: Entity Relationships")
    add_footer(slide10, 10)

    card_headers = ["Relationship Name", "Entity 1", "Cardinality", "Entity 2", "Associative Entity / Foreign Key", "Business Integrity Rule"]
    card_data = [
        ["Conference_Has_Tracks", "Conference", "1 : N", "Track", "Track.conference_id", "Every track belongs to exactly 1 conference; cascade on delete."],
        ["Track_Has_Topics", "Track", "1 : N", "Topic", "Topic.track_id", "Topics categorize papers and reviewer expertise."],
        ["Paper_Authored_By", "Paper", "M : N", "Author", "Paper_Author (paper_id, author_id)", "Papers can have multiple authors; authors can write multiple papers."],
        ["Paper_Has_Versions", "Paper", "1 : N", "Version", "Paper_Version.paper_id", "A paper has 1 or more versions; version_no incremented."],
        ["Reviewer_Topic_Expertise", "Reviewer", "M : N", "Topic", "Reviewer_Expertise (reviewer_id, topic_id)", "Captures rating: Expert, Knowledgeable, or Informed."],
        ["Reviewer_Author_Conflict", "Reviewer", "M : N", "Author", "Reviewer_Conflict (reviewer_id, author_id)", "Bars reviewer from any paper written by this author."],
        ["Paper_Assigned_To_Reviewer", "Paper", "M : N", "Reviewer", "Paper_Assignment (paper_id, reviewer_id)", "Enforces max capacity & zero conflict; target 3 per paper."],
        ["Assignment_Has_Review", "Assignment", "1 : 1", "Review", "Review.assignment_id (UNIQUE)", "Each completed assignment produces exactly one formal review."],
        ["Paper_Has_Decision", "Paper", "1 : 1", "Decision", "Decision.paper_id (UNIQUE)", "Each evaluated paper receives exactly one official chair verdict."],
        ["Session_Has_Slots", "Session", "1 : N", "Presentation_Slot", "Presentation_Slot.session_id", "Sessions group slots by theme, date, and conference room."],
        ["Paper_Presentation_Slot", "Paper", "1 : 1", "Presentation_Slot", "Presentation_Slot.paper_id (UNIQUE)", "Accepted papers get at most 1 presentation slot; no overlaps."]
    ]

    create_styled_table(slide10, Inches(0.8), Inches(1.5), Inches(11.733), Inches(4.35),
                        card_headers, card_data,
                        [Inches(2.2), Inches(1.4), Inches(1.0), Inches(1.5), Inches(2.8), Inches(2.833)])

    add_callout(slide10, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.8),
                "Key Relational Bridge",
                "Many-to-Many relationships (`Author-Paper`, `Reviewer-Topic`, `Reviewer-Author`, `Paper-Reviewer`) are resolved into composite-key bridge entities, eliminating redundancy.")

    # ==========================================
    # SLIDE 11: CONCEPTUAL ER DIAGRAM (VISUAL FLOW)
    # ==========================================
    slide11 = add_blank_slide()
    add_header(slide11, "Conceptual ER Diagram: Architectural Blueprint", "Deliverable 2: ER Diagram")
    add_footer(slide11, 11)

    cl_w = Inches(5.6)
    cl_h = Inches(2.1)

    add_card(slide11, Inches(0.8), Inches(1.5), cl_w, cl_h, "Cluster A: Conference & Track Setup", [
        ("CONFERENCE (1)", "──< TRACK (N) ──< TOPIC (N)"),
        ("Hierarchy:", "A conference contains multiple tracks; each track hosts distinct topic keywords."),
        ("Key Entities:", "Conference, Track, Topic, Session.")
    ], C_BLUE_PRIMARY)

    add_card(slide11, Inches(6.8), Inches(1.5), cl_w, cl_h, "Cluster B: Submission & Versioning", [
        ("USER (1)", "──< AUTHOR (1) ──< PAPER_AUTHOR >── PAPER (1) ──< VERSION (N)"),
        ("Hierarchy:", "Authors submit Papers with discrete Versions (V1, V2, Camera-Ready)."),
        ("Key Entities:", "User, Author, Paper, Paper_Author, Paper_Version.")
    ], C_TEAL)

    add_card(slide11, Inches(0.8), Inches(3.8), cl_w, cl_h, "Cluster C: Review & Evaluation", [
        ("REVIEWER (1)", "──< EXPERTISE >── TOPIC  |  REVIEWER ──< CONFLICT >── AUTHOR"),
        ("Workflow:", "PAPER >── ASSIGNMENT (M:N) ──< REVIEWER  ──>  REVIEW (1:1)"),
        ("Key Entities:", "Reviewer, Reviewer_Expertise, Reviewer_Conflict, Paper_Assignment, Review.")
    ], C_AMBER)

    add_card(slide11, Inches(6.8), Inches(3.8), cl_w, cl_h, "Cluster D: Decisions & Presentation Scheduling", [
        ("DECISION (1:1)", "Gated by ≥3 Reviews ──> Accepted Papers ──> REGISTRATION"),
        ("Timetable:", "REGISTRATION (Paid) ──> PRESENTATION_SLOT (1:1) ──> SESSION"),
        ("Key Entities:", "Decision, Registration, Session, Presentation_Slot.")
    ], C_NAVY_DEEP)

    add_callout(slide11, Inches(0.8), Inches(6.05), Inches(11.7), Inches(0.8),
                "Mermaid ER Diagram Available in Documentation",
                "Full Crow's Foot ER Diagram is generated in the accompanying documentation file (`REVIEW_1_DOCUMENTATION.md`) ready for projection and submission.")

    # ==========================================
    # SLIDE 12: RELATIONAL SCHEMA - SUBMISSION MODULE
    # ==========================================
    slide12 = add_blank_slide()
    add_header(slide12, "Relational Schema: Submission & Version Module", "Deliverable 3: Relational Tables")
    add_footer(slide12, 12)

    s1_headers = ["Table Name", "Primary Key (PK)", "Foreign Keys (FK)", "Key Attributes & Types", "Constraints (NOT NULL, UNIQUE, CHECK)"]
    s1_data = [
        ["Conferences", "conference_id (INT)", "None", "title (VARCHAR), acronym, year, start_date, end_date", "title NOT NULL, UNIQUE(acronym, year), CHECK(end_date >= start_date)"],
        ["Tracks", "track_id (INT)", "conference_id → Conferences", "track_name (VARCHAR), description (TEXT)", "track_name NOT NULL, UNIQUE(conference_id, track_name)"],
        ["Topics", "topic_id (INT)", "track_id → Tracks", "topic_name (VARCHAR), keywords (TEXT)", "topic_name NOT NULL, UNIQUE(track_id, topic_name)"],
        ["Users", "user_id (INT)", "None", "first_name, last_name, email, affiliation, role", "email UNIQUE NOT NULL, role IN ('CHAIR','AUTHOR','REVIEWER','ATTENDEE')"],
        ["Authors", "author_id (INT)", "user_id → Users", "bio (TEXT), orcid_id (VARCHAR)", "user_id UNIQUE NOT NULL"],
        ["Papers", "paper_id (INT)", "track_id → Tracks, primary_author_id → Authors", "title (VARCHAR), abstract (TEXT), status (VARCHAR)", "title NOT NULL, status IN ('SUBMITTED','UNDER_REVIEW','ACCEPTED','REJECTED')"],
        ["Paper_Authors", "(paper_id, author_id)", "paper_id → Papers, author_id → Authors", "author_order (INT), is_corresponding (BOOLEAN)", "author_order >= 1, composite PK ensures unique author link"],
        ["Paper_Versions", "version_id (INT)", "paper_id → Papers", "version_num (INT), file_path, is_camera_ready, created_at", "UNIQUE(paper_id, version_num), file_path NOT NULL"]
    ]

    create_styled_table(slide12, Inches(0.8), Inches(1.5), Inches(11.733), Inches(4.35),
                        s1_headers, s1_data,
                        [Inches(1.8), Inches(1.8), Inches(2.8), Inches(2.8), Inches(2.533)])

    add_callout(slide12, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.8),
                "Normalization Highlight (Submission Module)",
                "Paper versions are extracted to `Paper_Versions`, ensuring `Papers` remains in 3NF without repeating file groups or overwriting original submissions.")

    # ==========================================
    # SLIDE 13: RELATIONAL SCHEMA - REVIEW & ASSIGNMENT MODULE
    # ==========================================
    slide13 = add_blank_slide()
    add_header(slide13, "Relational Schema: Review & Assignment Module", "Deliverable 3: Relational Tables")
    add_footer(slide13, 13)

    s2_headers = ["Table Name", "Primary Key (PK)", "Foreign Keys (FK)", "Key Attributes & Types", "Constraints & Business Rules"]
    s2_data = [
        ["Reviewers", "reviewer_id (INT)", "user_id → Users", "max_workload (INT), is_active (BOOL)", "user_id UNIQUE, max_workload DEFAULT 5, CHECK(max_workload > 0)"],
        ["Reviewer_Expertise", "(reviewer_id, topic_id)", "reviewer_id → Reviewers, topic_id → Topics", "expertise_level (VARCHAR)", "CHECK(expertise_level IN ('EXPERT', 'KNOWLEDGEABLE', 'INFORMED'))"],
        ["Reviewer_Conflicts", "conflict_id (INT)", "reviewer_id → Reviewers, author_id → Authors", "conflict_type (VARCHAR), declared_at (TIMESTAMP)", "UNIQUE(reviewer_id, author_id), conflict_type IN ('CO_AUTHOR','SAME_INSTITUTION','ADVISORY')"],
        ["Paper_Assignments", "assignment_id (INT)", "paper_id → Papers, reviewer_id → Reviewers", "assigned_at, due_date, status (VARCHAR)", "UNIQUE(paper_id, reviewer_id), status IN ('ASSIGNED','ACCEPTED','DECLINED','COMPLETED')"],
        ["Reviews", "review_id (INT)", "assignment_id → Paper_Assignments", "originality (INT), soundness (INT), clarity (INT), overall_score (INT), comments", "assignment_id UNIQUE (1:1), CHECK scores BETWEEN 1 AND 10"]
    ]

    create_styled_table(slide13, Inches(0.8), Inches(1.5), Inches(11.733), Inches(4.35),
                        s2_headers, s2_data,
                        [Inches(2.0), Inches(2.0), Inches(3.0), Inches(2.6), Inches(2.133)])

    add_callout(slide13, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.8),
                "Integrity Highlight (Review Engine)",
                "The `UNIQUE(paper_id, reviewer_id)` constraint guarantees a reviewer cannot be assigned the same paper twice, while score CHECK constraints guarantee data cleanliness.")

    # ==========================================
    # SLIDE 14: RELATIONAL SCHEMA - DECISIONS & SCHEDULING MODULE
    # ==========================================
    slide14 = add_blank_slide()
    add_header(slide14, "Relational Schema: Decisions, Registration & Scheduling", "Deliverable 3: Relational Tables")
    add_footer(slide14, 14)

    s3_headers = ["Table Name", "Primary Key (PK)", "Foreign Keys (FK)", "Key Attributes & Types", "Constraints & Business Rules"]
    s3_data = [
        ["Decisions", "decision_id (INT)", "paper_id → Papers, chair_id → Users", "decision_type (VARCHAR), decision_date, feedback_summary", "paper_id UNIQUE (1:1), decision_type IN ('ACCEPT','REJECT','REVISE')"],
        ["Registrations", "registration_id (INT)", "conference_id → Conferences, user_id → Users, paper_id → Papers", "reg_type (VARCHAR), payment_status (VARCHAR), amount_paid (DECIMAL)", "payment_status IN ('PAID','PENDING','WAIVED'), UNIQUE(conference_id, user_id, paper_id)"],
        ["Sessions", "session_id (INT)", "conference_id → Conferences, track_id → Tracks", "session_title (VARCHAR), session_date, room_no, chair_name", "session_title NOT NULL, room_no NOT NULL"],
        ["Presentation_Slots", "slot_id (INT)", "session_id → Sessions, paper_id → Papers", "slot_date, start_time, end_time, presentation_order", "paper_id UNIQUE (1:1 slot per paper), CHECK(end_time > start_time)"]
    ]

    create_styled_table(slide14, Inches(0.8), Inches(1.5), Inches(11.733), Inches(4.35),
                        s3_headers, s3_data,
                        [Inches(2.0), Inches(2.0), Inches(3.0), Inches(2.6), Inches(2.133)])

    add_callout(slide14, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.8),
                "Scheduling Integrity Highlight",
                "`paper_id UNIQUE` prevents an accepted paper from being scheduled multiple times. Time intervals and room assignments enforce conflict-free proceedings.")

    # ==========================================
    # SLIDE 15: NORMALIZATION STRATEGY (1NF, 2NF, 3NF)
    # ==========================================
    slide15 = add_blank_slide()
    add_header(slide15, "Normalization Analysis: 1NF, 2NF & 3NF Proof", "Deliverable 3: Relational Normalization")
    add_footer(slide15, 15)

    n_w = Inches(3.7)
    n_h = Inches(4.3)

    add_card(slide15, Inches(0.8), Inches(1.5), n_w, n_h, "First Normal Form (1NF)", [
        ("Condition:", "All attributes contain only atomic (indivisible) values; no repeating groups."),
        ("Design Proof:", "Authors were previously stored as comma-separated strings. Decomposed into `Paper_Authors` table."),
        ("Multi-Version Atomicity:", "Versions decomposed into `Paper_Versions` rather than array/comma-separated filepaths."),
        ("Result:", "Every table has a defined Primary Key and all cell values are strictly scalar.")
    ], C_BLUE_PRIMARY)

    add_card(slide15, Inches(4.8), Inches(1.5), n_w, n_h, "Second Normal Form (2NF)", [
        ("Condition:", "Must be in 1NF AND contain no partial key dependencies (every non-prime attribute depends on full PK)."),
        ("Design Proof:", "In composite key tables like `Paper_Authors(paper_id, author_id)`, attributes `author_order` and `is_corresponding` depend on BOTH keys."),
        ("No Partial Leak:", "Author bio/name is NOT stored in `Paper_Authors`; it resides strictly in `Users`/`Authors`."),
        ("Result:", "Zero partial key dependencies across all bridge entities.")
    ], C_TEAL)

    add_card(slide15, Inches(8.8), Inches(1.5), n_w, n_h, "Third Normal Form (3NF)", [
        ("Condition:", "Must be in 2NF AND contain no transitive dependencies (X → Y where Y is non-prime)."),
        ("Design Proof:", "In `Papers`, track name or chair info is NOT stored; only `track_id` is referenced."),
        ("User Decoupling:", "Reviewers and Authors reference `user_id`; personal data (name, email) is not repeated."),
        ("Result:", "Every non-key attribute depends ONLY on the Primary Key ('The key, the whole key, and nothing but the key').")
    ], C_AMBER)

    add_callout(slide15, Inches(0.8), Inches(6.0), Inches(11.7), Inches(0.85),
                "Anomaly Elimination Summary",
                "Insertion Anomaly: Resolved (tracks exist without papers). Deletion Anomaly: Resolved (deleting a paper does not delete author profile). Update Anomaly: Resolved (author email updated in one place: `Users`).")

    # ==========================================
    # SLIDE 16: INTEGRITY CONSTRAINTS & BUSINESS RULES IMPLEMENTATION
    # ==========================================
    slide16 = add_blank_slide()
    add_header(slide16, "Integrity Constraints & Business Logic Enforcement", "Deliverable 3: Constraints & Logic")
    add_footer(slide16, 16)

    rule_headers = ["Constraint Type", "Target Table", "SQL Constraint / Rule Definition", "Business Impact"]
    rule_data = [
        ["Domain CHECK", "Reviews", "CHECK (overall_score BETWEEN 1 AND 10)", "Guarantees valid standardized score inputs; prevents corrupt rating averages."],
        ["Domain CHECK", "Presentation_Slots", "CHECK (end_time > start_time)", "Prevents impossible or negative presentation durations."],
        ["Domain CHECK", "Conferences", "CHECK (end_date >= start_date)", "Ensures conference date validity."],
        ["Candidate UNIQUE", "Paper_Assignments", "UNIQUE (paper_id, reviewer_id)", "Prevents double-assigning the same paper to a reviewer."],
        ["Candidate UNIQUE", "Decisions", "UNIQUE (paper_id)", "Enforces single authoritative decision per submission."],
        ["Candidate UNIQUE", "Presentation_Slots", "UNIQUE (paper_id)", "Guarantees accepted papers are scheduled in at most one slot."],
        ["Business Logic Trigger", "Paper_Assignments", "BEFORE INSERT: Check `Reviewer_Conflicts` for any co-author", "Enforces zero-conflict assignment: aborts transaction if COI exists."],
        ["Business Logic Trigger", "Presentation_Slots", "BEFORE INSERT: Check author overlap across all rooms", "Prevents multi-paper authors from being scheduled simultaneously in 2 rooms."]
    ]

    create_styled_table(slide16, Inches(0.8), Inches(1.5), Inches(11.733), Inches(4.35),
                        rule_headers, rule_data,
                        [Inches(2.0), Inches(1.8), Inches(4.2), Inches(3.733)])

    add_callout(slide16, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.8),
                "Multi-Tiered Enforcement",
                "Level 1: Declarative DDL constraints (NOT NULL, CHECK, UNIQUE). Level 2: Foreign Key cascade controls. Level 3: Procedural database triggers for cross-table conflict checks.")

    # ==========================================
    # SLIDE 17: IMPLEMENTATION ROADMAP & TECH STACK
    # ==========================================
    slide17 = add_blank_slide()
    add_header(slide17, "Implementation Roadmap & Technology Stack", "Roadmap: Review 1 to Review 3")
    add_footer(slide17, 17)

    tech_w = Inches(3.7)
    tech_h = Inches(4.3)

    add_card(slide17, Inches(0.8), Inches(1.5), tech_w, tech_h, "Review 1 (Week 7) [TODAY]", [
        ("Status:", "COMPLETED & SUBMITTED (5 Marks)"),
        ("Deliverables:", "Problem statement, objectives, scope, user roles."),
        ("Conceptual Design:", "14 Principal Entities, Cardinalities, ER Model."),
        ("Relational Schema:", "Normalized tables up to 3NF, PK/FK definitions, constraint rules."),
        ("Artifacts Ready:", "PPT Presentation, ER Diagram, Schema SQL script, Viva guide.")
    ], C_TEAL)

    add_card(slide17, Inches(4.8), Inches(1.5), tech_w, tech_h, "Review 2 (Week 10) [NEXT]", [
        ("Target Weightage:", "10 Marks"),
        ("DDL & Population:", "Executing schema in PostgreSQL/MySQL with realistic mock data (50+ records)."),
        ("Advanced SQL Queries:", "Aggregate functions, nested queries, joins across 4+ tables."),
        ("Views & Reports:", "Pending reviews, reviewer workload distribution, track statistics, schedule timetable."),
        ("Indexes & Optimization:", "Query execution plan analysis (EXPLAIN ANALYZE).")
    ], C_BLUE_PRIMARY)

    add_card(slide17, Inches(8.8), Inches(1.5), tech_w, tech_h, "Review 3 (Week 14) [FINAL]", [
        ("Target Weightage:", "15 Marks"),
        ("Front-End Development:", "Python (Flask / FastAPI) or Java (Spring Boot / JavaFX)."),
        ("UI Workflows:", "Paper submission portal, version tracking, reviewer scoring, chair decision dashboard."),
        ("Transaction Management:", "ACID transaction boundaries during assignment & decision triggers."),
        ("Systematic Testing:", "Input validation, boundary tests, end-to-end conference lifecycle demo.")
    ], C_NAVY_DEEP)

    add_callout(slide17, Inches(0.8), Inches(6.0), Inches(11.7), Inches(0.85),
                "Selected Tech Stack",
                "Database Engine: PostgreSQL 16 (or MySQL 8.0)  |  Front-End: Python (Flask + Bootstrap 5) or Java  |  Tooling: pgAdmin / DBeaver, Git version control.")

    # ==========================================
    # SLIDE 18: SUMMARY & VIVA DISCUSSION (DARK THEME)
    # ==========================================
    slide18 = add_blank_slide(C_NAVY_DARK)

    accent_bar18 = slide18.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.15))
    accent_bar18.fill.solid()
    accent_bar18.fill.fore_color.rgb = C_CYAN_ACCENT
    accent_bar18.line.fill.background()

    t_box18 = slide18.shapes.add_textbox(Inches(1.0), Inches(1.0), Inches(11.333), Inches(1.6))
    tf18 = t_box18.text_frame
    tf18.word_wrap = True

    p0 = tf18.paragraphs[0]
    p0.text = "REVIEW 1 SUMMARY & CONCLUSION"
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = C_CYAN_ACCENT
    p0.space_after = Pt(6)

    p1 = tf18.add_paragraph()
    p1.text = "All Review 1 Milestones Successfully Formulated"
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.font.color.rgb = C_TEXT_WHITE
    p1.space_after = Pt(8)

    p2 = tf18.add_paragraph()
    p2.text = "Solid theoretical foundations in place for database implementation and front-end integration."
    p2.font.size = Pt(12)
    p2.font.color.rgb = RGBColor(148, 163, 184)

    sc_w = Inches(3.5)
    sc_h = Inches(3.2)
    sc_y = Inches(2.9)

    sc1 = slide18.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), sc_y, sc_w, sc_h)
    sc1.fill.solid()
    sc1.fill.fore_color.rgb = RGBColor(15, 34, 64)
    sc1.line.color.rgb = RGBColor(30, 58, 138)
    tf_sc1 = sc1.text_frame
    tf_sc1.word_wrap = True
    tf_sc1.margin_left = Inches(0.2)
    tf_sc1.margin_top = Inches(0.2)
    p = tf_sc1.paragraphs[0]
    p.text = "1. Requirements & Scope"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT
    p.space_after = Pt(6)
    for b in [
        "Rigorous problem identification targeting email workflow failures",
        "Clear demarcation of in-scope vs out-of-scope modules",
        "Comprehensive user role matrix with 6 distinct actors",
        "Functional requirements covering submission to timetable scheduling"
    ]:
        p = tf_sc1.add_paragraph()
        p.text = "✔ " + b
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_TEXT_LIGHT
        p.space_after = Pt(4)

    sc2 = slide18.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.9), sc_y, sc_w, sc_h)
    sc2.fill.solid()
    sc2.fill.fore_color.rgb = RGBColor(15, 34, 64)
    sc2.line.color.rgb = RGBColor(30, 58, 138)
    tf_sc2 = sc2.text_frame
    tf_sc2.word_wrap = True
    tf_sc2.margin_left = Inches(0.2)
    tf_sc2.margin_top = Inches(0.2)
    p = tf_sc2.paragraphs[0]
    p.text = "2. Conceptual ER Design"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT
    p.space_after = Pt(6)
    for b in [
        "All 14 principal entities explicitly modeled",
        "M:N relationships resolved via dedicated bridge tables",
        "Clear cardinalities (1:1, 1:N, M:N) mapped to business rules",
        "Structured cluster architecture: Admin, Submission, Review, Scheduling"
    ]:
        p = tf_sc2.add_paragraph()
        p.text = "✔ " + b
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_TEXT_LIGHT
        p.space_after = Pt(4)

    sc3 = slide18.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), sc_y, sc_w, sc_h)
    sc3.fill.solid()
    sc3.fill.fore_color.rgb = RGBColor(15, 34, 64)
    sc3.line.color.rgb = RGBColor(30, 58, 138)
    tf_sc3 = sc3.text_frame
    tf_sc3.word_wrap = True
    tf_sc3.margin_left = Inches(0.2)
    tf_sc3.margin_top = Inches(0.2)
    p = tf_sc3.paragraphs[0]
    p.text = "3. 3NF Relational Schema"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT
    p.space_after = Pt(6)
    for b in [
        "Mathematically verified 1NF, 2NF, and 3NF normalization",
        "Elimination of insertion, deletion, and update anomalies",
        "Multi-tiered constraints: PK, FK, UNIQUE, NOT NULL, CHECK",
        "Executable SQL DDL script prepared for immediate testing"
    ]:
        p = tf_sc3.add_paragraph()
        p.text = "✔ " + b
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_TEXT_LIGHT
        p.space_after = Pt(4)

    qa_box = slide18.shapes.add_textbox(Inches(1.0), Inches(6.35), Inches(11.333), Inches(0.7))
    tf_qa = qa_box.text_frame
    tf_qa.word_wrap = True
    p = tf_qa.paragraphs[0]
    p.text = "Thank You! We are now open for Evaluator Questions & Review Discussion."
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT
    p.alignment = PP_ALIGN.CENTER

    output_path = "Academic_Conference_DBMS_Review1.pptx"
    prs.save(output_path)
    print(f"Presentation successfully saved to: {output_path}")

if __name__ == "__main__":
    create_presentation()
