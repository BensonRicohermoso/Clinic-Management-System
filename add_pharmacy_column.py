import sqlite3

def add_pharmacy_status_column():
    """Add pharmacy_status column to prescriptions table"""
    conn = sqlite3.connect('clinical_management.db')
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute('PRAGMA table_info(prescriptions)')
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'pharmacy_status' not in columns:
            # Add the column
            cursor.execute('ALTER TABLE prescriptions ADD COLUMN pharmacy_status TEXT DEFAULT "not_sent"')
            
            # Update existing records
            cursor.execute('UPDATE prescriptions SET pharmacy_status = "not_sent" WHERE pharmacy_status IS NULL')
            
            conn.commit()
            print('✓ pharmacy_status column added successfully!')
        else:
            print('✓ pharmacy_status column already exists')
            
    except Exception as e:
        conn.rollback()
        print(f'✗ Error: {str(e)}')
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    add_pharmacy_status_column()
