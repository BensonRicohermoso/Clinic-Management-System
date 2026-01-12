# Clinical Management System

A Flask-based system for managing patient records, vital signs, and appointments. Made for nursing staff.

## Features

- Patient management (add, edit, delete records)
- Vital signs tracking (BP, HR, temp, RR, SpO2)
- Appointment scheduling
- Dashboard with stats
- User authentication

## Setup

1. Install Python 3.8+

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python app.py
```

4. Open browser to `http://127.0.0.1:5000`

## Login

Default accounts:

- Admin: `admin` / `admin123`
- Nurse: `nurse1` / `nurse123`

**Note:** Change these passwords if using for real

## Tech Stack

- Python/Flask
- SQLite
- Tailwind CSS
- Font Awesome icons

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
