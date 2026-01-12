#!/usr/bin/env python3
"""
Database Backup Utility
Automatically creates timestamped backups of the clinical management database
"""

import os
import shutil
from datetime import datetime
import sys

def backup_database():
    """Create a timestamped backup of the database"""
    
    # Database file
    db_file = 'clinical_management.db'
    
    # Check if database exists
    if not os.path.exists(db_file):
        print(f"ERROR: Database file '{db_file}' not found!")
        return False
    
    # Create backups directory if it doesn't exist
    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"Created backups directory: {backup_dir}")
    
    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_dir, f'clinical_management_backup_{timestamp}.db')
    
    try:
        # Copy database file
        shutil.copy2(db_file, backup_file)
        file_size = os.path.getsize(backup_file)
        print(f"✓ Backup created successfully!")
        print(f"  File: {backup_file}")
        print(f"  Size: {file_size:,} bytes")
        
        # Clean up old backups (keep last 30)
        cleanup_old_backups(backup_dir, keep=30)
        
        return True
    except Exception as e:
        print(f"ERROR: Failed to create backup: {e}")
        return False

def cleanup_old_backups(backup_dir, keep=30):
    """Remove old backup files, keeping only the most recent ones"""
    try:
        # Get all backup files sorted by modification time
        backup_files = []
        for filename in os.listdir(backup_dir):
            if filename.startswith('clinical_management_backup_') and filename.endswith('.db'):
                filepath = os.path.join(backup_dir, filename)
                backup_files.append((filepath, os.path.getmtime(filepath)))
        
        # Sort by modification time (newest first)
        backup_files.sort(key=lambda x: x[1], reverse=True)
        
        # Remove old backups
        removed_count = 0
        for filepath, _ in backup_files[keep:]:
            try:
                os.remove(filepath)
                removed_count += 1
            except Exception as e:
                print(f"Warning: Could not remove old backup {filepath}: {e}")
        
        if removed_count > 0:
            print(f"  Cleaned up {removed_count} old backup(s)")
            
    except Exception as e:
        print(f"Warning: Error during backup cleanup: {e}")

def list_backups():
    """List all available backups"""
    backup_dir = 'backups'
    
    if not os.path.exists(backup_dir):
        print("No backups found.")
        return
    
    backup_files = []
    for filename in os.listdir(backup_dir):
        if filename.startswith('clinical_management_backup_') and filename.endswith('.db'):
            filepath = os.path.join(backup_dir, filename)
            size = os.path.getsize(filepath)
            mtime = os.path.getmtime(filepath)
            backup_files.append((filename, size, mtime))
    
    if not backup_files:
        print("No backups found.")
        return
    
    backup_files.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\nAvailable backups ({len(backup_files)}):")
    print("-" * 70)
    for filename, size, mtime in backup_files:
        date_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        print(f"  {filename}")
        print(f"    Date: {date_str}  |  Size: {size:,} bytes")

if __name__ == '__main__':
    print("Clinical Management System - Database Backup")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == 'list':
        list_backups()
    else:
        if backup_database():
            print("\nBackup completed successfully!")
        else:
            print("\nBackup failed!")
            sys.exit(1)
