-- =============================================================================
-- DATABASE SCHEMA: ACADEMIC CONFERENCE PAPER SUBMISSION AND REVIEW SYSTEM
-- Course: Database Management Systems (CS304) | Review 1 Deliverable
-- Compatible with: PostgreSQL 14+ / MySQL 8.0+
-- =============================================================================

-- Drop tables in reverse order of foreign key dependency if they exist
DROP TABLE IF EXISTS Presentation_Slots;
DROP TABLE IF EXISTS Sessions;
DROP TABLE IF EXISTS Registrations;
DROP TABLE IF EXISTS Decisions;
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS Paper_Assignments;
DROP TABLE IF EXISTS Reviewer_Conflicts;
DROP TABLE IF EXISTS Reviewer_Expertise;
DROP TABLE IF EXISTS Reviewers;
DROP TABLE IF EXISTS Paper_Versions;
DROP TABLE IF EXISTS Paper_Authors;
DROP TABLE IF EXISTS Papers;
DROP TABLE IF EXISTS Authors;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Topics;
DROP TABLE IF EXISTS Tracks;
DROP TABLE IF EXISTS Conferences;

-- =============================================================================
-- MODULE 1: CONFERENCES, TRACKS & TOPICS
-- =============================================================================

CREATE TABLE Conferences (
    conference_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    acronym VARCHAR(30) NOT NULL,
    year INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    location VARCHAR(255) NOT NULL,
    submission_deadline DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_conf_acronym_year UNIQUE (acronym, year),
    CONSTRAINT chk_conf_dates CHECK (end_date >= start_date),
    CONSTRAINT chk_conf_deadline CHECK (submission_deadline <= start_date)
);

CREATE TABLE Tracks (
    track_id INT AUTO_INCREMENT PRIMARY KEY,
    conference_id INT NOT NULL,
    track_name VARCHAR(100) NOT NULL,
    description TEXT,
    CONSTRAINT fk_track_conference FOREIGN KEY (conference_id) 
        REFERENCES Conferences(conference_id) ON DELETE CASCADE,
    CONSTRAINT uk_track_name_per_conf UNIQUE (conference_id, track_name)
);

CREATE TABLE Topics (
    topic_id INT AUTO_INCREMENT PRIMARY KEY,
    track_id INT NOT NULL,
    topic_name VARCHAR(150) NOT NULL,
    keywords TEXT,
    CONSTRAINT fk_topic_track FOREIGN KEY (track_id) 
        REFERENCES Tracks(track_id) ON DELETE CASCADE,
    CONSTRAINT uk_topic_per_track UNIQUE (track_id, topic_name)
);

-- =============================================================================
-- MODULE 2: USERS, AUTHORS & REVIEWERS
-- =============================================================================

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(80) NOT NULL,
    last_name VARCHAR(80) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    affiliation VARCHAR(200) NOT NULL,
    country VARCHAR(80) NOT NULL,
    role VARCHAR(30) NOT NULL DEFAULT 'AUTHOR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_user_role CHECK (role IN ('CHAIR', 'TRACK_CHAIR', 'AUTHOR', 'REVIEWER', 'ATTENDEE', 'ADMIN'))
);

