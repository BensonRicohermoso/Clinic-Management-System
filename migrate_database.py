"""
Database Migration Script
Adds CHECK constraints and improves schema validation
"""

import sqlite3
import os

def migrate_database():
    """Add CHECK constraints to existing tables"""
    
    db_path = 'clinical_management.db'
    
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("Starting database migration...")
        
        # Enable foreign keys
        cursor.execute('PRAGMA foreign_keys = ON')
        
        # Check if consultations table has CHECK constraint
        # SQLite doesn't support adding CHECK constraints to existing tables,
        # so we'll create views or triggers instead
        
        # Create trigger to validate consultation status
        print("Creating consultation status validation trigger...")
        cursor.execute('''
            DROP TRIGGER IF EXISTS validate_consultation_status
        ''')
        cursor.execute('''
            CREATE TRIGGER validate_consultation_status
            BEFORE INSERT ON consultations
            FOR EACH ROW
            WHEN NEW.status NOT IN ('waiting', 'processing', 'sent_to_lab', 'completed')
            BEGIN
                SELECT RAISE(ABORT, 'Invalid consultation status. Must be: waiting, processing, sent_to_lab, or completed');
            END
        ''')
        
        cursor.execute('''
            DROP TRIGGER IF EXISTS validate_consultation_status_update
        ''')
        cursor.execute('''
            CREATE TRIGGER validate_consultation_status_update
            BEFORE UPDATE ON consultations
            FOR EACH ROW
            WHEN NEW.status NOT IN ('waiting', 'processing', 'sent_to_lab', 'completed')
            BEGIN
                SELECT RAISE(ABORT, 'Invalid consultation status. Must be: waiting, processing, sent_to_lab, or completed');
            END
        ''')
        
        # Create trigger to validate exam status
        print("Creating exam status validation trigger...")
        cursor.execute('''
            DROP TRIGGER IF EXISTS validate_exam_status
        ''')
        cursor.execute('''
            CREATE TRIGGER validate_exam_status
            BEFORE INSERT ON exams
            FOR EACH ROW
            WHEN NEW.status NOT IN ('pending', 'in_progress', 'completed', 'cancelled')
            BEGIN
                SELECT RAISE(ABORT, 'Invalid exam status. Must be: pending, in_progress, completed, or cancelled');
            END
        ''')
        
        cursor.execute('''
            DROP TRIGGER IF EXISTS validate_exam_status_update
        ''')
        cursor.execute('''
            CREATE TRIGGER validate_exam_status_update
            BEFORE UPDATE ON exams
            FOR EACH ROW
            WHEN NEW.status NOT IN ('pending', 'in_progress', 'completed', 'cancelled')
            BEGIN
                SELECT RAISE(ABORT, 'Invalid exam status. Must be: pending, in_progress, completed, or cancelled');
            END
        ''')
        
        # Create trigger to validate laboratory status
        print("Creating laboratory status validation trigger...")
        cursor.execute('''
            DROP TRIGGER IF EXISTS validate_laboratory_status
        ''')
        cursor.execute('''
            CREATE TRIGGER validate_laboratory_status
            BEFORE INSERT ON laboratory
            FOR EACH ROW
            WHEN NEW.status NOT IN ('pending', 'in_progress', 'completed')
            BEGIN
                SELECT RAISE(ABORT, 'Invalid laboratory status. Must be: pending, in_progress, or completed');
            END
        ''')
        
        cursor.execute('''
            DROP TRIGGER IF EXISTS validate_laboratory_status_update
        ''')
        cursor.execute('''
            CREATE TRIGGER validate_laboratory_status_update
            BEFORE UPDATE ON laboratory
            FOR EACH ROW
            WHEN NEW.status NOT IN ('pending', 'in_progress', 'completed')
            BEGIN
                SELECT RAISE(ABORT, 'Invalid laboratory status. Must be: pending, in_progress, or completed');
            END
        ''')
        
        # Create index for better query performance
        print("Creating performance indexes...")
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_consultations_status 
            ON consultations(status)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_exams_status 
            ON exams(status)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_laboratory_status 
            ON laboratory(status)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_exams_patient_id 
            ON exams(patient_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_laboratory_exam_id 
            ON laboratory(exam_id)
        ''')
        
        conn.commit()
        print("\n✓ Migration completed successfully!")
        print("✓ Status validation triggers created")
        print("✓ Performance indexes created")
        
    except Exception as e:
        conn.rollback()
        print(f"\n✗ Migration failed: {str(e)}")
        raise
    
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()
