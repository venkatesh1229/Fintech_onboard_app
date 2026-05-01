-- ============================================================
-- schema.sql — MySQL Database Schema
-- ============================================================
-- Run this to set up the database from scratch:
--   mysql -u root -p < database/schema.sql
-- ============================================================

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS fintech_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE fintech_db;

-- ============================================================
-- TABLE: users — Merchant accounts
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    business_name   VARCHAR(200)  NOT NULL,
    contact_person  VARCHAR(100)  NOT NULL,
    mobile          VARCHAR(15)   NOT NULL UNIQUE,
    email           VARCHAR(100)  NOT NULL UNIQUE,
    business_type   ENUM('sole_proprietorship','partnership','pvt_ltd','llp','public_ltd') NOT NULL,
    pan_number      VARCHAR(10)   NOT NULL UNIQUE,
    gst_number      VARCHAR(15)   NOT NULL,
    services        VARCHAR(300)  NOT NULL,          -- Comma-separated: "PayIn,UPI"
    hashed_password VARCHAR(200)  NOT NULL,
    is_active       BOOLEAN       DEFAULT TRUE,
    created_at      DATETIME      DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
);

-- ============================================================
-- TABLE: merchant_applications — One application per merchant
-- ============================================================
CREATE TABLE IF NOT EXISTS merchant_applications (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    merchant_id  INT  NOT NULL,
    status       ENUM('pending','under_review','approved','rejected') DEFAULT 'pending',
    remarks      TEXT,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (merchant_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_status (status)
);

-- ============================================================
-- TABLE: documents — Uploaded files per application
-- ============================================================
CREATE TABLE IF NOT EXISTS documents (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    application_id INT          NOT NULL,
    doc_type       VARCHAR(50)  NOT NULL,     -- "pan_card", "gst_certificate", etc.
    file_name      VARCHAR(200) NOT NULL,     -- Original file name shown to admin
    file_path      VARCHAR(500) NOT NULL,     -- Server file path for download
    uploaded_at    DATETIME     DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES merchant_applications(id) ON DELETE CASCADE
);

-- ============================================================
-- TABLE: admin_users — Admin accounts (created manually)
-- ============================================================
CREATE TABLE IF NOT EXISTS admin_users (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    username        VARCHAR(50)  NOT NULL UNIQUE,
    email           VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(200) NOT NULL,
    is_superadmin   BOOLEAN      DEFAULT FALSE,
    created_at      DATETIME     DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- Seed: Default admin user
-- Password: admin123 (bcrypt hash — change this!)
-- To generate: python -c "from passlib.context import CryptContext; print(CryptContext(['bcrypt']).hash('admin123'))"
-- ============================================================
INSERT IGNORE INTO admin_users (username, email, hashed_password, is_superadmin)
VALUES (
    'admin',
    'admin@company.com',
    '$2b$12$examplehashchangethisbeforeproduction000000000000000000',
    TRUE
);
