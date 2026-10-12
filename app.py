import os
import sqlite3
from flask import Flask, render_template_string, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "academic_conference_dbms_secret_key"
DB_NAME = "conference_review2.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# Base HTML Template using Bootstrap 5 CDN
BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - Academic Conference DBMS</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root { --primary-navy: #1E3A8A; --accent-blue: #2563EB; }
        body { background-color: #F8FAFC; color: #1E293B; font-family: 'Segoe UI', system-ui, sans-serif; }
        .navbar-brand { font-weight: 700; color: #FFFFFF !important; letter-spacing: 0.5px; }
        .navbar { background-color: var(--primary-navy); box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .nav-link { color: #E2E8F0 !important; font-weight: 500; margin-right: 8px; }
        .nav-link:hover, .nav-link.active { color: #60A5FA !important; }
        .card { border: 1px solid #E2E8F0; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 20px; }
        .card-header { background-color: #FFFFFF; border-bottom: 2px solid #EFF6FF; font-weight: 700; color: var(--primary-navy); }
        .badge-status { font-size: 0.85rem; padding: 5px 10px; border-radius: 4px; }
        .btn-primary { background-color: var(--accent-blue); border-color: var(--accent-blue); }
        .btn-primary:hover { background-color: var(--primary-navy); }
        .table th { background-color: #EFF6FF; color: var(--primary-navy); font-weight: 600; }
        footer { margin-top: 40px; padding: 20px 0; border-top: 1px solid #E2E8F0; color: #64748B; font-size: 0.9rem; text-align: center; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark sticky-top">
        <div class="container">
            <a class="navbar-brand" href="/">🏛 ICDSAI 2026 DBMS</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navContent">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navContent">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="/">📊 Dashboard & Reports</a></li>
                    <li class="nav-item"><a class="nav-link" href="/author">📝 Author Portal</a></li>
                    <li class="nav-item"><a class="nav-link" href="/reviewer">⚖ Reviewer Portal</a></li>
                    <li class="nav-item"><a class="nav-link" href="/chair">👑 Program Chair</a></li>
                    <li class="nav-item"><a class="nav-link" href="/schedule">📅 Timetable</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container my-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </div>

    <footer>
        <p>CS304 Database Management Systems Project &bull; Review 3: Front-End Application & End-to-End System</p>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# -----------------------------------------------------------------------------
# ROUTE 1: DASHBOARD & ANALYTICAL REPORTS
# -----------------------------------------------------------------------------
@app.route("/")
def dashboard():
    conn = get_db()
    # Query summary metrics
    stats = conn.execute("""
        SELECT 
            (SELECT COUNT(*) FROM Papers) AS total_papers,
            (SELECT COUNT(*) FROM Papers WHERE status='ACCEPTED') AS accepted_papers,
            (SELECT COUNT(*) FROM Reviews) AS total_reviews,
            (SELECT COUNT(*) FROM Reviewers) AS total_reviewers,
            (SELECT COUNT(*) FROM Paper_Assignments WHERE status='ASSIGNED') AS pending_reviews
    """).fetchone()

    # Track statistics
    track_stats = conn.execute("SELECT * FROM vw_track_statistics").fetchall()
    # Reviewer workloads
    workloads = conn.execute("SELECT * FROM vw_reviewer_workload").fetchall()
    # Pending reviews
    pending = conn.execute("SELECT * FROM vw_pending_reviews").fetchall()
    conn.close()

    template = BASE_LAYOUT + """
    {% block content %}
    <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
            <h2 class="fw-bold mb-1" style="color: #1E3A8A;">Conference Editorial Dashboard</h2>
            <p class="text-muted mb-0">IEEE International Conference on Distributed Systems & AI 2026 (ICDSAI '26)</p>
        </div>
        <span class="badge bg-success p-2">● Live SQLite Database Connected</span>
    </div>

    <!-- Quick Stats Cards -->
    <div class="row g-3 mb-4">
        <div class="col-md">
            <div class="card p-3 border-start border-4 border-primary">
                <span class="text-muted small fw-bold">TOTAL SUBMISSIONS</span>
                <h3 class="fw-bold text-primary mb-0">{{ stats.total_papers }}</h3>
            </div>
        </div>
        <div class="col-md">
            <div class="card p-3 border-start border-4 border-success">
                <span class="text-muted small fw-bold">ACCEPTED PAPERS</span>
                <h3 class="fw-bold text-success mb-0">{{ stats.accepted_papers }}</h3>
            </div>
        </div>
        <div class="col-md">
            <div class="card p-3 border-start border-4 border-info">
                <span class="text-muted small fw-bold">SUBMITTED REVIEWS</span>
                <h3 class="fw-bold text-info mb-0">{{ stats.total_reviews }}</h3>
            </div>
        </div>
        <div class="col-md">
            <div class="card p-3 border-start border-4 border-warning">
                <span class="text-muted small fw-bold">PENDING REVIEWS</span>
                <h3 class="fw-bold text-warning mb-0">{{ stats.pending_reviews }}</h3>
            </div>
        </div>
        <div class="col-md">
            <div class="card p-3 border-start border-4 border-secondary">
                <span class="text-muted small fw-bold">ACTIVE REVIEWERS</span>
                <h3 class="fw-bold text-secondary mb-0">{{ stats.total_reviewers }}</h3>
            </div>
        </div>
    </div>

    <!-- Track Statistics Table -->
    <div class="card mb-4">
        <div class="card-header d-flex justify-content-between align-items-center">
            <span>📈 Track Acceptance & Volume Statistics (`vw_track_statistics`)</span>
        </div>
        <div class="card-body p-0">
            <div class="table-responsive">
                <table class="table table-hover mb-0">
                    <thead>
                        <tr>
                            <th>Track ID</th>
                            <th>Track Name</th>
                            <th>Submissions</th>
                            <th>Accepted</th>
                            <th>Rejected</th>
                            <th>Under Review</th>
                            <th>Avg Score</th>
                            <th>Acceptance Rate</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for row in track_stats %}
                        <tr>
                            <td>{{ row.track_id }}</td>
                            <td class="fw-bold">{{ row.track_name }}</td>
                            <td>{{ row.total_submissions }}</td>
                            <td><span class="badge bg-success">{{ row.accepted_count }}</span></td>
                            <td><span class="badge bg-danger">{{ row.rejected_count }}</span></td>
                            <td><span class="badge bg-warning text-dark">{{ row.under_review_count }}</span></td>
                            <td><strong>{{ row.track_avg_score or 'N/A' }}</strong> / 10</td>
                            <td>
                                <div class="d-flex align-items-center">
                                    <span class="me-2 fw-bold">{{ row.acceptance_rate_pct }}%</span>
                                    <div class="progress flex-grow-1" style="height: 6px;">
                                        <div class="progress-bar bg-primary" style="width: {{ row.acceptance_rate_pct }}%;"></div>
                                    </div>
                                </div>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <div class="row">
        <!-- Reviewer Workload Table -->
        <div class="col-lg-7">
            <div class="card">
                <div class="card-header">👥 Reviewer Workload Saturation (`vw_reviewer_workload`)</div>
                <div class="card-body p-0">
                    <table class="table table-hover mb-0">
                        <thead>
                            <tr>
                                <th>Reviewer</th>
                                <th>Affiliation</th>
                                <th>Assigned</th>
                                <th>Done</th>
                                <th>Pending</th>
                                <th>Capacity</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for w in workloads %}
                            <tr>
                                <td class="fw-bold">{{ w.reviewer_name }}</td>
                                <td class="text-muted small">{{ w.affiliation }}</td>
                                <td>{{ w.total_assigned_papers }} / {{ w.max_workload }}</td>
                                <td><span class="badge bg-success">{{ w.completed_reviews }}</span></td>
                                <td>
                                    {% if w.pending_reviews > 0 %}
                                        <span class="badge bg-warning text-dark">{{ w.pending_reviews }}</span>
                                    {% else %}
                                        <span class="badge bg-light text-muted">0</span>
                                    {% endif %}
                                </td>
                                <td><span class="badge bg-info text-dark">{{ w.remaining_capacity }} left</span></td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Pending Reviews -->
        <div class="col-lg-5">
            <div class="card">
                <div class="card-header text-danger">⏳ Urgent Pending Reviews (`vw_pending_reviews`)</div>
                <div class="card-body p-0">
                    {% if pending %}
                    <ul class="list-group list-group-flush">
                        {% for p in pending %}
                        <li class="list-group-item">
                            <div class="d-flex justify-content-between align-items-start">
                                <div>
                                    <h6 class="mb-1 text-primary">{{ p.paper_title }}</h6>
                                    <p class="mb-1 small text-muted">Assigned to: <strong>{{ p.reviewer_name }}</strong> ({{ p.reviewer_email }})</p>
                                </div>
                                <span class="badge bg-warning text-dark">Due {{ p.due_date }}</span>
                            </div>
                        </li>
                        {% endfor %}
                    </ul>
                    {% else %}
                    <div class="p-3 text-center text-muted">No pending reviews! All papers evaluated.</div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
    {% endblock %}
    """
    return render_template_string(template, title="Dashboard", stats=stats, track_stats=track_stats, workloads=workloads, pending=pending)

# -----------------------------------------------------------------------------
# ROUTE 2: AUTHOR PORTAL (SUBMISSION & VERSIONS)
# -----------------------------------------------------------------------------
@app.route("/author", methods=["GET", "POST"])
def author_portal():
    conn = get_db()
    if request.method == "POST":
        action = request.form.get("action")
        if action == "submit_paper":
            title = request.form.get("title").strip()
            abstract = request.form.get("abstract").strip()
            track_id = int(request.form.get("track_id"))
            author_id = int(request.form.get("author_id"))

            if not title or not abstract:
                flash("Paper title and abstract are required!", "danger")
            else:
                cur = conn.cursor()
                # Insert master paper
                cur.execute("INSERT INTO Papers (track_id, primary_author_id, title, abstract, status) VALUES (?, ?, ?, ?, 'SUBMITTED')",
                            (track_id, author_id, title, abstract))
                new_paper_id = cur.lastrowid
                # Associate author in Paper_Authors
                cur.execute("INSERT INTO Paper_Authors (paper_id, author_id, author_order, is_corresponding) VALUES (?, ?, 1, 1)",
                            (new_paper_id, author_id))
                # Initial Version 1
                cur.execute("INSERT INTO Paper_Versions (paper_id, version_num, file_path, changelog, is_camera_ready) VALUES (?, 1, ?, 'Initial blind submission', 0)",
                            (new_paper_id, f"/uploads/papers/p{new_paper_id}_v1_blind.pdf"))
                conn.commit()
                flash(f"Paper '{title}' successfully submitted! System assigned Paper ID: {new_paper_id}.", "success")
                return redirect(url_for("author_portal"))

        elif action == "upload_version":
            paper_id = int(request.form.get("paper_id"))
            changelog = request.form.get("changelog", "Revision uploaded").strip()
            is_camera = 1 if request.form.get("is_camera_ready") else 0
            
            # Find current max version
            max_v = conn.execute("SELECT COALESCE(MAX(version_num), 0) FROM Paper_Versions WHERE paper_id = ?", (paper_id,)).fetchone()[0]
            new_v = max_v + 1
            file_name = f"/uploads/papers/p{paper_id}_v{new_v}_{'cameraready' if is_camera else 'draft'}.pdf"
            
            conn.execute("INSERT INTO Paper_Versions (paper_id, version_num, file_path, changelog, is_camera_ready) VALUES (?, ?, ?, ?, ?)",
                         (paper_id, new_v, file_name, changelog, is_camera))
            conn.commit()
            flash(f"Version {new_v} successfully recorded for Paper #{paper_id}!", "success")
            return redirect(url_for("author_portal"))

    # Fetch author submissions and tracks
    tracks = conn.execute("SELECT * FROM Tracks").fetchall()
    authors = conn.execute("SELECT a.author_id, u.first_name || ' ' || u.last_name AS name FROM Authors a JOIN Users u ON a.user_id = u.user_id").fetchall()
    papers = conn.execute("""
        SELECT p.paper_id, p.title, t.track_name, p.status,
               u.first_name || ' ' || u.last_name AS primary_author,
               (SELECT COUNT(*) FROM Paper_Versions pv WHERE pv.paper_id = p.paper_id) AS version_count,
               (SELECT MAX(is_camera_ready) FROM Paper_Versions pv WHERE pv.paper_id = p.paper_id) AS has_camera_ready
        FROM Papers p
        JOIN Tracks t ON p.track_id = t.track_id
        JOIN Authors a ON p.primary_author_id = a.author_id
        JOIN Users u ON a.user_id = u.user_id
        ORDER BY p.paper_id DESC
    """).fetchall()
    conn.close()

    template = BASE_LAYOUT + """
    {% block content %}
    <h2 class="fw-bold mb-3" style="color: #1E3A8A;">Author Submission & Version Tracking Portal</h2>
    
    <div class="row">
        <!-- Submission Form -->
        <div class="col-lg-5">
            <div class="card">
                <div class="card-header">📤 Submit New Research Manuscript</div>
                <div class="card-body">
                    <form method="POST">
                        <input type="hidden" name="action" value="submit_paper">
                        <div class="mb-3">
                            <label class="form-label fw-bold">Primary Author</label>
                            <select name="author_id" class="form-select" required>
                                {% for a in authors %}
                                <option value="{{ a.author_id }}">{{ a.name }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">Conference Track</label>
                            <select name="track_id" class="form-select" required>
                                {% for t in tracks %}
                                <option value="{{ t.track_id }}">{{ t.track_name }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">Paper Title</label>
                            <input type="text" name="title" class="form-control" placeholder="e.g. Scalable Sharding in Proof-of-Stake" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">Abstract</label>
                            <textarea name="abstract" class="form-control" rows="3" placeholder="Summary of the contribution..." required></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">Submit Paper (Creates Version 1)</button>
                    </form>
                </div>
            </div>

            <!-- Upload Revision Form -->
            <div class="card">
                <div class="card-header">🔄 Upload Paper Revision / Camera-Ready</div>
                <div class="card-body">
                    <form method="POST">
                        <input type="hidden" name="action" value="upload_version">
                        <div class="mb-3">
                            <label class="form-label fw-bold">Select Paper</label>
                            <select name="paper_id" class="form-select" required>
                                {% for p in papers %}
                                <option value="{{ p.paper_id }}">#{{ p.paper_id }}: {{ p.title }} (Status: {{ p.status }})</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">Revision Changelog</label>
                            <input type="text" name="changelog" class="form-control" placeholder="e.g. Addressed Reviewer 2 remarks on convergence">
                        </div>
                        <div class="form-check mb-3">
                            <input class="form-check-input" type="checkbox" name="is_camera_ready" id="crCheck">
                            <label class="form-check-label fw-bold text-success" for="crCheck">
                                This is the final Camera-Ready PDF
                            </label>
                        </div>
                        <button type="submit" class="btn btn-success w-100">Upload New Version</button>
                    </form>
                </div>
            </div>
        </div>

        <!-- Papers List -->
        <div class="col-lg-7">
            <div class="card">
                <div class="card-header">📑 Submitted Papers & Version Evolution</div>
                <div class="card-body p-0">
                    <table class="table table-hover mb-0">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Title & Author</th>
                                <th>Track</th>
                                <th>Status</th>
                                <th>Versions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for p in papers %}
                            <tr>
                                <td class="fw-bold">#{{ p.paper_id }}</td>
                                <td>
                                    <strong>{{ p.title }}</strong><br>
                                    <span class="text-muted small">By {{ p.primary_author }}</span>
                                </td>
                                <td class="small">{{ p.track_name }}</td>
                                <td>
                                    {% if p.status == 'ACCEPTED' %}
                                        <span class="badge bg-success">ACCEPTED</span>
                                    {% elif p.status == 'REJECTED' %}
                                        <span class="badge bg-danger">REJECTED</span>
                                    {% else %}
                                        <span class="badge bg-warning text-dark">{{ p.status }}</span>
                                    {% endif %}
                                </td>
                                <td>
                                    <span class="badge bg-secondary">{{ p.version_count }} Versions</span>
                                    {% if p.has_camera_ready %}
                                        <span class="badge bg-success">Camera-Ready ✔</span>
                                    {% endif %}
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}
    """
    return render_template_string(template, title="Author Portal", tracks=tracks, authors=authors, papers=papers)

# -----------------------------------------------------------------------------
# ROUTE 3: REVIEWER PORTAL (SCORES & EVALUATION)
# -----------------------------------------------------------------------------
@app.route("/reviewer", methods=["GET", "POST"])
def reviewer_portal():
    conn = get_db()
    if request.method == "POST":
        action = request.form.get("action")
        if action == "submit_review":
            assignment_id = int(request.form.get("assignment_id"))
            orig = int(request.form.get("originality"))
            sound = int(request.form.get("soundness"))
            clarity = int(request.form.get("clarity"))
            overall = int(request.form.get("overall_score"))
            comments_author = request.form.get("comments_for_author", "").strip()
            comments_chair = request.form.get("confidential_chair_comments", "").strip()

            cur = conn.cursor()
            try:
                # Insert review
                cur.execute("""
                    INSERT INTO Reviews (assignment_id, originality, soundness, clarity, overall_score, comments_for_author, confidential_chair_comments)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (assignment_id, orig, sound, clarity, overall, comments_author, comments_chair))
                # Update assignment status to COMPLETED
                cur.execute("UPDATE Paper_Assignments SET status = 'COMPLETED' WHERE assignment_id = ?", (assignment_id,))
                conn.commit()
                flash("Review submitted successfully! Scores and feedback logged.", "success")
            except Exception as e:
                flash(f"Error submitting review: {str(e)}", "danger")
            return redirect(url_for("reviewer_portal"))

    # Active pending assignments for review
    assignments = conn.execute("""
        SELECT pa.assignment_id, p.paper_id, p.title AS paper_title, p.abstract, t.track_name,
               u.first_name || ' ' || u.last_name AS reviewer_name, r.reviewer_id,
               pa.due_date, pa.status
        FROM Paper_Assignments pa
        JOIN Papers p ON pa.paper_id = p.paper_id
        JOIN Tracks t ON p.track_id = t.track_id
        JOIN Reviewers r ON pa.reviewer_id = r.reviewer_id
        JOIN Users u ON r.user_id = u.user_id
        WHERE pa.status = 'ASSIGNED'
    """).fetchall()

    # Completed reviews
    completed_reviews = conn.execute("""
        SELECT r.review_id, p.title, rev_u.first_name || ' ' || rev_u.last_name AS reviewer_name,
               r.originality, r.soundness, r.clarity, r.overall_score, r.comments_for_author
        FROM Reviews r
        JOIN Paper_Assignments pa ON r.assignment_id = pa.assignment_id
        JOIN Papers p ON pa.paper_id = p.paper_id
        JOIN Reviewers rev ON pa.reviewer_id = rev.reviewer_id
        JOIN Users rev_u ON rev.user_id = rev_u.user_id
        ORDER BY r.review_id DESC LIMIT 10
    """).fetchall()
    conn.close()

    template = BASE_LAYOUT + """
    {% block content %}
    <h2 class="fw-bold mb-3" style="color: #1E3A8A;">Reviewer Portal & Double-Blind Evaluation</h2>

    <div class="row">
        <!-- Review Submission Form -->
        <div class="col-lg-6">
            <div class="card">
                <div class="card-header text-primary">✍ Submit Peer Review Scores (Double-Blind)</div>
                <div class="card-body">
                    {% if assignments %}
                    <form method="POST">
                        <input type="hidden" name="action" value="submit_review">
                        <div class="mb-3">
                            <label class="form-label fw-bold">Select Assigned Blinded Manuscript</label>
                            <select name="assignment_id" class="form-select" required>
                                {% for a in assignments %}
                                <option value="{{ a.assignment_id }}">
                                    Assignment #{{ a.assignment_id }}: "{{ a.paper_title }}" [Reviewer: {{ a.reviewer_name }}]
                                </option>
                                {% endfor %}
                            </select>
                            <small class="text-muted">Author identities are strictly concealed in double-blind mode.</small>
                        </div>
                        <div class="row g-2 mb-3">
                            <div class="col">
                                <label class="form-label small fw-bold">Originality (1-10)</label>
                                <input type="number" name="originality" class="form-control" min="1" max="10" value="8" required>
                            </div>
                            <div class="col">
                                <label class="form-label small fw-bold">Soundness (1-10)</label>
                                <input type="number" name="soundness" class="form-control" min="1" max="10" value="8" required>
                            </div>
                            <div class="col">
                                <label class="form-label small fw-bold">Clarity (1-10)</label>
                                <input type="number" name="clarity" class="form-control" min="1" max="10" value="8" required>
                            </div>
                            <div class="col">
                                <label class="form-label small fw-bold text-primary">Overall (1-10)</label>
                                <input type="number" name="overall_score" class="form-control" min="1" max="10" value="8" required>
                            </div>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">Public Constructive Feedback (Visible to Author)</label>
                            <textarea name="comments_for_author" class="form-control" rows="2" placeholder="Constructive remarks on methodology, proofs, and related work..." required></textarea>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold text-danger">Confidential Remarks (Chair Eyes Only)</label>
                            <textarea name="confidential_chair_comments" class="form-control" rows="2" placeholder="Private recommendation to the Program Chair..."></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">Submit Binding Review Scores</button>
                    </form>
                    {% else %}
                    <div class="p-4 text-center text-muted">
                        <h5>🎉 All reviews completed!</h5>
                        <p>There are no pending assignments waiting for review entry.</p>
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>

        <!-- Recent Completed Reviews -->
        <div class="col-lg-6">
            <div class="card">
                <div class="card-header">📋 Recent Submitted Reviews (Audit Log)</div>
                <div class="card-body p-0">
                    <table class="table table-hover mb-0">
                        <thead>
                            <tr>
                                <th>Paper</th>
                                <th>Reviewer</th>
                                <th>Orig</th>
                                <th>Sound</th>
                                <th>Clar</th>
                                <th>Overall</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for cr in completed_reviews %}
                            <tr>
                                <td class="small fw-bold">{{ cr.title[:35] }}...</td>
                                <td class="small">{{ cr.reviewer_name }}</td>
                                <td>{{ cr.originality }}</td>
                                <td>{{ cr.soundness }}</td>
                                <td>{{ cr.clarity }}</td>
                                <td><span class="badge bg-primary">{{ cr.overall_score }}</span></td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}
    """
    return render_template_string(template, title="Reviewer Portal", assignments=assignments, completed_reviews=completed_reviews)

# -----------------------------------------------------------------------------
# ROUTE 4: PROGRAM CHAIR (ASSIGNMENT, DECISIONS & SCHEDULING)
# -----------------------------------------------------------------------------
@app.route("/chair", methods=["GET", "POST"])
def chair_portal():
    conn = get_db()
    if request.method == "POST":
        action = request.form.get("action")
        
        # 1. ASSIGN REVIEWER WITH AUTOMATED COI CHECK
        if action == "assign_reviewer":
            paper_id = int(request.form.get("paper_id"))
            reviewer_id = int(request.form.get("reviewer_id"))
            due_date = request.form.get("due_date", "2026-11-01")

            # Check Conflict of Interest in database
            coi_check = conn.execute("""
                SELECT rc.conflict_type, au_u.first_name || ' ' || au_u.last_name AS author_name
                FROM Paper_Authors pa
                JOIN Authors a ON pa.author_id = a.author_id
                JOIN Users au_u ON a.user_id = au_u.user_id
                JOIN Reviewer_Conflicts rc ON pa.author_id = rc.author_id
                WHERE pa.paper_id = ? AND rc.reviewer_id = ?
            """, (paper_id, reviewer_id)).fetchone()

            if coi_check:
                flash(f"❌ INTEGRITY VIOLATION BLOCKED: Reviewer has an active Conflict of Interest ('{coi_check['conflict_type']}') with author {coi_check['author_name']}! Assignment aborted.", "danger")
            else:
                try:
                    conn.execute("INSERT INTO Paper_Assignments (paper_id, reviewer_id, due_date, status) VALUES (?, ?, ?, 'ASSIGNED')",
                                 (paper_id, reviewer_id, due_date))
                    conn.commit()
                    flash(f"✔ Reviewer successfully assigned to Paper #{paper_id}! Zero conflicts detected.", "success")
                except sqlite3.IntegrityError:
                    flash(f"Reviewer is already assigned to Paper #{paper_id}!", "warning")
            return redirect(url_for("chair_portal"))

        # 2. RECORD DECISION WITH 3-REVIEW QUOTA CHECK
        elif action == "record_decision":
            paper_id = int(request.form.get("paper_id"))
            decision_type = request.form.get("decision_type")
            summary = request.form.get("feedback_summary", "").strip()

            # Check review count quota
            rev_count = conn.execute("""
                SELECT COUNT(r.review_id)
                FROM Paper_Assignments pa
                JOIN Reviews r ON pa.assignment_id = r.assignment_id
                WHERE pa.paper_id = ?
            """, (paper_id,)).fetchone()[0]

            if rev_count < 3:
                flash(f"❌ DECISION BLOCKED: Paper #{paper_id} has only {rev_count} completed reviews! University business rule mandates at least 3 completed reviews before a decision can be recorded.", "danger")
            else:
                try:
                    # Insert decision and update status
                    conn.execute("INSERT INTO Decisions (paper_id, chair_id, decision_type, feedback_summary) VALUES (?, 1, ?, ?)",
                                 (paper_id, decision_type, summary))
                    conn.execute("UPDATE Papers SET status = ? WHERE paper_id = ?",
                                 ('ACCEPTED' if decision_type == 'ACCEPT' else 'REJECTED', paper_id))
                    conn.commit()
                    flash(f"✔ Program Committee verdict '{decision_type}' successfully logged for Paper #{paper_id}!", "success")
                except sqlite3.IntegrityError:
                    flash(f"A decision has already been logged for Paper #{paper_id}!", "warning")
            return redirect(url_for("chair_portal"))

    # Fetch papers, reviewers, decisions
    papers = conn.execute("SELECT * FROM vw_paper_scores").fetchall()
    reviewers = conn.execute("SELECT r.reviewer_id, u.first_name || ' ' || u.last_name AS name, u.affiliation FROM Reviewers r JOIN Users u ON r.user_id = u.user_id").fetchall()
    decisions = conn.execute("SELECT * FROM vw_decisions_summary").fetchall()
    conn.close()

    template = BASE_LAYOUT + """
    {% block content %}
    <h2 class="fw-bold mb-3" style="color: #1E3A8A;">Program Chair Editorial Control Panel</h2>

    <div class="row">
        <!-- Reviewer Assignment with COI Check -->
        <div class="col-lg-6">
            <div class="card">
                <div class="card-header">🛡 Automated Reviewer Assignment (COI Protected)</div>
                <div class="card-body">
                    <form method="POST">
                        <input type="hidden" name="action" value="assign_reviewer">
                        <div class="mb-3">
                            <label class="form-label fw-bold">Select Paper</label>
                            <select name="paper_id" class="form-select" required>
                                {% for p in papers %}
                                <option value="{{ p.paper_id }}">#{{ p.paper_id }}: {{ p.paper_title }} ({{ p.review_count }} reviews)</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">Candidate Reviewer</label>
                            <select name="reviewer_id" class="form-select" required>
                                {% for r in reviewers %}
                                <option value="{{ r.reviewer_id }}">{{ r.name }} ({{ r.affiliation }})</option>
                                {% endfor %}
                            </select>
                            <small class="text-muted">The system automatically evaluates COI tables before inserting.</small>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">Review Deadline</label>
                            <input type="date" name="due_date" class="form-control" value="2026-11-05" required>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">Verify COI & Assign Reviewer</button>
                    </form>
                </div>
            </div>
        </div>

        <!-- Decision Logging with Quota Check -->
        <div class="col-lg-6">
            <div class="card">
                <div class="card-header">⚖ Record Binding Editorial Verdict (Quota Protected)</div>
                <div class="card-body">
                    <form method="POST">
                        <input type="hidden" name="action" value="record_decision">
                        <div class="mb-3">
                            <label class="form-label fw-bold">Select Paper for Verdict</label>
                            <select name="paper_id" class="form-select" required>
                                {% for p in papers %}
                                <option value="{{ p.paper_id }}">
                                    #{{ p.paper_id }}: {{ p.paper_title }} [{{ p.review_count }} Reviews | Avg: {{ p.avg_overall_score or 'N/A' }}]
                                </option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">Verdict</label>
                            <select name="decision_type" class="form-select" required>
                                <option value="ACCEPT">ACCEPT (Oral Presentation)</option>
                                <option value="REJECT">REJECT</option>
                                <option value="MAJOR_REVISION">MAJOR REVISION</option>
                                <option value="MINOR_REVISION">MINOR REVISION</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">Chair Consensus Rationale</label>
                            <input type="text" name="feedback_summary" class="form-control" placeholder="Summary of Program Committee rationale..." required>
                        </div>
                        <button type="submit" class="btn btn-success w-100">Record Decision (Requires ≥ 3 Reviews)</button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <!-- Paper Scores & Decisions Summary -->
    <div class="card mt-3">
        <div class="card-header">📊 All Papers Composite Ratings & Editorial Decisions</div>
        <div class="card-body p-0">
            <table class="table table-hover mb-0">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Paper Title</th>
                        <th>Track</th>
                        <th>Reviews</th>
                        <th>Avg Score</th>
                        <th>Soundness</th>
                        <th>Clarity</th>
                        <th>Current Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for p in papers %}
                    <tr>
                        <td class="fw-bold">#{{ p.paper_id }}</td>
                        <td><strong>{{ p.paper_title }}</strong></td>
                        <td class="small">{{ p.track_name }}</td>
                        <td>
                            {% if p.review_count >= 3 %}
                                <span class="badge bg-success">{{ p.review_count }} (Quota Met)</span>
                            {% else %}
                                <span class="badge bg-warning text-dark">{{ p.review_count }} (Under Quota)</span>
                            {% endif %}
                        </td>
                        <td><strong>{{ p.avg_overall_score or '-' }}</strong></td>
                        <td>{{ p.avg_soundness or '-' }}</td>
                        <td>{{ p.avg_clarity or '-' }}</td>
                        <td>
                            {% if p.current_status == 'ACCEPTED' %}
                                <span class="badge bg-success">ACCEPTED</span>
                            {% elif p.current_status == 'REJECTED' %}
                                <span class="badge bg-danger">REJECTED</span>
                            {% else %}
                                <span class="badge bg-warning text-dark">{{ p.current_status }}</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    {% endblock %}
    """
    return render_template_string(template, title="Program Chair Portal", papers=papers, reviewers=reviewers, decisions=decisions)

# -----------------------------------------------------------------------------
# ROUTE 5: PRESENTATION TIMETABLE & SCHEDULING
# -----------------------------------------------------------------------------
@app.route("/schedule", methods=["GET", "POST"])
def schedule_page():
    conn = get_db()
    if request.method == "POST":
        paper_id = int(request.form.get("paper_id"))
        session_id = int(request.form.get("session_id"))
        slot_date = request.form.get("slot_date")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")

        # Validate non-overlapping author presentation schedule
        overlap_check = conn.execute("""
            SELECT ps.paper_id, p_other.title, ps.start_time, ps.end_time, s.room_no
            FROM Presentation_Slots ps
            JOIN Sessions s ON ps.session_id = s.session_id
            JOIN Papers p_other ON ps.paper_id = p_other.paper_id
            JOIN Paper_Authors pa_existing ON ps.paper_id = pa_existing.paper_id
            JOIN Paper_Authors pa_new ON pa_new.author_id = pa_existing.author_id
            WHERE pa_new.paper_id = ?
              AND ps.slot_date = ?
              AND ps.paper_id != ?
              AND (
                  (? >= ps.start_time AND ? < ps.end_time) OR
                  (? > ps.start_time AND ? <= ps.end_time)
              )
        """, (paper_id, slot_date, paper_id, start_time, start_time, end_time, end_time)).fetchone()

        if overlap_check:
            flash(f"❌ SCHEDULING COLLISION BLOCKED: An author of this paper is already scheduled in {overlap_check['room_no']} ({overlap_check['start_time']} - {overlap_check['end_time']}) for '{overlap_check['title']}'!", "danger")
        else:
            try:
                conn.execute("""
                    INSERT INTO Presentation_Slots (session_id, paper_id, slot_date, start_time, end_time, presentation_order)
                    VALUES (?, ?, ?, ?, ?, 1)
                """, (session_id, paper_id, slot_date, start_time, end_time))
                conn.commit()
                flash(f"✔ Presentation slot successfully booked for Paper #{paper_id}!", "success")
            except sqlite3.IntegrityError:
                flash(f"Paper #{paper_id} is already scheduled in a presentation slot!", "warning")
        return redirect(url_for("schedule_page"))

    timetable = conn.execute("SELECT * FROM vw_programme_schedule").fetchall()
    accepted_unassigned = conn.execute("""
        SELECT p.paper_id, p.title 
        FROM Papers p 
        WHERE p.status = 'ACCEPTED' 
          AND p.paper_id NOT IN (SELECT paper_id FROM Presentation_Slots)
    """).fetchall()
    sessions = conn.execute("SELECT * FROM Sessions").fetchall()
    conn.close()

    template = BASE_LAYOUT + """
    {% block content %}
    <h2 class="fw-bold mb-3" style="color: #1E3A8A;">Conference Master Timetable & Slot Allocation</h2>

    <div class="row mb-4">
        <!-- Slot Allocation Form -->
        <div class="col-lg-5">
            <div class="card">
                <div class="card-header">📅 Schedule Accepted Paper into Session</div>
                <div class="card-body">
                    {% if accepted_unassigned %}
                    <form method="POST">
                        <div class="mb-3">
                            <label class="form-label fw-bold">Accepted Paper</label>
                            <select name="paper_id" class="form-select" required>
                                {% for ap in accepted_unassigned %}
                                <option value="{{ ap.paper_id }}">#{{ ap.paper_id }}: {{ ap.title }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">Conference Session</label>
                            <select name="session_id" class="form-select" required>
                                {% for s in sessions %}
                                <option value="{{ s.session_id }}">{{ s.session_title }} ({{ s.room_no }})</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">Presentation Date</label>
                            <input type="date" name="slot_date" class="form-control" value="2026-11-16" required>
                        </div>
                        <div class="row g-2 mb-3">
                            <div class="col">
                                <label class="form-label small fw-bold">Start Time</label>
                                <input type="time" name="start_time" class="form-control" value="14:00" required>
                            </div>
                            <div class="col">
                                <label class="form-label small fw-bold">End Time</label>
                                <input type="time" name="end_time" class="form-control" value="14:30" required>
                            </div>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">Validate & Book Presentation Slot</button>
                    </form>
                    {% else %}
                    <div class="p-3 text-center text-success">
                        <h6>All accepted papers have been scheduled!</h6>
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>

        <!-- Master Schedule Table -->
        <div class="col-lg-7">
            <div class="card">
                <div class="card-header">🏛 Official Conference Programme Schedule (`vw_programme_schedule`)</div>
                <div class="card-body p-0">
                    <table class="table table-hover mb-0">
                        <thead>
                            <tr>
                                <th>Time & Date</th>
                                <th>Hall / Room</th>
                                <th>Session & Chair</th>
                                <th>Paper & Presenter</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for row in timetable %}
                            <tr>
                                <td class="small fw-bold">
                                    {{ row.slot_date }}<br>
                                    <span class="text-primary">{{ row.start_time }} - {{ row.end_time }}</span>
                                </td>
                                <td><span class="badge bg-secondary">{{ row.room_no }}</span></td>
                                <td>
                                    <strong>{{ row.session_title }}</strong><br>
                                    <span class="text-muted small">Chair: {{ row.session_chair }}</span>
                                </td>
                                <td>
                                    <strong class="text-dark">{{ row.paper_title }}</strong><br>
                                    <span class="text-muted small">Presenter: {{ row.presenter_name }} ({{ row.affiliation }})</span>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}
    """
    return render_template_string(template, title="Conference Timetable", timetable=timetable, accepted_unassigned=accepted_unassigned, sessions=sessions)

if __name__ == "__main__":
    print("Academic Conference DBMS Web Application running on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
