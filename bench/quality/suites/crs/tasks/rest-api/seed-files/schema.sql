-- User Management Database Schema

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('user', 'admin')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);

-- Constraints:
-- - email: must be valid email format, max 255 chars
-- - password: minimum 8 chars, must contain uppercase, lowercase, number
-- - full_name: 1-100 chars
-- - role: either 'user' or 'admin'

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- Seed admin user (password: Admin123!)
INSERT INTO users (email, password_hash, full_name, role) VALUES
('admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzqJOa/7G6', 'System Admin', 'admin');