CREATE TABLE Authors (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    orcid_id VARCHAR(30),
    bio TEXT,
    CONSTRAINT fk_author_user FOREIGN KEY (user_id) 
        REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Reviewers (
    reviewer_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    max_workload INT NOT NULL DEFAULT 5,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_reviewer_user FOREIGN KEY (user_id) 
        REFERENCES Users(user_id) ON DELETE CASCADE,
    CONSTRAINT chk_reviewer_workload CHECK (max_workload > 0)
);

CREATE TABLE Reviewer_Expertise (
    reviewer_id INT NOT NULL,
    topic_id INT NOT NULL,
    expertise_level VARCHAR(30) NOT NULL DEFAULT 'KNOWLEDGEABLE',
    PRIMARY KEY (reviewer_id, topic_id),
    CONSTRAINT fk_exp_reviewer FOREIGN KEY (reviewer_id) 
        REFERENCES Reviewers(reviewer_id) ON DELETE CASCADE,
    CONSTRAINT fk_exp_topic FOREIGN KEY (topic_id) 
        REFERENCES Topics(topic_id) ON DELETE CASCADE,
    CONSTRAINT chk_exp_level CHECK (expertise_level IN ('EXPERT', 'KNOWLEDGEABLE', 'INFORMED'))
);

CREATE TABLE Reviewer_Conflicts (
    conflict_id INT AUTO_INCREMENT PRIMARY KEY,
    reviewer_id INT NOT NULL,
    author_id INT NOT NULL,
    conflict_type VARCHAR(50) NOT NULL,
    declared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_conf_reviewer FOREIGN KEY (reviewer_id) 
        REFERENCES Reviewers(reviewer_id) ON DELETE CASCADE,
    CONSTRAINT fk_conf_author FOREIGN KEY (author_id) 
        REFERENCES Authors(author_id) ON DELETE CASCADE,
    CONSTRAINT uk_reviewer_author_conflict UNIQUE (reviewer_id, author_id),
    CONSTRAINT chk_conflict_type CHECK (conflict_type IN ('CO_AUTHOR', 'SAME_INSTITUTION', 'ADVISORY', 'PERSONAL_RELATION', 'OTHER'))
);

-- =============================================================================
-- MODULE 3: PAPERS, VERSIONS & CO-AUTHORS
-- =============================================================================

CREATE TABLE Papers (
    paper_id INT AUTO_INCREMENT PRIMARY KEY,
    track_id INT NOT NULL,
    primary_author_id INT NOT NULL,
    title VARCHAR(300) NOT NULL,
    abstract TEXT NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'SUBMITTED',
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_paper_track FOREIGN KEY (track_id) 
        REFERENCES Tracks(track_id) ON DELETE RESTRICT,
    CONSTRAINT fk_paper_primary_author FOREIGN KEY (primary_author_id) 
        REFERENCES Authors(author_id) ON DELETE RESTRICT,
    CONSTRAINT chk_paper_status CHECK (status IN ('SUBMITTED', 'UNDER_REVIEW', 'REVISION_REQUESTED', 'ACCEPTED', 'REJECTED', 'WITHDRAWN'))
);

CREATE TABLE Paper_Authors (
    paper_id INT NOT NULL,
    author_id INT NOT NULL,
    author_order INT NOT NULL,
    is_corresponding BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (paper_id, author_id),
    CONSTRAINT fk_pa_paper FOREIGN KEY (paper_id) 
        REFERENCES Papers(paper_id) ON DELETE CASCADE,
    CONSTRAINT fk_pa_author FOREIGN KEY (author_id) 
        REFERENCES Authors(author_id) ON DELETE RESTRICT,
    CONSTRAINT chk_author_order CHECK (author_order >= 1),
    CONSTRAINT uk_paper_author_order UNIQUE (paper_id, author_order)
);

CREATE TABLE Paper_Versions (
    version_id INT AUTO_INCREMENT PRIMARY KEY,
    paper_id INT NOT NULL,
    version_num INT NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    changelog TEXT,
    is_camera_ready BOOLEAN NOT NULL DEFAULT FALSE,
    upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_version_paper FOREIGN KEY (paper_id) 
        REFERENCES Papers(paper_id) ON DELETE CASCADE,
    CONSTRAINT uk_paper_version_num UNIQUE (paper_id, version_num),
    CONSTRAINT chk_version_num CHECK (version_num >= 1)
);

-- =============================================================================
-- MODULE 4: ASSIGNMENTS & REVIEWS
-- =============================================================================

CREATE TABLE Paper_Assignments (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    paper_id INT NOT NULL,
    reviewer_id INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date DATE NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'ASSIGNED',
    CONSTRAINT fk_asgn_paper FOREIGN KEY (paper_id) 
        REFERENCES Papers(paper_id) ON DELETE CASCADE,
    CONSTRAINT fk_asgn_reviewer FOREIGN KEY (reviewer_id) 
        REFERENCES Reviewers(reviewer_id) ON DELETE RESTRICT,
    CONSTRAINT uk_paper_reviewer UNIQUE (paper_id, reviewer_id),
    CONSTRAINT chk_asgn_status CHECK (status IN ('ASSIGNED', 'ACCEPTED', 'DECLINED', 'COMPLETED'))
);

CREATE TABLE Reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    assignment_id INT NOT NULL UNIQUE,
    originality INT NOT NULL,
    soundness INT NOT NULL,
    clarity INT NOT NULL,
    overall_score INT NOT NULL,
    comments_for_author TEXT NOT NULL,
    confidential_chair_comments TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_rev_assignment FOREIGN KEY (assignment_id) 
        REFERENCES Paper_Assignments(assignment_id) ON DELETE RESTRICT,
    CONSTRAINT chk_rev_originality CHECK (originality BETWEEN 1 AND 10),
    CONSTRAINT chk_rev_soundness CHECK (soundness BETWEEN 1 AND 10),
    CONSTRAINT chk_rev_clarity CHECK (clarity BETWEEN 1 AND 10),
    CONSTRAINT chk_rev_overall CHECK (overall_score BETWEEN 1 AND 10)
);

