import os
from PIL import Image, ImageDraw, ImageFont

def generate_er_image():
    width = 2800
    height = 1750
    img = Image.new("RGB", (width, height), color=(248, 250, 252)) # #F8FAFC
    draw = ImageDraw.Draw(img)

    # Load Windows fonts
    font_title = ImageFont.truetype("C:/Windows/Fonts/calibrib.ttf", 36)
    font_sub = ImageFont.truetype("C:/Windows/Fonts/calibri.ttf", 22)
    font_hdr = ImageFont.truetype("C:/Windows/Fonts/calibrib.ttf", 22)
    font_attr_bold = ImageFont.truetype("C:/Windows/Fonts/calibrib.ttf", 17)
    font_attr = ImageFont.truetype("C:/Windows/Fonts/calibri.ttf", 17)
    font_rel = ImageFont.truetype("C:/Windows/Fonts/calibrib.ttf", 16)

    # Color Palette
    C_NAVY_HDR     = (30, 58, 138)      # #1E3A8A
    C_PURPLE_HDR   = (109, 40, 217)     # #6D28D9
    C_AMBER_HDR    = (180, 83, 9)       # #B45309
    C_TEAL_HDR     = (13, 148, 136)     # #0D9488
    C_CARD_BG      = (255, 255, 255)
    C_CARD_BORDER  = (203, 213, 225)    # #CBD5E1
    C_PK_COLOR     = (220, 38, 38)      # #DC2626
    C_FK_COLOR     = (37, 99, 235)      # #2563EB
    C_TEXT_MAIN    = (30, 41, 59)       # #1E293B
    C_LINE_COLOR   = (100, 116, 139)    # #64748B
    C_LABEL_BG     = (238, 242, 255)    # #EEF2FF
    C_LABEL_BORDER = (191, 219, 254)    # #BFDBFE

    # Banner Title
    draw.rectangle([0, 0, width, 80], fill=(30, 58, 138))
    draw.text((60, 20), "CONCEPTUAL ENTITY-RELATIONSHIP (ER) DIAGRAM", fill=(255, 255, 255), font=font_title)
    draw.text((1600, 28), "ACADEMIC CONFERENCE PAPER SUBMISSION & REVIEW SYSTEM", fill=(191, 219, 254), font=font_sub)

    entities = {}

    def draw_entity(name, x, y, w, h, header_col, attrs):
        entities[name] = {"x": x, "y": y, "w": w, "h": h, "cx": x + w // 2, "cy": y + h // 2}
        
        # Shadow / border
        draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=C_CARD_BG, outline=C_CARD_BORDER, width=2)
        
        # Header bar
        hdr_h = 38
        draw.rounded_rectangle([x, y, x + w, y + hdr_h], radius=8, fill=header_col)
        draw.rectangle([x, y + hdr_h - 6, x + w, y + hdr_h], fill=header_col) # square bottom corners of header
        
        # Header text
        draw.text((x + 14, y + 7), name, fill=(255, 255, 255), font=font_hdr)
        
        # Attributes
        curr_y = y + hdr_h + 10
        for tag, attr_name, attr_type in attrs:
            # Tag: PK, FK, PF (PK+FK), or ""
            tx = x + 14
            if tag == "PK":
                draw.text((tx, curr_y), "PK", fill=C_PK_COLOR, font=font_attr_bold)
                tx += 30
            elif tag == "FK":
                draw.text((tx, curr_y), "FK", fill=C_FK_COLOR, font=font_attr_bold)
                tx += 30
            elif tag == "PF":
                draw.text((tx, curr_y), "PK,FK", fill=(147, 51, 234), font=font_attr_bold)
                tx += 48
            else:
                draw.text((tx, curr_y), "•", fill=(148, 163, 184), font=font_attr)
                tx += 20
                
            draw.text((tx, curr_y), attr_name, fill=C_TEXT_MAIN, font=font_attr)
            
            # Type right-aligned or muted
            draw.text((x + w - 120, curr_y), attr_type, fill=(148, 163, 184), font=font_attr)
            curr_y += 24

    # -------------------------------------------------------------
    # 1. COLUMN 1: CONFERENCE STRUCTURE & SESSIONS (Left)
    # -------------------------------------------------------------
    draw_entity("CONFERENCES", 80, 120, 520, 290, C_NAVY_HDR, [
        ("PK", "conference_id", "INT"),
        ("",   "title", "VARCHAR(255)"),
        ("",   "acronym", "VARCHAR(30)"),
        ("",   "year", "INT"),
        ("",   "start_date", "DATE"),
        ("",   "end_date", "DATE"),
        ("",   "location", "VARCHAR(255)"),
        ("",   "submission_deadline", "DATE"),
        ("",   "created_at", "TIMESTAMP")
    ])

    draw_entity("TRACKS", 80, 480, 520, 200, C_NAVY_HDR, [
        ("PK", "track_id", "INT"),
        ("FK", "conference_id", "INT"),
        ("",   "track_name", "VARCHAR(100)"),
        ("",   "description", "TEXT"),
        ("",   "UNIQUE(conf_id, track_name)", "CONSTRAINT")
    ])

    draw_entity("TOPICS", 80, 750, 520, 200, C_NAVY_HDR, [
        ("PK", "topic_id", "INT"),
        ("FK", "track_id", "INT"),
        ("",   "topic_name", "VARCHAR(150)"),
        ("",   "keywords", "TEXT"),
        ("",   "UNIQUE(track_id, topic_name)", "CONSTRAINT")
    ])

    draw_entity("SESSIONS", 80, 1020, 520, 250, C_NAVY_HDR, [
        ("PK", "session_id", "INT"),
        ("FK", "conference_id", "INT"),
        ("FK", "track_id", "INT"),
        ("",   "session_title", "VARCHAR(200)"),
        ("",   "session_date", "DATE"),
        ("",   "room_no", "VARCHAR(50)"),
        ("",   "session_chair", "VARCHAR(150)")
    ])

    draw_entity("PRESENTATION_SLOTS", 80, 1340, 520, 260, C_TEAL_HDR, [
        ("PK", "slot_id", "INT"),
        ("FK", "session_id", "INT"),
        ("FK", "paper_id (UNIQUE)", "INT"),
        ("",   "slot_date", "DATE"),
        ("",   "start_time", "TIME"),
        ("",   "end_time", "TIME"),
        ("",   "presentation_order", "INT"),
        ("",   "CHECK(end_time > start_time)", "CONSTRAINT")
    ])

    # -------------------------------------------------------------
    # 2. COLUMN 2: USERS, AUTHORS & PAPERS (Center-Left)
    # -------------------------------------------------------------
    draw_entity("USERS", 720, 120, 540, 270, C_PURPLE_HDR, [
        ("PK", "user_id", "INT"),
        ("",   "first_name", "VARCHAR(80)"),
        ("",   "last_name", "VARCHAR(80)"),
        ("",   "email (UNIQUE)", "VARCHAR(150)"),
        ("",   "password_hash", "VARCHAR(255)"),
        ("",   "affiliation", "VARCHAR(200)"),
        ("",   "country", "VARCHAR(80)"),
        ("",   "role", "VARCHAR(30)")
    ])

    draw_entity("AUTHORS", 720, 460, 540, 190, C_PURPLE_HDR, [
        ("PK", "author_id", "INT"),
        ("FK", "user_id (UNIQUE 1:1)", "INT"),
        ("",   "orcid_id", "VARCHAR(30)"),
        ("",   "bio", "TEXT")
    ])

    draw_entity("PAPER_AUTHORS", 720, 720, 540, 210, C_PURPLE_HDR, [
        ("PF", "paper_id", "INT"),
        ("PF", "author_id", "INT"),
        ("",   "author_order", "INT"),
        ("",   "is_corresponding", "BOOLEAN"),
        ("",   "PRIMARY KEY (paper_id, author_id)", "COMPOSITE"),
        ("",   "UNIQUE (paper_id, author_order)", "CONSTRAINT")
    ])

    draw_entity("PAPERS", 720, 1000, 540, 270, C_PURPLE_HDR, [
        ("PK", "paper_id", "INT"),
        ("FK", "track_id", "INT"),
        ("FK", "primary_author_id", "INT"),
        ("",   "title", "VARCHAR(300)"),
        ("",   "abstract", "TEXT"),
        ("",   "status", "VARCHAR(40)"),
        ("",   "submission_date", "TIMESTAMP")
    ])

    draw_entity("PAPER_VERSIONS", 720, 1340, 540, 240, C_PURPLE_HDR, [
        ("PK", "version_id", "INT"),
        ("FK", "paper_id", "INT"),
        ("",   "version_num", "INT"),
        ("",   "file_path", "VARCHAR(500)"),
        ("",   "changelog", "TEXT"),
        ("",   "is_camera_ready", "BOOLEAN"),
        ("",   "upload_timestamp", "TIMESTAMP"),
        ("",   "UNIQUE(paper_id, version_num)", "CONSTRAINT")
    ])

    # -------------------------------------------------------------
    # 3. COLUMN 3: REVIEWERS, CONFLICTS & REVIEWS (Center-Right)
    # -------------------------------------------------------------
    draw_entity("REVIEWERS", 1380, 120, 540, 200, C_AMBER_HDR, [
        ("PK", "reviewer_id", "INT"),
        ("FK", "user_id (UNIQUE 1:1)", "INT"),
        ("",   "max_workload (DEFAULT 5)", "INT"),
        ("",   "is_active", "BOOLEAN")
    ])

    draw_entity("REVIEWER_EXPERTISE", 1380, 390, 540, 190, C_AMBER_HDR, [
        ("PF", "reviewer_id", "INT"),
        ("PF", "topic_id", "INT"),
        ("",   "expertise_level", "VARCHAR(30)"),
        ("",   "CHECK(level IN ('EXPERT','KNOW','INF'))", "CONSTRAINT")
    ])

    draw_entity("REVIEWER_CONFLICTS", 1380, 650, 540, 210, C_AMBER_HDR, [
        ("PK", "conflict_id", "INT"),
        ("FK", "reviewer_id", "INT"),
        ("FK", "author_id", "INT"),
        ("",   "conflict_type", "VARCHAR(50)"),
        ("",   "declared_at", "TIMESTAMP"),
        ("",   "UNIQUE(reviewer_id, author_id)", "CONSTRAINT")
    ])

    draw_entity("PAPER_ASSIGNMENTS", 1380, 930, 540, 230, C_AMBER_HDR, [
        ("PK", "assignment_id", "INT"),
        ("FK", "paper_id", "INT"),
        ("FK", "reviewer_id", "INT"),
        ("",   "assigned_at", "TIMESTAMP"),
        ("",   "due_date", "DATE"),
        ("",   "status", "VARCHAR(30)"),
        ("",   "UNIQUE(paper_id, reviewer_id)", "CONSTRAINT")
    ])

    draw_entity("REVIEWS", 1380, 1230, 540, 290, C_AMBER_HDR, [
        ("PK", "review_id", "INT"),
        ("FK", "assignment_id (UNIQUE 1:1)", "INT"),
        ("",   "originality [1-10]", "INT"),
        ("",   "soundness [1-10]", "INT"),
        ("",   "clarity [1-10]", "INT"),
        ("",   "overall_score [1-10]", "INT"),
        ("",   "comments_for_author", "TEXT"),
        ("",   "confidential_chair_comments", "TEXT"),
        ("",   "submitted_at", "TIMESTAMP")
    ])

    # -------------------------------------------------------------
    # 4. COLUMN 4: DECISIONS & REGISTRATIONS (Right)
    # -------------------------------------------------------------
    draw_entity("DECISIONS", 2040, 350, 520, 240, C_TEAL_HDR, [
        ("PK", "decision_id", "INT"),
        ("FK", "paper_id (UNIQUE 1:1)", "INT"),
        ("FK", "chair_id", "INT"),
        ("",   "decision_type", "VARCHAR(30)"),
        ("",   "feedback_summary", "TEXT"),
        ("",   "decision_date", "TIMESTAMP"),
        ("",   "CHECK(type IN ('ACCEPT','REJECT',..))", "CONSTRAINT")
    ])

    draw_entity("REGISTRATIONS", 2040, 720, 520, 270, C_TEAL_HDR, [
        ("PK", "registration_id", "INT"),
        ("FK", "conference_id", "INT"),
        ("FK", "user_id", "INT"),
        ("FK", "paper_id", "INT"),
        ("",   "registration_type", "VARCHAR(40)"),
        ("",   "payment_status", "VARCHAR(30)"),
        ("",   "amount_paid", "DECIMAL(10,2)"),
        ("",   "transaction_ref", "VARCHAR(100)"),
        ("",   "registered_at", "TIMESTAMP")
    ])

    # -------------------------------------------------------------
    # CONNECTING RELATIONSHIP LINES & CARDINALITY BADGES
    # -------------------------------------------------------------
    def draw_line_with_label(p1, p2, label):
        # Draw clean line
        draw.line([p1, p2], fill=C_LINE_COLOR, width=3)
        # Midpoint label
        mx = (p1[0] + p2[0]) // 2
        my = (p1[1] + p2[1]) // 2
        
        tw = len(label) * 10 + 12
        th = 24
        draw.rounded_rectangle([mx - tw//2, my - th//2, mx + tw//2, my + th//2], radius=4, fill=C_LABEL_BG, outline=C_LABEL_BORDER, width=1)
        draw.text((mx - tw//2 + 6, my - th//2 + 3), label, fill=C_NAVY_HDR, font=font_rel)

    # 1. Conferences -> Tracks (1:N)
    draw_line_with_label((340, 410), (340, 480), "1 : N")
    
    # 2. Tracks -> Topics (1:N)
    draw_line_with_label((340, 680), (340, 750), "1 : N")

    # 3. Tracks -> Sessions (1:N)
    draw_line_with_label((340, 950), (340, 1020), "1 : N")

    # 4. Sessions -> Presentation_Slots (1:N)
    draw_line_with_label((340, 1270), (340, 1340), "1 : N")

    # 5. Users -> Authors (1:1)
    draw_line_with_label((990, 390), (990, 460), "1 : 1")

    # 6. Authors -> Paper_Authors (1:N)
    draw_line_with_label((990, 650), (990, 720), "1 : N")

    # 7. Paper_Authors -> Papers (N:1)
    draw_line_with_label((990, 930), (990, 1000), "N : 1")

    # 8. Papers -> Paper_Versions (1:N)
    draw_line_with_label((990, 1270), (990, 1340), "1 : N")

    # 9. Users -> Reviewers (1:1)
    draw_line_with_label((1260, 220), (1380, 220), "1 : 1")

    # 10. Reviewers -> Reviewer_Expertise (1:N)
    draw_line_with_label((1650, 320), (1650, 390), "1 : N")

    # 11. Reviewers -> Reviewer_Conflicts (1:N)
    draw_line_with_label((1650, 580), (1650, 650), "1 : N")

    # 12. Reviewers -> Paper_Assignments (1:N)
    draw_line_with_label((1650, 860), (1650, 930), "1 : N")

    # 13. Paper_Assignments -> Reviews (1:1)
    draw_line_with_label((1650, 1160), (1650, 1230), "1 : 1")

    # 14. Papers -> Paper_Assignments (1:N)
    draw_line_with_label((1260, 1070), (1380, 1070), "1 : N")

    # 15. Papers -> Decisions (1:1)
    draw_line_with_label((1260, 1030), (2040, 450), "1 : 1")

    # 16. Papers -> Presentation_Slots (1:1)
    draw_line_with_label((720, 1200), (600, 1420), "1 : 1")

    # Save high-resolution image
    out_path = "er_diagram.png"
    img.save(out_path, quality=95)
    print(f"High-resolution ER Diagram successfully generated: {out_path} ({width}x{height})")

if __name__ == "__main__":
    generate_er_image()
