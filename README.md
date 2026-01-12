# Clinical Management System

A Flask-based system for managing patient records, vital signs, and appointments. Made for nursing staff.

## Features

- Patient management (add, edit, delete records)
- Vital signs tracking (BP, HR, temp, RR, SpO2)
- Appointment scheduling
- Consultation queue management
- Dashboard with stats
- User authentication
- Automated database backups
- Payment method tracking

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

## Usage

### Patients

Click "Patients" tab to add/edit patient records. Required fields are name, age, and gender.

### Vitals

Record vital signs in "Vitals" tab. Blood pressure format: 120/80

### Appointments

Schedule appointments in "Appointments" tab. Can mark as completed or cancelled.

## Notes

- Database file (clinical_management.db) is created automatically on first run
- For production use, deploy with gunicorn or similar WSGI server
- Change default passwords before deploying

## Building Executable

If you want a standalone exe:

```bash
python build_executable.py
```

This creates a dist/ folder with the executable inside.

## TODO

- Add PDF export for patient records
- Email notifications for appointments
- Better search/filter options
- Medication tracking maybe

---

Created for nursing project - January 2026