-- =============================================================================
-- MODULE 5: EDITORIAL DECISIONS, REGISTRATIONS & PRESENTATION SCHEDULING
-- =============================================================================

CREATE TABLE Decisions (
    decision_id INT AUTO_INCREMENT PRIMARY KEY,
    paper_id INT NOT NULL UNIQUE,
    chair_id INT NOT NULL,
    decision_type VARCHAR(30) NOT NULL,
    feedback_summary TEXT,
    decision_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_dec_paper FOREIGN KEY (paper_id) 
        REFERENCES Papers(paper_id) ON DELETE RESTRICT,
    CONSTRAINT fk_dec_chair FOREIGN KEY (chair_id) 
        REFERENCES Users(user_id) ON DELETE RESTRICT,
    CONSTRAINT chk_dec_type CHECK (decision_type IN ('ACCEPT', 'REJECT', 'MAJOR_REVISION', 'MINOR_REVISION'))
);

CREATE TABLE Registrations (
    registration_id INT AUTO_INCREMENT PRIMARY KEY,
    conference_id INT NOT NULL,
    user_id INT NOT NULL,
    paper_id INT,
    registration_type VARCHAR(40) NOT NULL,
    payment_status VARCHAR(30) NOT NULL DEFAULT 'PENDING',
    amount_paid DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    transaction_ref VARCHAR(100),
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_reg_conference FOREIGN KEY (conference_id) 
        REFERENCES Conferences(conference_id) ON DELETE RESTRICT,
    CONSTRAINT fk_reg_user FOREIGN KEY (user_id) 
        REFERENCES Users(user_id) ON DELETE RESTRICT,
    CONSTRAINT fk_reg_paper FOREIGN KEY (paper_id) 
        REFERENCES Papers(paper_id) ON DELETE SET NULL,
    CONSTRAINT chk_reg_type CHECK (registration_type IN ('STUDENT_AUTHOR', 'REGULAR_AUTHOR', 'ACADEMIC_ATTENDEE', 'INDUSTRY_ATTENDEE')),
    CONSTRAINT chk_reg_payment CHECK (payment_status IN ('PAID', 'PENDING', 'WAIVED', 'REFUNDED')),
    CONSTRAINT chk_reg_amount CHECK (amount_paid >= 0.00)
);

CREATE TABLE Sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    conference_id INT NOT NULL,
    track_id INT NOT NULL,
    session_title VARCHAR(200) NOT NULL,
    session_date DATE NOT NULL,
    room_no VARCHAR(50) NOT NULL,
    session_chair VARCHAR(150),
    CONSTRAINT fk_sess_conference FOREIGN KEY (conference_id) 
        REFERENCES Conferences(conference_id) ON DELETE CASCADE,
    CONSTRAINT fk_sess_track FOREIGN KEY (track_id) 
        REFERENCES Tracks(track_id) ON DELETE RESTRICT,
    CONSTRAINT uk_sess_room_time UNIQUE (conference_id, session_date, room_no, session_title)
);

CREATE TABLE Presentation_Slots (
    slot_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    paper_id INT NOT NULL UNIQUE,
    slot_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    presentation_order INT NOT NULL,
    CONSTRAINT fk_slot_session FOREIGN KEY (session_id) 
        REFERENCES Sessions(session_id) ON DELETE CASCADE,
    CONSTRAINT fk_slot_paper FOREIGN KEY (paper_id) 
        REFERENCES Papers(paper_id) ON DELETE RESTRICT,
    CONSTRAINT chk_slot_duration CHECK (end_time > start_time),
    CONSTRAINT uk_session_presentation_order UNIQUE (session_id, presentation_order)
);

-- =============================================================================
-- PERFORMANCE INDEXES
-- =============================================================================

CREATE INDEX idx_papers_track ON Papers(track_id);
CREATE INDEX idx_papers_status ON Papers(status);
CREATE INDEX idx_assignments_reviewer ON Paper_Assignments(reviewer_id);
CREATE INDEX idx_assignments_paper ON Paper_Assignments(paper_id);
CREATE INDEX idx_reviews_assignment ON Reviews(assignment_id);
CREATE INDEX idx_versions_paper ON Paper_Versions(paper_id);
CREATE INDEX idx_slots_session ON Presentation_Slots(session_id);

