-- =============================================================================
-- DATABASE SCHEMA, ADVANCED QUERIES & VIEWS: REVIEW 2 MILESTONE
-- Course: Database Management Systems (CS304)
-- Compatible with: PostgreSQL 14+ / MySQL 8.0+ / SQLite 3.35+
-- =============================================================================

-- =============================================================================
-- SECTION 1: PHYSICAL SCHEMA DDL (17 NORMALIZED TABLES)
-- =============================================================================

DROP VIEW IF EXISTS vw_track_statistics;
DROP VIEW IF EXISTS vw_programme_schedule;
DROP VIEW IF EXISTS vw_accepted_papers;
DROP VIEW IF EXISTS vw_decisions_summary;
DROP VIEW IF EXISTS vw_paper_scores;
DROP VIEW IF EXISTS vw_reviewer_workload;
DROP VIEW IF EXISTS vw_pending_reviews;

DROP TABLE IF EXISTS Presentation_Slots;
DROP TABLE IF EXISTS Sessions;
DROP TABLE IF EXISTS Registrations;
DROP TABLE IF EXISTS Decisions;
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS Paper_Assignments;
DROP TABLE IF EXISTS Paper_Versions;
DROP TABLE IF EXISTS Paper_Authors;
DROP TABLE IF EXISTS Papers;
DROP TABLE IF EXISTS Reviewer_Conflicts;
DROP TABLE IF EXISTS Reviewer_Expertise;
DROP TABLE IF EXISTS Reviewers;
DROP TABLE IF EXISTS Authors;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Topics;
DROP TABLE IF EXISTS Tracks;
DROP TABLE IF EXISTS Conferences;

