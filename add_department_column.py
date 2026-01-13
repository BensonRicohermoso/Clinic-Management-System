import sqlite3

def add_department_column():
    """Add department column to patients table"""
    conn = sqlite3.connect('clinical_management.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('PRAGMA table_info(patients)')
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'department' not in columns:
            cursor.execute('ALTER TABLE patients ADD COLUMN department TEXT')
            conn.commit()
            print('✓ department column added successfully!')
        else:
            print('✓ department column already exists')
            
    except Exception as e:
        conn.rollback()
        print(f'✗ Error: {str(e)}')
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    add_department_column()