-- =============================================================================
-- ANALYTICAL VIEWS
-- =============================================================================

-- View 1: Reviewer Workload Summary
CREATE OR REPLACE VIEW vw_reviewer_workload AS
SELECT 
    r.reviewer_id,
    CONCAT(u.first_name, ' ', u.last_name) AS reviewer_name,
    u.affiliation,
    r.max_workload,
    COUNT(pa.assignment_id) AS total_assigned_papers,
    SUM(CASE WHEN pa.status = 'COMPLETED' THEN 1 ELSE 0 END) AS completed_reviews,
    SUM(CASE WHEN pa.status = 'ASSIGNED' THEN 1 ELSE 0 END) AS pending_reviews,
    (r.max_workload - COUNT(pa.assignment_id)) AS remaining_capacity
FROM Reviewers r
JOIN Users u ON r.user_id = u.user_id
LEFT JOIN Paper_Assignments pa ON r.reviewer_id = pa.reviewer_id
GROUP BY r.reviewer_id, u.first_name, u.last_name, u.affiliation, r.max_workload;

-- View 2: Paper Evaluation & Score Aggregation
CREATE OR REPLACE VIEW vw_paper_scores AS
SELECT 
    p.paper_id,
    p.title,
    t.track_name,
    COUNT(r.review_id) AS review_count,
    ROUND(AVG(r.overall_score), 2) AS avg_overall_score,
    ROUND(AVG(r.originality), 2) AS avg_originality,
    ROUND(AVG(r.soundness), 2) AS avg_soundness,
    ROUND(AVG(r.clarity), 2) AS avg_clarity,
    MIN(r.overall_score) AS min_score,
    MAX(r.overall_score) AS max_score,
    p.status AS current_status,
    d.decision_type AS final_decision
FROM Papers p
JOIN Tracks t ON p.track_id = t.track_id
LEFT JOIN Paper_Assignments pa ON p.paper_id = pa.paper_id
LEFT JOIN Reviews r ON pa.assignment_id = r.assignment_id
LEFT JOIN Decisions d ON p.paper_id = d.paper_id
GROUP BY p.paper_id, p.title, t.track_name, p.status, d.decision_type;

-- View 3: Complete Conference Schedule & Timetable
CREATE OR REPLACE VIEW vw_conference_schedule AS
SELECT 
    s.session_date,
    s.room_no,
    s.session_title,
    s.session_chair,
    t.track_name,
    ps.presentation_order,
    ps.start_time,
    ps.end_time,
    p.paper_id,
    p.title AS paper_title,
    CONCAT(u.first_name, ' ', u.last_name) AS presenter_name,
    u.affiliation
FROM Presentation_Slots ps
JOIN Sessions s ON ps.session_id = s.session_id
JOIN Tracks t ON s.track_id = t.track_id
JOIN Papers p ON ps.paper_id = p.paper_id
JOIN Authors a ON p.primary_author_id = a.author_id
JOIN Users u ON a.user_id = u.user_id
ORDER BY s.session_date, s.room_no, ps.start_time;

-- =============================================================================
-- SAMPLE DATA INSERTION (FOR TESTING & VERIFICATION)
-- =============================================================================

-- 1. Conference
INSERT INTO Conferences (title, acronym, year, start_date, end_date, location, submission_deadline)
VALUES ('IEEE International Conference on Distributed Systems & AI 2026', 'ICDSAI', 2026, '2026-11-15', '2026-11-18', 'San Francisco, CA, USA', '2026-08-30');

-- 2. Tracks
INSERT INTO Tracks (conference_id, track_name, description) VALUES 
(1, 'Artificial Intelligence & Machine Learning', 'Deep learning, LLMs, reinforcement learning and neural architectures.'),
(1, 'Distributed & Cloud Systems', 'Consensus algorithms, microservices, edge computing and cloud orchestration.'),
(1, 'Cybersecurity & Privacy', 'Cryptography, blockchain, intrusion detection and zero-trust networks.');