CREATE TABLE Conferences (
    conference_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    acronym VARCHAR(30) NOT NULL,
    year INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    location VARCHAR(255) NOT NULL,
    submission_deadline DATE NOT NULL,
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

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(80) NOT NULL,
    last_name VARCHAR(80) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    affiliation VARCHAR(200) NOT NULL,
    country VARCHAR(80) NOT NULL,
    role VARCHAR(30) NOT NULL DEFAULT 'AUTHOR',
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
-- SECTION 2: B-TREE PERFORMANCE INDEXES
-- =============================================================================

CREATE INDEX idx_papers_track ON Papers(track_id);
CREATE INDEX idx_papers_status ON Papers(status);
CREATE INDEX idx_asgn_reviewer ON Paper_Assignments(reviewer_id);
CREATE INDEX idx_asgn_paper ON Paper_Assignments(paper_id);
CREATE INDEX idx_rev_asgn ON Reviews(assignment_id);
CREATE INDEX idx_slots_paper ON Presentation_Slots(paper_id);

-- =============================================================================
-- SECTION 3: REALISTIC SAMPLE DATA INSERTION (DML)
-- =============================================================================

INSERT INTO Conferences (title, acronym, year, start_date, end_date, location, submission_deadline) VALUES
('IEEE International Conference on Distributed Systems & AI 2026', 'ICDSAI', 2026, '2026-11-15', '2026-11-18', 'San Francisco, CA, USA', '2026-08-30');

INSERT INTO Tracks (conference_id, track_name, description) VALUES
(1, 'AI & Machine Learning', 'Deep learning, LLMs, reinforcement learning and neural models'),
(1, 'Cloud & Distributed Systems', 'Consensus protocols, serverless, microservices and edge architectures'),
(1, 'Cybersecurity & Privacy', 'Applied cryptography, blockchain security, network defense'),
(1, 'Software Engineering', 'Automated testing, DevOps, program synthesis and formal verification');

INSERT INTO Topics (track_id, topic_name, keywords) VALUES
(1, 'Large Language Models', 'transformers, attention, quantization, scaling laws'),
(1, 'Federated Learning', 'differential privacy, distributed gradients, edge optimization'),
(2, 'Consensus Protocols', 'paxos, raft, Byzantine fault tolerance, finality'),
(2, 'Serverless Architecture', 'FaaS, cold starts, resource scheduling, autoscaling'),
(3, 'Zero-Knowledge Proofs', 'zk-SNARKs, verifiable computation, cryptographic proofs'),
(3, 'Blockchain Systems', 'layer 2, rollups, smart contracts, decentralized consensus'),
(4, 'Automated Test Generation', 'fuzzing, symbolic execution, mutation testing'),
(4, 'Program Synthesis', 'AI-assisted code generation, formal semantics, correctness');

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

INSERT INTO Authors (user_id, orcid_id, bio) VALUES
(3, '0000-0002-1825-0097', 'Pioneer in deep neural networks and representation learning.'),
(4, '0000-0003-4567-8901', 'Inventor of convolutional networks and self-supervised learning.'),
(5, '0000-0001-2345-6789', 'Researcher in attention mechanisms and generative AI models.'),
(6, '0000-0004-9876-5432', 'Founder of DeepLearning.AI and Adjunct Professor at Stanford.');

INSERT INTO Reviewers (user_id, max_workload, is_active) VALUES
(7, 5, 1),
(8, 4, 1),
(9, 5, 1),
(10, 4, 1),
(11, 5, 1),
(12, 4, 1);

INSERT INTO Reviewer_Expertise (reviewer_id, topic_id, expertise_level) VALUES
(1, 3, 'EXPERT'),
(1, 4, 'KNOWLEDGEABLE'),
(2, 4, 'EXPERT'),
(2, 3, 'EXPERT'),
(3, 5, 'EXPERT'),
(3, 6, 'EXPERT'),
(4, 7, 'EXPERT'),
(4, 2, 'KNOWLEDGEABLE'),
(5, 7, 'EXPERT'),
(5, 8, 'EXPERT'),
(6, 8, 'EXPERT');

INSERT INTO Reviewer_Conflicts (reviewer_id, author_id, conflict_type) VALUES
(1, 1, 'SAME_INSTITUTION'),
(2, 4, 'CO_AUTHOR'),
(3, 2, 'ADVISORY');

INSERT INTO Papers (track_id, primary_author_id, title, abstract, status) VALUES
(1, 1, 'Energy-Efficient Quantization for Distributed LLM Inference', 'We introduce an 8-bit hybrid quantization framework reducing memory bandwidth by 42% while preserving 99.8% model perplexity.', 'ACCEPTED'),
(1, 2, 'Self-Supervised Contrastive Representation Learning across Distributed Graph Nodes', 'This paper develops an invariant contrastive loss function suitable for asynchronous node classification.', 'ACCEPTED'),
(2, 3, 'Optimistic Consensus in High-Throughput Byzantine Distributed Ledgers', 'We introduce BFT-Opt, a leaderless consensus protocol achieving sub-second finality under partial synchrony.', 'ACCEPTED'),
(3, 4, 'Zero-Knowledge Succinct Verification for Layer-2 Rollups', 'We formulate a recursive proof composition technique providing sub-linear verification time for transactions.', 'ACCEPTED'),
(4, 1, 'Automated Symbolic Fuzzing for Microservice API Boundaries', 'A boundary-directed greybox fuzzer identifying state violation vulnerabilities in distributed microservices.', 'REJECTED'),
(2, 2, 'Adaptive Autoscaling in Serverless Compute Clouds', 'Dynamic cold-start mitigation using predictive kernel pre-warming.', 'UNDER_REVIEW');

INSERT INTO Paper_Authors (paper_id, author_id, author_order, is_corresponding) VALUES
(1, 1, 1, 1),
(1, 2, 2, 0),
(2, 2, 1, 1),
(3, 3, 1, 1),
(4, 4, 1, 1),
(5, 1, 1, 1),
(5, 3, 2, 0),
(6, 2, 1, 1);

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

INSERT INTO Paper_Assignments (paper_id, reviewer_id, due_date, status) VALUES
(1, 2, '2026-10-01', 'COMPLETED'),
(1, 4, '2026-10-01', 'COMPLETED'),
(1, 5, '2026-10-01', 'COMPLETED'),
(2, 1, '2026-10-01', 'COMPLETED'),
(2, 4, '2026-10-01', 'COMPLETED'),
(2, 6, '2026-10-01', 'COMPLETED'),
(3, 1, '2026-10-01', 'COMPLETED'),
(3, 2, '2026-10-01', 'COMPLETED'),
(3, 5, '2026-10-01', 'COMPLETED'),
(4, 3, '2026-10-01', 'COMPLETED'),
(4, 5, '2026-10-01', 'COMPLETED'),
(4, 6, '2026-10-01', 'COMPLETED'),
(5, 4, '2026-10-01', 'COMPLETED'),
(5, 5, '2026-10-01', 'COMPLETED'),
(5, 6, '2026-10-01', 'COMPLETED'),
(6, 1, '2026-10-20', 'COMPLETED'),
(6, 2, '2026-10-20', 'ASSIGNED'),
(6, 3, '2026-10-20', 'ASSIGNED');

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

INSERT INTO Decisions (paper_id, chair_id, decision_type, feedback_summary) VALUES
(1, 1, 'ACCEPT', 'Consensus recommendation: Accept as Regular Oral Presentation.'),
(2, 1, 'ACCEPT', 'Consensus recommendation: Accept as Regular Oral Presentation.'),
(3, 1, 'ACCEPT', 'Consensus recommendation: Accept as Regular Oral Presentation.'),
(4, 1, 'ACCEPT', 'Consensus recommendation: Accept as Regular Oral Presentation.'),
(5, 1, 'REJECT', 'Consensus recommendation: Reject due to limited novelty and weak empirical benchmarking.');

INSERT INTO Registrations (conference_id, user_id, paper_id, registration_type, payment_status, amount_paid, transaction_ref) VALUES
(1, 3, 1, 'REGULAR_AUTHOR', 'PAID', 650.00, 'TXN_IEEE_2026_01'),
(1, 4, 2, 'REGULAR_AUTHOR', 'PAID', 650.00, 'TXN_IEEE_2026_02'),
(1, 5, 3, 'REGULAR_AUTHOR', 'PAID', 650.00, 'TXN_IEEE_2026_03'),
(1, 6, 4, 'REGULAR_AUTHOR', 'PAID', 650.00, 'TXN_IEEE_2026_04');

INSERT INTO Sessions (conference_id, track_id, session_title, session_date, room_no, session_chair) VALUES
(1, 1, 'Session 1A: Next-Gen Neural Architectures', '2026-11-16', 'Hall A - Main Auditorium', 'Dr. Barbara Liskov'),
(1, 2, 'Session 2A: High-Throughput Consensus Systems', '2026-11-16', 'Hall B - West Wing', 'Dr. Leslie Lamport'),
(1, 3, 'Session 3A: Applied Zero-Knowledge Cryptography', '2026-11-17', 'Hall C - Innovation Lab', 'Dr. Shafi Goldwasser');

INSERT INTO Presentation_Slots (session_id, paper_id, slot_date, start_time, end_time, presentation_order) VALUES
(1, 1, '2026-11-16', '09:30', '10:00', 1),
(1, 2, '2026-11-16', '10:00', '10:30', 2),
(2, 3, '2026-11-16', '11:00', '11:30', 1),
(3, 4, '2026-11-17', '14:00', '14:30', 1);

-- =============================================================================
-- SECTION 4: THE 7 ANALYTICAL VIEWS
-- =============================================================================

CREATE OR REPLACE VIEW vw_pending_reviews AS
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

CREATE OR REPLACE VIEW vw_reviewer_workload AS
SELECT 
    r.reviewer_id,
    u.first_name || ' ' || u.last_name AS reviewer_name,
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

CREATE OR REPLACE VIEW vw_paper_scores AS
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

CREATE OR REPLACE VIEW vw_decisions_summary AS
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

CREATE OR REPLACE VIEW vw_accepted_papers AS
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

CREATE OR REPLACE VIEW vw_programme_schedule AS
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

CREATE OR REPLACE VIEW vw_track_statistics AS
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

-- =============================================================================
-- SECTION 5: ADVANCED SQL DEMONSTRATION QUERIES
-- =============================================================================

-- Query 1: Multi-Table Join (Papers, Authors, Tracks, Versions)
SELECT 
    p.paper_id,
    p.title AS paper_title,
    t.track_name,
    u.first_name || ' ' || u.last_name AS primary_author,
    u.affiliation,
    COUNT(pv.version_id) AS total_versions,
    MAX(pv.is_camera_ready) AS has_camera_ready,
    p.status
FROM Papers p
JOIN Tracks t ON p.track_id = t.track_id
JOIN Authors a ON p.primary_author_id = a.author_id
JOIN Users u ON a.user_id = u.user_id
LEFT JOIN Paper_Versions pv ON p.paper_id = pv.paper_id
GROUP BY p.paper_id, p.title, t.track_name, u.first_name, u.last_name, u.affiliation, p.status
ORDER BY p.paper_id;

-- Query 2: Aggregate Scoring with GROUP BY and HAVING
SELECT 
    p.paper_id,
    p.title AS paper_title,
    COUNT(r.review_id) AS total_reviews,
    ROUND(AVG(r.originality), 2) AS avg_originality,
    ROUND(AVG(r.soundness), 2) AS avg_soundness,
    ROUND(AVG(r.clarity), 2) AS avg_clarity,
    ROUND(AVG(r.overall_score), 2) AS composite_avg_score,
    MIN(r.overall_score) AS min_rating,
    MAX(r.overall_score) AS max_rating
FROM Papers p
JOIN Paper_Assignments pa ON p.paper_id = pa.paper_id
JOIN Reviews r ON pa.assignment_id = r.assignment_id
GROUP BY p.paper_id, p.title
HAVING COUNT(r.review_id) >= 3 AND AVG(r.overall_score) >= 8.0
ORDER BY composite_avg_score DESC;

-- Query 3: Correlated Subquery with NOT EXISTS (Bottleneck Identification)
SELECT 
    p.paper_id,
    p.title AS paper_title,
    t.track_name,
    (SELECT COUNT(*) FROM Paper_Assignments pa WHERE pa.paper_id = p.paper_id AND pa.status = 'COMPLETED') AS completed_reviews,
    (SELECT COUNT(*) FROM Paper_Assignments pa WHERE pa.paper_id = p.paper_id AND pa.status = 'ASSIGNED') AS pending_reviews
FROM Papers p
JOIN Tracks t ON p.track_id = t.track_id
WHERE p.status = 'UNDER_REVIEW'
  AND NOT EXISTS (
      SELECT 1 FROM Decisions d 
      WHERE d.paper_id = p.paper_id
  );

-- Query 4: Correlated Subquery to Isolate Best Paper in Each Track
SELECT 
    p.paper_id,
    p.title AS paper_title,
    t.track_name,
    ROUND(AVG(r.overall_score), 2) AS track_best_score
FROM Papers p
JOIN Tracks t ON p.track_id = t.track_id
JOIN Paper_Assignments pa ON p.paper_id = pa.paper_id
JOIN Reviews r ON pa.assignment_id = r.assignment_id
GROUP BY p.paper_id, p.title, t.track_name
HAVING AVG(r.overall_score) = (
    SELECT MAX(sub.avg_score)
    FROM (
        SELECT AVG(r2.overall_score) AS avg_score
        FROM Papers p2
        JOIN Paper_Assignments pa2 ON p2.paper_id = pa2.paper_id
        JOIN Reviews r2 ON pa2.assignment_id = r2.assignment_id
        WHERE p2.track_id = p.track_id
        GROUP BY p2.paper_id
    ) sub
)
ORDER BY track_best_score DESC;
