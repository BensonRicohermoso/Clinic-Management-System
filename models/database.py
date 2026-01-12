# Database setup and connection

import sqlite3
from flask import g, current_app
from werkzeug.security import generate_password_hash

def get_db():
    # get or create db connection
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        # Enable foreign key constraints for CASCADE deletes
        g.db.execute('PRAGMA foreign_keys = ON')
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    # creates tables and default users
    db = get_db()
    
    # Create users table
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'nurse',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create patients table
    db.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            gender TEXT NOT NULL,
            blood_type TEXT,
            allergies TEXT,
            contact TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create vitals table
    db.execute('''
        CREATE TABLE IF NOT EXISTS vitals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            blood_pressure TEXT NOT NULL,
            heart_rate INTEGER NOT NULL,
            temperature REAL NOT NULL,
            respiratory_rate INTEGER NOT NULL,
            oxygen_saturation INTEGER,
            notes TEXT,
            recorded_by TEXT NOT NULL,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
        )
    ''')
    
    # Create appointments table
    db.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            date DATE NOT NULL,
            time TIME NOT NULL,
            reason TEXT NOT NULL,
            status TEXT DEFAULT 'scheduled',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
        )
    ''')
    
    # Create consultations table
    db.execute('''
        CREATE TABLE IF NOT EXISTS consultations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            status TEXT DEFAULT 'waiting',
            added_by TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
        )
    ''')
    
    # Check if default admin user exists
    admin = db.execute('SELECT * FROM users WHERE username = ?', ('admin',)).fetchone()
    
    if not admin:
        # Create default admin user (username: admin, password: admin123)
        db.execute(
            'INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)',
            ('admin', generate_password_hash('admin123'), 'System Administrator', 'admin')
        )
        
        # Create sample nurse user (username: nurse1, password: nurse123)
        db.execute(
            'INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)',
            ('nurse1', generate_password_hash('nurse123'), 'Nurse Jane Doe', 'nurse')
        )
        
        print("Default users created:")
        print("  Admin - Username: admin, Password: admin123")
        print("  Nurse - Username: nurse1, Password: nurse123")
    
    db.commit()

def seed_sample_data():
    # adds test patients if db is empty
    db = get_db()
    
    # Check if sample data already exists
    patient_count = db.execute('SELECT COUNT(*) as count FROM patients').fetchone()['count']
    
    if patient_count == 0:
        # Add sample patients
        sample_patients = [
            ('John Smith', '1980-03-15', 'Male', 'O+', 'Penicillin', '555-0101', '123 Main St'),
            ('Mary Johnson', '1963-07-22', 'Female', 'A+', 'None', '555-0102', '456 Oak Ave'),
            ('Robert Brown', '1987-11-08', 'Male', 'B-', 'Aspirin', '555-0103', '789 Pine Rd'),
            ('Patricia Davis', '1970-05-30', 'Female', 'AB+', 'Latex', '555-0104', '321 Elm St'),
            ('Michael Wilson', '1954-09-12', 'Male', 'O-', 'Sulfa drugs', '555-0105', '654 Maple Dr')
        ]
        
        for patient in sample_patients:
            db.execute(
                '''INSERT INTO patients (name, date_of_birth, gender, blood_type, allergies, contact, address)
                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
                patient
            )
        
        db.commit()
        print("Sample patient data added successfully!")

def init_app(app):
    app.teardown_appcontext(close_db)