-- 3. Topics
INSERT INTO Topics (track_id, topic_name, keywords) VALUES
(1, 'Large Language Model Architecture', 'transformer, attention, quantization, inference'),
(1, 'Federated Learning', 'privacy, distributed gradients, edge optimization'),
(2, 'Consensus Protocols', 'paxos, raft, Byzantine fault tolerance'),
(2, 'Serverless Computing', 'FaaS, cold start, autoscaling'),
(3, 'Zero-Knowledge Cryptography', 'zk-SNARKs, proof systems, verifiable computation'),
(3, 'Blockchain Scalability', 'sharding, layer 2, rollups');

-- 4. Users (Chairs, Authors, Reviewers)
INSERT INTO Users (first_name, last_name, email, password_hash, affiliation, country, role) VALUES
('Alan', 'Turing', 'chair@icdsai2026.org', 'pbkdf2_sha256$hash1', 'Cambridge University', 'UK', 'CHAIR'),
('Barbara', 'Liskov', 'trackchair@icdsai2026.org', 'pbkdf2_sha256$hash2', 'MIT', 'USA', 'TRACK_CHAIR'),
('Geoffrey', 'Hinton', 'author1@toronto.edu', 'pbkdf2_sha256$hash3', 'University of Toronto', 'Canada', 'AUTHOR'),
('Yann', 'LeCun', 'author2@nyu.edu', 'pbkdf2_sha256$hash4', 'New York University', 'USA', 'AUTHOR'),
('Yoshua', 'Bengio', 'author3@mila.quebec', 'pbkdf2_sha256$hash5', 'Mila / Univ of Montreal', 'Canada', 'AUTHOR'),
('Leslie', 'Lamport', 'reviewer1@microsoft.com', 'pbkdf2_sha256$hash6', 'Microsoft Research', 'USA', 'REVIEWER'),
('Michael', 'Stonebraker', 'reviewer2@mit.edu', 'pbkdf2_sha256$hash7', 'MIT CSAIL', 'USA', 'REVIEWER'),
('Shafi', 'Goldwasser', 'reviewer3@berkeley.edu', 'pbkdf2_sha256$hash8', 'UC Berkeley', 'USA', 'REVIEWER'),
('Andrew', 'Ng', 'reviewer4@stanford.edu', 'pbkdf2_sha256$hash9', 'Stanford University', 'USA', 'REVIEWER');

-- 5. Authors
INSERT INTO Authors (user_id, orcid_id, bio) VALUES
(3, '0000-0002-1825-0097', 'Pioneer in deep neural network architectures and backpropagation.'),
(4, '0000-0003-4567-8901', 'Inventor of convolutional neural networks and self-supervised learning.'),
(5, '0000-0001-2345-6789', 'Researcher in generative models, attention mechanisms, and deep architectures.');

-- 6. Reviewers
INSERT INTO Reviewers (user_id, max_workload, is_active) VALUES
(6, 4, TRUE),
(7, 5, TRUE),
(8, 5, TRUE),
(9, 4, TRUE);

-- 7. Reviewer Expertise
INSERT INTO Reviewer_Expertise (reviewer_id, topic_id, expertise_level) VALUES
(1, 3, 'EXPERT'),       -- Leslie Lamport in Consensus Protocols
(2, 4, 'EXPERT'),       -- Michael Stonebraker in Serverless/Data
(3, 5, 'EXPERT'),       -- Shafi Goldwasser in Cryptography
(4, 1, 'EXPERT'),       -- Andrew Ng in LLMs
(4, 2, 'KNOWLEDGEABLE');-- Andrew Ng in Federated Learning

-- 8. Reviewer Conflicts (COI)
INSERT INTO Reviewer_Conflicts (reviewer_id, author_id, conflict_type) VALUES
(4, 1, 'CO_AUTHOR');    -- Andrew Ng and Geoffrey Hinton are long-time academic collaborators

-- 9. Papers
INSERT INTO Papers (track_id, primary_author_id, title, abstract, status) VALUES
(1, 1, 'Energy-Efficient Quantization for Distributed LLM Inference', 'We present an 8-bit hybrid quantization framework that reduces memory bandwidth by 42% while retaining 99.8% model perplexity.', 'ACCEPTED'),
(1, 2, 'Self-Supervised Contrastive Representation Learning across Distributed Graph Nodes', 'This paper develops an invariant contrastive loss function suitable for asynchronous node classification.', 'ACCEPTED'),
(2, 3, 'Optimistic Consensus in High-Throughput Byzantine Distributed Ledgers', 'We introduce BFT-Opt, a leaderless consensus protocol providing sub-second finality under partial synchrony.', 'UNDER_REVIEW');

