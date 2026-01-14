"""
Database Update Script - Add Missing Indexes and Constraints
This script adds the pharmacy_status index to existing databases
Run this after updating the codebase to improve query performance
"""

import sqlite3
import sys

def update_database(db_path='clinical_management.db'):
    """Add missing indexes to existing database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"Updating database: {db_path}")
        
        # Add pharmacy_status index if it doesn't exist
        try:
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_prescriptions_pharmacy_status ON prescriptions(pharmacy_status)')
            print("✓ Added index: idx_prescriptions_pharmacy_status")
        except sqlite3.Error as e:
            print(f"✗ Error adding pharmacy_status index: {e}")
        
        # Note: Cannot add UNIQUE constraint to existing table without recreating it
        # The unique constraint for consultations will be applied to new databases
        print("\nNote: Unique constraint for consultations (patient_id, status) will only apply to new databases.")
        print("Existing databases will continue to work but may allow duplicate consultation entries.")
        print("To apply the constraint, backup and recreate the database using models/database.py")
        
        conn.commit()
        conn.close()
        
        print("\n✓ Database update completed successfully!")
        return True
        
    except sqlite3.Error as e:
        print(f"\n✗ Database error: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False

if __name__ == '__main__':
    db_file = sys.argv[1] if len(sys.argv) > 1 else 'clinical_management.db'
    success = update_database(db_file)
    sys.exit(0 if success else 1)
