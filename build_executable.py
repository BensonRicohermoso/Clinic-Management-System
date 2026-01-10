"""
Build Script for Creating Standalone Executable
This script automates the process of creating a distributable executable
using PyInstaller for the Clinical Management System.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
        return True
    except ImportError:
        print("✗ PyInstaller is not installed")
        return False

def install_pyinstaller():
    """Install PyInstaller"""
    print("→ Installing PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install PyInstaller")
        return False

def create_spec_file():
    """Create PyInstaller spec file with custom configuration"""
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('models', 'models'),
    ],
    hiddenimports=[
        'flask',
        'werkzeug',
        'jinja2',
        'sqlite3',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ClinicalCMS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
"""
    
    with open('ClinicalCMS.spec', 'w') as f:
        f.write(spec_content)
    print("✓ Spec file created: ClinicalCMS.spec")

def build_executable():
    """Build the executable using PyInstaller"""
    print("→ Building executable (this may take a few minutes)...")
    
    try:
        # Use the spec file for build
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "PyInstaller",
            "--clean",
            "--noconfirm",
            "ClinicalCMS.spec"
        ])
        print("✓ Build completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return False

def create_distribution_package():
    """Create a distribution package with executable and necessary files"""
    print("→ Creating distribution package...")
    
    dist_dir = Path("dist/ClinicalCMS_Package")
    
    # Create distribution directory
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir(parents=True)
    
    # Copy executable
    exe_name = "ClinicalCMS.exe" if sys.platform == "win32" else "ClinicalCMS"
    src_exe = Path("dist") / exe_name
    if src_exe.exists():
        shutil.copy2(src_exe, dist_dir / exe_name)
        print(f"  ✓ Copied executable: {exe_name}")
    
    # Copy README
    if Path("README.md").exists():
        shutil.copy2("README.md", dist_dir / "README.md")
        print("  ✓ Copied README.md")
    
    # Create templates directory in package
    templates_dir = dist_dir / "templates"
    if Path("templates").exists():
        shutil.copytree("templates", templates_dir)
        print("  ✓ Copied templates folder")
    
    # Create a startup script
    if sys.platform == "win32":
        startup_script = dist_dir / "START_CMS.bat"
        with open(startup_script, 'w') as f:
            f.write('@echo off\n')
            f.write('echo Starting Clinical Management System...\n')
            f.write(f'{exe_name}\n')
            f.write('pause\n')
        print("  ✓ Created START_CMS.bat")
    else:
        startup_script = dist_dir / "start_cms.sh"
        with open(startup_script, 'w') as f:
            f.write('#!/bin/bash\n')
            f.write('echo "Starting Clinical Management System..."\n')
            f.write(f'./{exe_name}\n')
        os.chmod(startup_script, 0o755)
        print("  ✓ Created start_cms.sh")
    
    # Create quick start guide
    quick_start = dist_dir / "QUICK_START.txt"
    with open(quick_start, 'w') as f:
        f.write("CLINICAL MANAGEMENT SYSTEM - QUICK START GUIDE\n")
        f.write("=" * 60 + "\n\n")
        f.write("1. STARTING THE APPLICATION\n")
        if sys.platform == "win32":
            f.write("   - Double-click START_CMS.bat\n")
        else:
            f.write("   - Run: ./start_cms.sh\n")
        f.write("\n2. ACCESS THE SYSTEM\n")
        f.write("   - Open browser: http://localhost:5000\n")
        f.write("\n3. DEFAULT LOGIN\n")
        f.write("   - Username: admin\n")
        f.write("   - Password: admin123\n")
        f.write("\n4. IMPORTANT NOTES\n")
        f.write("   - Change default password after first login\n")
        f.write("   - Database file will be created automatically\n")
        f.write("   - Backup the .db file regularly\n")
        f.write("\nFor full documentation, see README.md\n")
    print("  ✓ Created QUICK_START.txt")
    
    print(f"✓ Distribution package created: {dist_dir}")
    return dist_dir

def cleanup():
    """Clean up build artifacts"""
    print("→ Cleaning up build artifacts...")
    
    dirs_to_remove = ['build', '__pycache__']
    files_to_remove = ['ClinicalCMS.spec']
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  ✓ Removed: {dir_name}")
    
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"  ✓ Removed: {file_name}")

def main():
    """Main build process"""
    print_header("Clinical Management System - Build Script")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # Check/Install PyInstaller
    if not check_pyinstaller():
        if not install_pyinstaller():
            print("\n✗ Cannot proceed without PyInstaller")
            sys.exit(1)
    
    # Create spec file
    create_spec_file()
    
    # Build executable
    if not build_executable():
        print("\n✗ Build process failed")
        sys.exit(1)
    
    # Create distribution package
    dist_dir = create_distribution_package()
    
    # Cleanup
    cleanup()
    
    # Success message
    print_header("BUILD COMPLETED SUCCESSFULLY!")
    print(f"\n📦 Distribution package location:")
    print(f"   {dist_dir.absolute()}")
    print(f"\n📋 Next steps:")
    print(f"   1. Navigate to: {dist_dir}")
    if sys.platform == "win32":
        print(f"   2. Run: START_CMS.bat")
    else:
        print(f"   2. Run: ./start_cms.sh")
    print(f"   3. Open browser: http://localhost:5000")
    print(f"\n✅ Ready for distribution!\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Unexpected error: {e}")
        sys.exit(1)