-- 10. Paper Authors
INSERT INTO Paper_Authors (paper_id, author_id, author_order, is_corresponding) VALUES
(1, 1, 1, TRUE),
(1, 2, 2, FALSE),
(2, 2, 1, TRUE),
(3, 3, 1, TRUE);

-- 11. Paper Versions
INSERT INTO Paper_Versions (paper_id, version_num, file_path, changelog, is_camera_ready) VALUES
(1, 1, '/uploads/papers/p1_v1_blind.pdf', 'Initial submission for double-blind peer review', FALSE),
(1, 2, '/uploads/papers/p1_v2_cameraready.pdf', 'Camera-ready copy including author details and affiliations', TRUE),
(2, 1, '/uploads/papers/p2_v1_blind.pdf', 'Initial submission for peer review', FALSE),
(2, 2, '/uploads/papers/p2_v2_cameraready.pdf', 'Camera-ready version incorporating reviewer feedback', TRUE),
(3, 1, '/uploads/papers/p3_v1_blind.pdf', 'Initial submission under review', FALSE);

-- 12. Paper Assignments (Enforcing no conflict: Reviewer 4 NOT assigned to Paper 1)
INSERT INTO Paper_Assignments (paper_id, reviewer_id, due_date, status) VALUES
(1, 1, '2026-10-01', 'COMPLETED'),
(1, 2, '2026-10-01', 'COMPLETED'),
(1, 3, '2026-10-01', 'COMPLETED'),
(2, 1, '2026-10-01', 'COMPLETED'),
(2, 2, '2026-10-01', 'COMPLETED'),
(2, 4, '2026-10-01', 'COMPLETED');

-- 13. Reviews (Scale 1-10)
INSERT INTO Reviews (assignment_id, originality, soundness, clarity, overall_score, comments_for_author, confidential_chair_comments) VALUES
(1, 9, 8, 9, 9, 'Outstanding contribution to low-precision inference on commodity hardware.', 'Clear accept; high technical value.'),
(2, 8, 9, 8, 8, 'Rigorous empirical evaluation on realistic distributed testbeds.', 'Solid paper; recommend acceptance.'),
(3, 9, 9, 8, 9, 'Strong theoretical proofs and exceptional clarity.', 'Top 5% paper; candidate for best paper award.'),
(4, 7, 8, 8, 8, 'Good graph formulation; slight concerns on asymptotic convergence.', 'Acceptable; minor revision needed.'),
(5, 8, 7, 8, 8, 'Very interesting approach to self-supervised multi-modal learning.', 'Accept.'),
(6, 9, 9, 9, 9, 'Excellent presentation and reproducible benchmark code.', 'Strong accept.');

-- 14. Decisions (P1 and P2 accepted; P3 under review)
INSERT INTO Decisions (paper_id, chair_id, decision_type, feedback_summary) VALUES
(1, 1, 'ACCEPT', 'Consensus recommendation: Accept as a regular oral presentation paper.'),
(2, 1, 'ACCEPT', 'Consensus recommendation: Accept as an oral presentation paper.');

-- 15. Registrations
INSERT INTO Registrations (conference_id, user_id, paper_id, registration_type, payment_status, amount_paid, transaction_ref) VALUES
(1, 3, 1, 'REGULAR_AUTHOR', 'PAID', 650.00, 'TXN_IEEE_2026_98712'),
(1, 4, 2, 'REGULAR_AUTHOR', 'PAID', 650.00, 'TXN_IEEE_2026_98713');

-- 16. Sessions
INSERT INTO Sessions (conference_id, track_id, session_title, session_date, room_no, session_chair) VALUES
(1, 1, 'Session 1A: Advanced Neural Architectures', '2026-11-16', 'Hall A - Main Auditorium', 'Dr. Barbara Liskov'),
(1, 1, 'Session 1B: Graph & Distributed Machine Learning', '2026-11-16', 'Hall B - West Wing', 'Dr. Michael Stonebraker');

-- 17. Presentation Slots (Conflict-free: P1 and P2 in distinct slots)
INSERT INTO Presentation_Slots (session_id, paper_id, slot_date, start_time, end_time, presentation_order) VALUES
(1, 1, '2026-11-16', '09:30:00', '10:00:00', 1),
(2, 2, '2026-11-16', '10:30:00', '11:00:00', 1);

-- =============================================================================
-- END OF SCHEMA SCRIPT
-- =============================================================================
