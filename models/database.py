import sqlite3
from flask import g, current_app
from werkzeug.security import generate_password_hash

def get_db():
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
            payment_method TEXT,
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
    
    # Create exams table
    db.execute('''
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consultation_id INTEGER NOT NULL,
            patient_id INTEGER NOT NULL,
            presenting_complaint TEXT,
            history_of_complaint TEXT,
            random_blood_sugar INTEGER DEFAULT 0,
            fasting_blood_sugar INTEGER DEFAULT 0,
            liver_function INTEGER DEFAULT 0,
            full_blood_count INTEGER DEFAULT 0,
            lipid_profile INTEGER DEFAULT 0,
            kidney_function INTEGER DEFAULT 0,
            thyroid_function INTEGER DEFAULT 0,
            urinalysis INTEGER DEFAULT 0,
            stool_examination INTEGER DEFAULT 0,
            chest_xray INTEGER DEFAULT 0,
            ecg INTEGER DEFAULT 0,
            ultrasound INTEGER DEFAULT 0,
            recommend_diagnosis INTEGER DEFAULT 0,
            clinical_details TEXT,
            status TEXT DEFAULT 'pending',
            created_by TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (consultation_id) REFERENCES consultations (id) ON DELETE CASCADE,
            FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
        )
    ''')
    
    # Create laboratory table
    db.execute('''
        CREATE TABLE IF NOT EXISTS laboratory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_id INTEGER NOT NULL,
            patient_id INTEGER NOT NULL,
            test_name TEXT NOT NULL,
            test_result_image TEXT,
            clinical_details TEXT,
            general_comments TEXT,
            status TEXT DEFAULT 'in_lab',
            processed_by TEXT,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (exam_id) REFERENCES exams (id) ON DELETE CASCADE,
            FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
        )
    ''')
    
    # Create diagnoses table
    db.execute('''
        CREATE TABLE IF NOT EXISTS diagnoses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consultation_id INTEGER NOT NULL,
            patient_id INTEGER NOT NULL,
            confirmed_diagnosis TEXT NOT NULL,
            test_feedbacks TEXT,
            lab_tech_comment TEXT,
            diagnosis_notes TEXT,
            diagnosed_by TEXT NOT NULL,
            diagnosed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (consultation_id) REFERENCES consultations (id) ON DELETE CASCADE,
            FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
        )
    ''')
    
    # Create prescriptions table
    db.execute('''
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consultation_id INTEGER NOT NULL,
            patient_id INTEGER NOT NULL,
            medicines TEXT NOT NULL,
            prescription_comment TEXT,
            management_plan TEXT,
            prescribed_by TEXT NOT NULL,
            prescribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending',
            pharmacy_status TEXT DEFAULT 'not_sent',
            FOREIGN KEY (consultation_id) REFERENCES consultations (id) ON DELETE CASCADE,
            FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
        )
    ''')
    
    # Create indexes for foreign keys to improve query performance
    db.execute('CREATE INDEX IF NOT EXISTS idx_vitals_patient_id ON vitals(patient_id)')
    db.execute('CREATE INDEX IF NOT EXISTS idx_appointments_patient_id ON appointments(patient_id)')
    db.execute('CREATE INDEX IF NOT EXISTS idx_consultations_patient_id ON consultations(patient_id)')
    db.execute('CREATE INDEX IF NOT EXISTS idx_consultations_status ON consultations(status)')
    db.execute('CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(date)')
    db.execute('CREATE INDEX IF NOT EXISTS idx_exams_patient_id ON exams(patient_id)')
    db.execute('CREATE INDEX IF NOT EXISTS idx_exams_consultation_id ON exams(consultation_id)')
    db.execute('CREATE INDEX IF NOT EXISTS idx_laboratory_exam_id ON laboratory(exam_id)')
    db.execute('CREATE INDEX IF NOT EXISTS idx_laboratory_patient_id ON laboratory(patient_id)')
    db.execute('CREATE INDEX IF NOT EXISTS idx_diagnoses_patient_id ON diagnoses(patient_id)')
    db.execute('CREATE INDEX IF NOT EXISTS idx_diagnoses_consultation_id ON diagnoses(consultation_id)')
    db.execute('CREATE INDEX IF NOT EXISTS idx_prescriptions_patient_id ON prescriptions(patient_id)')
    db.execute('CREATE INDEX IF NOT EXISTS idx_prescriptions_consultation_id ON prescriptions(consultation_id)')
    
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
        
        print("\n" + "="*70)
        print("  SECURITY WARNING: Default credentials created!")
        print("="*70)
        print("  Admin - Username: admin, Password: admin123")
        print("  Nurse - Username: nurse1, Password: nurse123")
        print("\n  ⚠️  IMPORTANT: Change these passwords immediately in production!")
        print("="*70 + "\n")
    
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