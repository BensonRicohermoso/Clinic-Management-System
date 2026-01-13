# Clinical Management System

A comprehensive Flask-based healthcare management system for clinical workflows. Manages the complete patient journey from registration through consultation, laboratory testing, diagnosis, prescription, payment, and pharmacy dispensing.

## Features

- **Patient Management** - Complete registration with medical history, allergies, blood type
- **Vital Signs** - Track BP, HR, temperature, respiratory rate, SpO2 with timestamps
- **Appointment Scheduling** - Schedule, manage, and track patient appointments
- **Consultation Queue** - Real-time consultation management with status tracking
- **Exam System** - Order laboratory tests (blood work, imaging, urinalysis, etc.)
- **Laboratory** - Upload and manage test results with images and clinical details
- **Diagnosis** - Record diagnosis with lab result feedback and clinical notes
- **Prescription** - Digital prescription with multiple medicines, dosage, and treatment plans
- **Account & Payment** - Payment processing with multiple payment methods
- **Pharmacy** - Medicine dispensing workflow with prescription verification
- **Patient History** - Complete medical history view with all encounters
- **Dashboard Analytics** - Real-time statistics and recent activity
- **User Authentication** - Secure login with role-based access
- **Automated Backups** - Database backup system with 30-day retention
- **Data Validation** - Comprehensive input validation and sanitization

## Setup

1. Install Python 3.8+

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment (optional but recommended):

```bash
# Copy the example environment file
copy .env.example .env

# Edit .env and set your SECRET_KEY
# Generate a secure key: python -c "import secrets; print(secrets.token_hex(32))"
```

4. Run the app:

```bash
python app.py
```

5. Open browser to `http://127.0.0.1:5000`

## Login

Default accounts (created on first run):

- Admin: `admin` / `admin123`
- Nurse: `nurse1` / `nurse123`

**⚠️ SECURITY WARNING:** Change these passwords immediately in production!

## Security Best Practices

### Before Production Deployment:

1. **Change Default Passwords**

   - Log in as admin and change the default password
   - Update or remove the default nurse account

2. **Set Environment Variables**

   - Generate a strong SECRET_KEY
   - Set DATABASE_PATH if using custom location
   - Never commit .env file to version control

3. **Database Backups**

   - Run regular backups: `python backup_database.py`
   - Backups are stored in `backups/` directory
   - List backups: `python backup_database.py list`
   - Automatic cleanup keeps last 30 backups

4. **Network Security**

   - Use HTTPS in production (set SESSION_COOKIE_SECURE=True)
   - Configure firewall to restrict access
   - Use strong passwords for all accounts

5. **Data Validation**
   - All inputs are validated on both client and server side
   - Blood pressure: 50-250 / 30-160 mmHg
   - Temperature: 32-45°C
   - Foreign key constraints enabled for data integrity

## Tech Stack

- Python/Flask 3.0+
- SQLite with foreign key constraints
- Tailwind CSS
- Font Awesome icons
- HTML5 form validation

## Project Structure

```
├── app.py              # main application
├── models/
│   └── database.py     # database setup
├── templates/          # HTML files
└── static/            # images, etc
```

## Complete Clinical Workflow

### 1. Patient Registration

- Add patient demographics, contact info, allergies, blood type
- View and edit patient profiles
- Add to consultation queue

### 2. Vitals Recording

- Record BP, heart rate, temperature, respiratory rate, oxygen saturation
- Add clinical notes
- Track vital sign history

### 3. Consultation

- Manage waiting queue
- View patient history (vitals, appointments, exams, diagnoses)
- Perform examination and order tests

### 4. Laboratory

- Receive exam requests with clinical details
- Upload test result images (blood work, X-rays, ECG, ultrasound)
- Add clinical findings and comments
- Return results to consultation

### 5. Diagnosis

- Review laboratory results with images
- Provide feedback on each test
- Confirm diagnosis from 24+ medical conditions
- Add diagnosis notes

### 6. Prescription

- Prescribe multiple medications with dosage, frequency, and duration
- Add prescription comments and management plans
- Send to Account for payment processing

### 7. Account & Payment

- View pending prescriptions
- Select payment method (Cash, Credit Card, Debit, Insurance, Mobile)
- Generate and print receipts
- Send paid prescriptions to Pharmacy

### 8. Pharmacy

- View prescriptions ready for dispensing
- Verify patient information and payment status
- Review complete prescription details
- Dispense medicines and complete patient record

## Database Schema

The system includes 9 interconnected tables:

- `users` - System users with authentication
- `patients` - Patient demographics and medical info
- `vitals` - Vital signs records
- `appointments` - Appointment scheduling
- `consultations` - Consultation queue with status tracking
- `exams` - Laboratory test orders
- `laboratory` - Test results with images
- `diagnoses` - Clinical diagnosis records
- `prescriptions` - Medication prescriptions with pharmacy status

## File Upload Support

Laboratory module supports uploading test result images:

- Formats: PNG, JPG, JPEG, GIF, PDF
- Max size: 16MB per file
- Secure filename sanitization
- Organized storage in `static/lab_results/`

## Notes

- Database created automatically on first run with foreign key constraints
- CASCADE deletes ensure data integrity when removing patients
- All user inputs are sanitized to prevent XSS and SQL injection
- File uploads are validated and stored securely
- Session-based authentication with secure cookie settings

## Building Executable

Create a standalone executable:

```bash
python build_executable.py
```

The exe will be in `dist/` folder with all dependencies included.

## Production Deployment

```bash
# Using gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Or with waitress (Windows)
pip install waitress
waitress-serve --host=0.0.0.0 --port=8000 app:app
```

---

Developed for clinical workflow management - January 2026
