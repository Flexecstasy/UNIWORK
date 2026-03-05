-- UniWork Database Schema
-- Campus Job and Internship Platform
-- Generated for DrawSQL visualization

-- ============================================================================
-- USERS TABLE (Base for authentication)
-- ============================================================================
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK(role IN ('student', 'employer')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- STUDENT PROFILE (One-to-One with users)
-- ============================================================================
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    specialty VARCHAR(255),
    year INTEGER,
    phone VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================================
-- EMPLOYER PROFILE (One-to-One with users)
-- ============================================================================
CREATE TABLE employers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    organization_name VARCHAR(255) NOT NULL,
    department VARCHAR(255),
    contact_person VARCHAR(255),
    phone VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================================
-- CATEGORIES (Job categories)
-- ============================================================================
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    description VARCHAR(255),
    icon VARCHAR(50)
);

-- ============================================================================
-- JOBS (Job listings from employers)
-- ============================================================================
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employer_id INTEGER NOT NULL,
    category_id INTEGER,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    salary REAL,
    job_type VARCHAR(50) NOT NULL DEFAULT 'internship' CHECK(job_type IN ('internship', 'part_time', 'assistant')),
    status VARCHAR(50) NOT NULL DEFAULT 'open' CHECK(status IN ('open', 'closed')),
    deadline DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employer_id) REFERENCES employers(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);

-- ============================================================================
-- APPLICATIONS (Student applications to jobs)
-- ============================================================================
CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    resume_id INTEGER,
    cover TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'accepted', 'rejected')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE SET NULL
);

-- ============================================================================
-- RESUMES (Student resumes)
-- ============================================================================
CREATE TABLE resumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- ============================================================================
-- REVIEWS (Reviews between students and employers)
-- ============================================================================
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    employer_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
    text TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (employer_id) REFERENCES employers(id) ON DELETE CASCADE
);

-- ============================================================================
-- MESSAGES (Direct messages between users)
-- ============================================================================
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================================
-- NOTIFICATIONS (User notifications)
-- ============================================================================
CREATE TABLE notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    text VARCHAR(255) NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================================
-- INDEXES for performance
-- ============================================================================
CREATE INDEX idx_students_user_id ON students(user_id);
CREATE INDEX idx_employers_user_id ON employers(user_id);
CREATE INDEX idx_jobs_employer_id ON jobs(employer_id);
CREATE INDEX idx_jobs_category_id ON jobs(category_id);
CREATE INDEX idx_applications_student_id ON applications(student_id);
CREATE INDEX idx_applications_job_id ON applications(job_id);
CREATE INDEX idx_resumes_student_id ON resumes(student_id);
CREATE INDEX idx_reviews_student_id ON reviews(student_id);
CREATE INDEX idx_reviews_employer_id ON reviews(employer_id);
CREATE INDEX idx_messages_sender_id ON messages(sender_id);
CREATE INDEX idx_messages_receiver_id ON messages(receiver_id);
CREATE INDEX idx_notifications_user_id ON notifications(user_id);

