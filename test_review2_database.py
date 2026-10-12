import sqlite3
import os

def build_and_test_db():
    db_file = "conference_review2.db"
    if os.path.exists(db_file):
        os.remove(db_file)

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    # 1. DDL Statements (SQLite compatible ANSI SQL)
    ddl = """
    CREATE TABLE Conferences (
        conference_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        acronym TEXT NOT NULL,
        year INTEGER NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        location TEXT NOT NULL,
        submission_deadline DATE NOT NULL,
        UNIQUE (acronym, year),
        CHECK (end_date >= start_date)
    );

    CREATE TABLE Tracks (
        track_id INTEGER PRIMARY KEY AUTOINCREMENT,
        conference_id INTEGER NOT NULL REFERENCES Conferences(conference_id) ON DELETE CASCADE,
        track_name TEXT NOT NULL,
        description TEXT,
        UNIQUE (conference_id, track_name)
    );

    CREATE TABLE Topics (
        topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
        track_id INTEGER NOT NULL REFERENCES Tracks(track_id) ON DELETE CASCADE,
        topic_name TEXT NOT NULL,
        keywords TEXT,
        UNIQUE (track_id, topic_name)
    );

    CREATE TABLE Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        affiliation TEXT NOT NULL,
        country TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'AUTHOR',
        CHECK (role IN ('CHAIR', 'TRACK_CHAIR', 'AUTHOR', 'REVIEWER', 'ATTENDEE', 'ADMIN'))
    );

    CREATE TABLE Authors (
        author_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE REFERENCES Users(user_id) ON DELETE CASCADE,
        orcid_id TEXT,
        bio TEXT
    );

    CREATE TABLE Reviewers (
        reviewer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE REFERENCES Users(user_id) ON DELETE CASCADE,
        max_workload INTEGER NOT NULL DEFAULT 5,
        is_active INTEGER NOT NULL DEFAULT 1,
        CHECK (max_workload > 0)
    );

    CREATE TABLE Reviewer_Expertise (
        reviewer_id INTEGER NOT NULL REFERENCES Reviewers(reviewer_id) ON DELETE CASCADE,
        topic_id INTEGER NOT NULL REFERENCES Topics(topic_id) ON DELETE CASCADE,
        expertise_level TEXT NOT NULL DEFAULT 'KNOWLEDGEABLE',
        PRIMARY KEY (reviewer_id, topic_id),
        CHECK (expertise_level IN ('EXPERT', 'KNOWLEDGEABLE', 'INFORMED'))
    );

    CREATE TABLE Reviewer_Conflicts (
        conflict_id INTEGER PRIMARY KEY AUTOINCREMENT,
        reviewer_id INTEGER NOT NULL REFERENCES Reviewers(reviewer_id) ON DELETE CASCADE,
        author_id INTEGER NOT NULL REFERENCES Authors(author_id) ON DELETE CASCADE,
        conflict_type TEXT NOT NULL,
        declared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (reviewer_id, author_id),
        CHECK (conflict_type IN ('CO_AUTHOR', 'SAME_INSTITUTION', 'ADVISORY', 'PERSONAL_RELATION', 'OTHER'))
    );

    CREATE TABLE Papers (
        paper_id INTEGER PRIMARY KEY AUTOINCREMENT,
        track_id INTEGER NOT NULL REFERENCES Tracks(track_id) ON DELETE RESTRICT,
        primary_author_id INTEGER NOT NULL REFERENCES Authors(author_id) ON DELETE RESTRICT,
        title TEXT NOT NULL,
        abstract TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'SUBMITTED',
        submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CHECK (status IN ('SUBMITTED', 'UNDER_REVIEW', 'REVISION_REQUESTED', 'ACCEPTED', 'REJECTED', 'WITHDRAWN'))
    );

    CREATE TABLE Paper_Authors (
        paper_id INTEGER NOT NULL REFERENCES Papers(paper_id) ON DELETE CASCADE,
        author_id INTEGER NOT NULL REFERENCES Authors(author_id) ON DELETE RESTRICT,
        author_order INTEGER NOT NULL,
        is_corresponding INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY (paper_id, author_id),
        UNIQUE (paper_id, author_order),
        CHECK (author_order >= 1)
    );

    CREATE TABLE Paper_Versions (
        version_id INTEGER PRIMARY KEY AUTOINCREMENT,
        paper_id INTEGER NOT NULL REFERENCES Papers(paper_id) ON DELETE CASCADE,
        version_num INTEGER NOT NULL,
        file_path TEXT NOT NULL,
        changelog TEXT,
        is_camera_ready INTEGER NOT NULL DEFAULT 0,
        upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (paper_id, version_num),
        CHECK (version_num >= 1)
    );

    CREATE TABLE Paper_Assignments (
        assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        paper_id INTEGER NOT NULL REFERENCES Papers(paper_id) ON DELETE CASCADE,
        reviewer_id INTEGER NOT NULL REFERENCES Reviewers(reviewer_id) ON DELETE RESTRICT,
        assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        due_date DATE NOT NULL,
        status TEXT NOT NULL DEFAULT 'ASSIGNED',
        UNIQUE (paper_id, reviewer_id),
        CHECK (status IN ('ASSIGNED', 'ACCEPTED', 'DECLINED', 'COMPLETED'))
    );

    CREATE TABLE Reviews (
        review_id INTEGER PRIMARY KEY AUTOINCREMENT,
        assignment_id INTEGER NOT NULL UNIQUE REFERENCES Paper_Assignments(assignment_id) ON DELETE RESTRICT,
        originality INTEGER NOT NULL,
        soundness INTEGER NOT NULL,
        clarity INTEGER NOT NULL,
        overall_score INTEGER NOT NULL,
        comments_for_author TEXT NOT NULL,
        confidential_chair_comments TEXT,
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CHECK (originality BETWEEN 1 AND 10),
        CHECK (soundness BETWEEN 1 AND 10),
        CHECK (clarity BETWEEN 1 AND 10),
        CHECK (overall_score BETWEEN 1 AND 10)
    );

    CREATE TABLE Decisions (
        decision_id INTEGER PRIMARY KEY AUTOINCREMENT,
        paper_id INTEGER NOT NULL UNIQUE REFERENCES Papers(paper_id) ON DELETE RESTRICT,
        chair_id INTEGER NOT NULL REFERENCES Users(user_id) ON DELETE RESTRICT,
        decision_type TEXT NOT NULL,
        feedback_summary TEXT,
        decision_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CHECK (decision_type IN ('ACCEPT', 'REJECT', 'MAJOR_REVISION', 'MINOR_REVISION'))
    );

    CREATE TABLE Registrations (
        registration_id INTEGER PRIMARY KEY AUTOINCREMENT,
        conference_id INTEGER NOT NULL REFERENCES Conferences(conference_id) ON DELETE RESTRICT,
        user_id INTEGER NOT NULL REFERENCES Users(user_id) ON DELETE RESTRICT,
        paper_id INTEGER REFERENCES Papers(paper_id) ON DELETE SET NULL,
        registration_type TEXT NOT NULL,
        payment_status TEXT NOT NULL DEFAULT 'PENDING',
        amount_paid REAL NOT NULL DEFAULT 0.00,
        transaction_ref TEXT,
        registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CHECK (payment_status IN ('PAID', 'PENDING', 'WAIVED', 'REFUNDED')),
        CHECK (amount_paid >= 0.00)
    );

    CREATE TABLE Sessions (
        session_id INTEGER PRIMARY KEY AUTOINCREMENT,
        conference_id INTEGER NOT NULL REFERENCES Conferences(conference_id) ON DELETE CASCADE,
        track_id INTEGER NOT NULL REFERENCES Tracks(track_id) ON DELETE RESTRICT,
        session_title TEXT NOT NULL,
        session_date DATE NOT NULL,
        room_no TEXT NOT NULL,
        session_chair TEXT,
        UNIQUE (conference_id, session_date, room_no, session_title)
    );

    CREATE TABLE Presentation_Slots (
        slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER NOT NULL REFERENCES Sessions(session_id) ON DELETE CASCADE,
        paper_id INTEGER NOT NULL UNIQUE REFERENCES Papers(paper_id) ON DELETE RESTRICT,
        slot_date DATE NOT NULL,
        start_time TIME NOT NULL,
        end_time TIME NOT NULL,
        presentation_order INTEGER NOT NULL,
        CHECK (end_time > start_time),
        UNIQUE (session_id, presentation_order)
    );
    """
    cur.executescript(ddl)

    # 2. Indexes
    indexes = """
    CREATE INDEX idx_papers_track ON Papers(track_id);
    CREATE INDEX idx_papers_status ON Papers(status);
    CREATE INDEX idx_asgn_reviewer ON Paper_Assignments(reviewer_id);
    CREATE INDEX idx_asgn_paper ON Paper_Assignments(paper_id);
    CREATE INDEX idx_rev_asgn ON Reviews(assignment_id);
    CREATE INDEX idx_slots_paper ON Presentation_Slots(paper_id);
    """
    cur.executescript(indexes)

    # 3. Rich Realistic Data
    dml = """
    -- Conferences
    INSERT INTO Conferences (title, acronym, year, start_date, end_date, location, submission_deadline) VALUES
    ('IEEE International Conference on Distributed Systems & AI 2026', 'ICDSAI', 2026, '2026-11-15', '2026-11-18', 'San Francisco, CA, USA', '2026-08-30');

    -- Tracks
    INSERT INTO Tracks (conference_id, track_name, description) VALUES
    (1, 'AI & Machine Learning', 'Deep learning, LLMs, reinforcement learning and neural models'),
    (1, 'Cloud & Distributed Systems', 'Consensus protocols, serverless, microservices and edge architectures'),
    (1, 'Cybersecurity & Privacy', 'Applied cryptography, blockchain security, network defense'),
    (1, 'Software Engineering', 'Automated testing, DevOps, program synthesis and formal verification');

    -- Topics
    INSERT INTO Topics (track_id, topic_name, keywords) VALUES
    (1, 'Large Language Models', 'transformers, attention, quantization, scaling laws'),
    (1, 'Federated Learning', 'differential privacy, distributed gradients, edge optimization'),
    (2, 'Consensus Protocols', 'paxos, raft, Byzantine fault tolerance, finality'),
    (2, 'Serverless Architecture', 'FaaS, cold starts, resource scheduling, autoscaling'),
    (3, 'Zero-Knowledge Proofs', 'zk-SNARKs, verifiable computation, cryptographic proofs'),
    (3, 'Blockchain Systems', 'layer 2, rollups, smart contracts, decentralized consensus'),
    (4, 'Automated Test Generation', 'fuzzing, symbolic execution, mutation testing'),
    (4, 'Program Synthesis', 'AI-assisted code generation, formal semantics, correctness');

    -- Users (Chairs, Authors, Reviewers)
    INSERT INTO Users (first_name, last_name, email, password_hash, affiliation, country, role) VALUES
    ('Alan', 'Turing', 'turing@icdsai2026.org', 'hash1', 'Cambridge University', 'UK', 'CHAIR'),
    ('Barbara', 'Liskov', 'liskov@icdsai2026.org', 'hash2', 'MIT', 'USA', 'TRACK_CHAIR'),
    ('Geoffrey', 'Hinton', 'hinton@toronto.edu', 'hash3', 'University of Toronto', 'Canada', 'AUTHOR'),
    ('Yann', 'LeCun', 'lecun@nyu.edu', 'hash4', 'New York University', 'USA', 'AUTHOR'),
    ('Yoshua', 'Bengio', 'bengio@mila.quebec', 'hash5', 'Mila / Univ of Montreal', 'Canada', 'AUTHOR'),
    ('Andrew', 'Ng', 'ng@stanford.edu', 'hash6', 'Stanford University', 'USA', 'AUTHOR'),
    ('Leslie', 'Lamport', 'lamport@microsoft.com', 'hash7', 'Microsoft Research', 'USA', 'REVIEWER'),
    ('Michael', 'Stonebraker', 'stonebraker@mit.edu', 'hash8', 'MIT CSAIL', 'USA', 'REVIEWER'),
    ('Shafi', 'Goldwasser', 'shafi@berkeley.edu', 'hash9', 'UC Berkeley', 'USA', 'REVIEWER'),
    ('Linus', 'Torvalds', 'torvalds@linux.org', 'hash10', 'Linux Foundation', 'USA', 'REVIEWER'),
    ('Margaret', 'Hamilton', 'hamilton@mit.edu', 'hash11', 'Hamilton Technologies', 'USA', 'REVIEWER'),
    ('Grace', 'Hopper', 'hopper@navy.mil', 'hash12', 'Yale University', 'USA', 'REVIEWER');

    -- Authors (Users 3, 4, 5, 6)
    INSERT INTO Authors (user_id, orcid_id, bio) VALUES
    (3, '0000-0002-1825-0097', 'Pioneer in deep neural networks and representation learning.'),
    (4, '0000-0003-4567-8901', 'Inventor of convolutional networks and self-supervised learning.'),
    (5, '0000-0001-2345-6789', 'Researcher in attention mechanisms and generative AI models.'),
    (6, '0000-0004-9876-5432', 'Founder of DeepLearning.AI and Adjunct Professor at Stanford.');

    -- Reviewers (Users 7, 8, 9, 10, 11, 12)
    INSERT INTO Reviewers (user_id, max_workload, is_active) VALUES
    (7, 5, 1),
    (8, 4, 1),
    (9, 5, 1),
    (10, 4, 1),
    (11, 5, 1),
    (12, 4, 1);

    -- Reviewer Expertise
    INSERT INTO Reviewer_Expertise (reviewer_id, topic_id, expertise_level) VALUES
    (1, 3, 'EXPERT'),       -- Lamport in Consensus Protocols
    (1, 4, 'KNOWLEDGEABLE'),-- Lamport in Serverless
    (2, 4, 'EXPERT'),       -- Stonebraker in Serverless / Storage
    (2, 3, 'EXPERT'),       -- Stonebraker in Consensus
    (3, 5, 'EXPERT'),       -- Goldwasser in Zero-Knowledge Proofs
    (3, 6, 'EXPERT'),       -- Goldwasser in Blockchain
    (4, 7, 'EXPERT'),       -- Torvalds in Software / Systems
    (4, 2, 'KNOWLEDGEABLE'),-- Torvalds in Distributed Gradients
    (5, 7, 'EXPERT'),       -- Hamilton in Automated Testing
    (5, 8, 'EXPERT'),       -- Hamilton in Program Synthesis
    (6, 8, 'EXPERT');       -- Hopper in Compilers / Synthesis

    -- Reviewer Conflicts (COI)
    INSERT INTO Reviewer_Conflicts (reviewer_id, author_id, conflict_type) VALUES
    (1, 1, 'SAME_INSTITUTION'), -- Lamport & Hinton
    (2, 4, 'CO_AUTHOR'),        -- Stonebraker & Andrew Ng
    (3, 2, 'ADVISORY');         -- Goldwasser & Yann LeCun

    -- Papers
    INSERT INTO Papers (track_id, primary_author_id, title, abstract, status) VALUES
    (1, 1, 'Energy-Efficient Quantization for Distributed LLM Inference', 'We introduce an 8-bit hybrid quantization framework reducing memory bandwidth by 42% while preserving 99.8% model perplexity.', 'ACCEPTED'),
    (1, 2, 'Self-Supervised Contrastive Representation Learning across Distributed Graph Nodes', 'This paper develops an invariant contrastive loss function suitable for asynchronous node classification.', 'ACCEPTED'),
    (2, 3, 'Optimistic Consensus in High-Throughput Byzantine Distributed Ledgers', 'We introduce BFT-Opt, a leaderless consensus protocol achieving sub-second finality under partial synchrony.', 'ACCEPTED'),
    (3, 4, 'Zero-Knowledge Succinct Verification for Layer-2 Rollups', 'We formulate a recursive proof composition technique providing sub-linear verification time for transactions.', 'ACCEPTED'),
    (4, 1, 'Automated Symbolic Fuzzing for Microservice API Boundaries', 'A boundary-directed greybox fuzzer identifying state violation vulnerabilities in distributed microservices.', 'REJECTED'),
    (2, 2, 'Adaptive Autoscaling in Serverless Compute Clouds', 'Dynamic cold-start mitigation using predictive kernel pre-warming.', 'UNDER_REVIEW');

    -- Paper Authors
    INSERT INTO Paper_Authors (paper_id, author_id, author_order, is_corresponding) VALUES
    (1, 1, 1, 1),
    (1, 2, 2, 0),
    (2, 2, 1, 1),
    (3, 3, 1, 1),
    (4, 4, 1, 1),
    (5, 1, 1, 1),
    (5, 3, 2, 0),
    (6, 2, 1, 1);

    -- Paper Versions
    INSERT INTO Paper_Versions (paper_id, version_num, file_path, changelog, is_camera_ready) VALUES
    (1, 1, '/uploads/papers/p1_v1_blind.pdf', 'Initial submission for double-blind review', 0),
    (1, 2, '/uploads/papers/p1_v2_cameraready.pdf', 'Camera-ready version with author affiliations included', 1),
    (2, 1, '/uploads/papers/p2_v1_blind.pdf', 'Initial submission', 0),
    (2, 2, '/uploads/papers/p2_v2_cameraready.pdf', 'Camera-ready version incorporating reviewer feedback', 1),
    (3, 1, '/uploads/papers/p3_v1_blind.pdf', 'Initial submission', 0),
    (3, 2, '/uploads/papers/p3_v2_cameraready.pdf', 'Camera-ready version', 1),
    (4, 1, '/uploads/papers/p4_v1_blind.pdf', 'Initial submission', 0),
    (4, 2, '/uploads/papers/p4_v2_cameraready.pdf', 'Camera-ready version', 1),
    (5, 1, '/uploads/papers/p5_v1_blind.pdf', 'Initial submission', 0),
    (6, 1, '/uploads/papers/p6_v1_blind.pdf', 'Initial submission under review', 0);

    -- Paper Assignments
    INSERT INTO Paper_Assignments (paper_id, reviewer_id, due_date, status) VALUES
    -- Paper 1: Assigned to Reviewers 2, 4, 5 (Reviewer 1 has COI with Author 1)
    (1, 2, '2026-10-01', 'COMPLETED'),
    (1, 4, '2026-10-01', 'COMPLETED'),
    (1, 5, '2026-10-01', 'COMPLETED'),
    -- Paper 2: Assigned to Reviewers 1, 4, 6 (Reviewer 3 has COI with Author 2)
    (2, 1, '2026-10-01', 'COMPLETED'),
    (2, 4, '2026-10-01', 'COMPLETED'),
    (2, 6, '2026-10-01', 'COMPLETED'),
    -- Paper 3: Assigned to Reviewers 1, 2, 5
    (3, 1, '2026-10-01', 'COMPLETED'),
    (3, 2, '2026-10-01', 'COMPLETED'),
    (3, 5, '2026-10-01', 'COMPLETED'),
    -- Paper 4: Assigned to Reviewers 3, 5, 6 (Reviewer 2 has COI with Author 4)
    (4, 3, '2026-10-01', 'COMPLETED'),
    (4, 5, '2026-10-01', 'COMPLETED'),
    (4, 6, '2026-10-01', 'COMPLETED'),
    -- Paper 5: Assigned to Reviewers 4, 5, 6
    (5, 4, '2026-10-01', 'COMPLETED'),
    (5, 5, '2026-10-01', 'COMPLETED'),
    (5, 6, '2026-10-01', 'COMPLETED'),
    -- Paper 6: Under review - Reviewer 1 completed, Reviewers 2 & 3 pending
    (6, 1, '2026-10-20', 'COMPLETED'),
    (6, 2, '2026-10-20', 'ASSIGNED'),
    (6, 3, '2026-10-20', 'ASSIGNED');

    -- Reviews (Scores 1 to 10)
    INSERT INTO Reviews (assignment_id, originality, soundness, clarity, overall_score, comments_for_author, confidential_chair_comments) VALUES
    (1, 9, 8, 9, 9, 'Strong empirical results and reproducible benchmarks.', 'Clear accept; top paper.'),
    (2, 8, 9, 8, 8, 'Rigorous evaluation across heterogeneous nodes.', 'Solid technical value.'),
    (3, 9, 9, 9, 9, 'Excellent mathematical formulation and clear writing.', 'Recommend for best paper candidate.'),
    (4, 8, 8, 8, 8, 'Comprehensive contrastive learning formulation.', 'Accept.'),
    (5, 7, 8, 8, 8, 'Solid proofs on asynchronous convergence.', 'Good contribution.'),
    (6, 9, 8, 9, 9, 'Well structured presentation and novel loss formulation.', 'Strong accept.'),
    (7, 9, 9, 9, 9, 'Breakthrough consensus throughput under high latency.', 'Clear accept.'),
    (8, 8, 9, 8, 8, 'Thorough benchmarking against Raft and PBFT.', 'Accept.'),
    (9, 9, 8, 8, 8, 'Sound theoretical safety and liveness proofs.', 'Solid accept.'),
    (10, 9, 9, 9, 9, 'Highly practical recursive zk-rollup verification.', 'Strong accept; top crypto submission.'),
    (11, 8, 9, 8, 8, 'Very efficient cryptographic proofs.', 'Accept.'),
    (12, 9, 8, 9, 9, 'Clear presentation of recursive SNARKs.', 'Strong accept.'),
    (13, 5, 4, 5, 4, 'Limited novelty beyond existing greybox fuzzers.', 'Reject; weak evaluation.'),
    (14, 4, 5, 5, 5, 'Evaluation only done on synthetic microservices.', 'Reject.'),
    (15, 5, 5, 6, 5, 'Does not demonstrate real bug discoveries.', 'Weak reject.'),
    (16, 7, 7, 8, 7, 'Interesting cold-start caching heuristics.', 'Promising preliminary draft.');

    -- Decisions
    INSERT INTO Decisions (paper_id, chair_id, decision_type, feedback_summary) VALUES
    (1, 1, 'ACCEPT', 'Consensus recommendation: Accept as Regular Oral Presentation.'),
    (2, 1, 'ACCEPT', 'Consensus recommendation: Accept as Regular Oral Presentation.'),
    (3, 1, 'ACCEPT', 'Consensus recommendation: Accept as Regular Oral Presentation.'),
    (4, 1, 'ACCEPT', 'Consensus recommendation: Accept as Regular Oral Presentation.'),
    (5, 1, 'REJECT', 'Consensus recommendation: Reject due to limited novelty and weak empirical benchmarking.');

    -- Registrations (Accepted papers authors registered)
    INSERT INTO Registrations (conference_id, user_id, paper_id, registration_type, payment_status, amount_paid, transaction_ref) VALUES
    (1, 3, 1, 'REGULAR_AUTHOR', 'PAID', 650.00, 'TXN_IEEE_2026_01'),
    (1, 4, 2, 'REGULAR_AUTHOR', 'PAID', 650.00, 'TXN_IEEE_2026_02'),
    (1, 5, 3, 'REGULAR_AUTHOR', 'PAID', 650.00, 'TXN_IEEE_2026_03'),
    (1, 6, 4, 'REGULAR_AUTHOR', 'PAID', 650.00, 'TXN_IEEE_2026_04');

    -- Sessions
    INSERT INTO Sessions (conference_id, track_id, session_title, session_date, room_no, session_chair) VALUES
    (1, 1, 'Session 1A: Next-Gen Neural Architectures', '2026-11-16', 'Hall A - Main Auditorium', 'Dr. Barbara Liskov'),
    (1, 2, 'Session 2A: High-Throughput Consensus Systems', '2026-11-16', 'Hall B - West Wing', 'Dr. Leslie Lamport'),
    (1, 3, 'Session 3A: Applied Zero-Knowledge Cryptography', '2026-11-17', 'Hall C - Innovation Lab', 'Dr. Shafi Goldwasser');

    -- Presentation Slots
    INSERT INTO Presentation_Slots (session_id, paper_id, slot_date, start_time, end_time, presentation_order) VALUES
    (1, 1, '2026-11-16', '09:30', '10:00', 1),
    (1, 2, '2026-11-16', '10:00', '10:30', 2),
    (2, 3, '2026-11-16', '11:00', '11:30', 1),
    (3, 4, '2026-11-17', '14:00', '14:30', 1);
    """
    cur.executescript(dml)
    conn.commit()
    print("Database built and populated with 100% success!")

    # 4. Create and Test the 7 Views
    views = """
    -- View 1: Pending Reviews
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

    -- View 2: Reviewer Workload
    CREATE VIEW vw_reviewer_workload AS
    SELECT 
        r.reviewer_id,
        u.first_name || ' ' || u.last_name AS reviewer_name,
        u.affiliation,
        r.max_workload,
        COUNT(pa.assignment_id) AS total_assigned,
        SUM(CASE WHEN pa.status = 'COMPLETED' THEN 1 ELSE 0 END) AS completed_reviews,
        SUM(CASE WHEN pa.status = 'ASSIGNED' THEN 1 ELSE 0 END) AS pending_reviews,
        (r.max_workload - COUNT(pa.assignment_id)) AS remaining_capacity
    FROM Reviewers r
    JOIN Users u ON r.user_id = u.user_id
    LEFT JOIN Paper_Assignments pa ON r.reviewer_id = pa.reviewer_id
    GROUP BY r.reviewer_id, u.first_name, u.last_name, u.affiliation, r.max_workload;

    -- View 3: Paper Scores
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

    -- View 4: Decisions Summary
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

    -- View 5: Accepted Papers & Camera-Ready Status
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

    -- View 6: Conference Programme Timetable
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

    -- View 7: Track Statistics
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
    """
    cur.executescript(views)
    conn.commit()
    print("All 7 Views created successfully!")

    # 5. Execute and print samples from all 7 views to confirm
    for vname in ['vw_pending_reviews', 'vw_reviewer_workload', 'vw_paper_scores', 'vw_decisions_summary', 'vw_accepted_papers', 'vw_programme_schedule', 'vw_track_statistics']:
        cur.execute(f"SELECT * FROM {vname}")
        rows = cur.fetchall()
        print(f"-> View '{vname}': {len(rows)} rows retrieved.")

    conn.close()

if __name__ == "__main__":
    build_and_test_db()
