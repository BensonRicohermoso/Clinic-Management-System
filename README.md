# 🏥 Clinical Management System

A comprehensive Flask-based nursing management system for patient tracking, vital signs monitoring, and appointment scheduling. Built with modern web technologies and featuring an intuitive olive green and yellow color theme.

## ✨ Features

### 👥 Patient Management

- Add, edit, and delete patient records
- Track patient demographics (age, gender, blood type)
- Record allergies and medical conditions
- Maintain contact information and addresses
- Search and filter patient database

### 📊 Vital Signs Monitoring

- Record comprehensive vital signs:
  - Blood Pressure (BP)
  - Heart Rate (HR)
  - Temperature
  - Respiratory Rate (RR)
  - Oxygen Saturation (SpO2)
- Real-time vital signs tracking
- Historical records with timestamps
- Automatic flagging of abnormal values
- Notes and observations for each reading

### 📅 Appointment Scheduling

- Schedule patient appointments
- View all appointments with filtering options
- Update appointment status (scheduled, completed, cancelled)
- Track appointment reasons and notes
- Calendar view of upcoming appointments

### 📈 Dashboard Analytics

- Real-time statistics overview
- Total patient count
- Today's appointments
- Recent vital signs (24-hour view)
- Quick action shortcuts
- Upcoming appointments preview

### 🔐 User Authentication

- Secure login system
- Role-based access (Admin/Nurse)
- Session management
- Password hashing with werkzeug

## 🛠️ Technologies Used

- **Backend**: Python 3.8+, Flask
- **Database**: SQLite3
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Icons**: Font Awesome 6.4.0
- **Security**: Werkzeug (password hashing)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Edge)

## 🚀 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/BensonRicohermoso/Clinic-Management-System.git
   cd Clinic-Management-System
   ```

2. **Install required packages**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**

   ```bash
   python app.py
   ```

   Or use the production runner:

   ```bash
   python run.py
   ```

4. **Access the application**
   - Open your web browser
   - Navigate to `http://127.0.0.1:5000`

## 👤 Default Login Credentials

### Admin Account

- **Username**: `admin`
- **Password**: `admin123`

### Nurse Account

- **Username**: `nurse1`
- **Password**: `nurse123`

> ⚠️ **Important**: Change these default credentials in a production environment!

## 📖 Usage Guide

### Getting Started

1. Login using the default credentials
2. Navigate through the main sections using the top navigation bar
3. Use the dashboard for quick overview and actions

### Managing Patients

1. Click on **Patients** in the navigation menu
2. Click **Add Patient** button
3. Fill in patient information:
   - Full Name (required)
   - Age (required)
   - Gender (required)
   - Blood Type
   - Allergies
   - Contact information
   - Address
4. Click **Save** to add the patient
5. Use edit/delete icons to modify or remove patients

### Recording Vital Signs

1. Navigate to **Vitals** section
2. Click **Record Vitals** button
3. Select patient from dropdown
4. Enter vital measurements:
   - Blood Pressure (format: 120/80)
   - Heart Rate (bpm)
   - Temperature (°C)
   - Respiratory Rate (breaths/min)
   - Oxygen Saturation (%) - optional
5. Add clinical notes if needed
6. Click **Record Vitals** to save

### Scheduling Appointments

1. Go to **Appointments** section
2. Click **New Appointment** button
3. Select patient
4. Choose date and time
5. Enter appointment reason
6. Click **Schedule** to confirm
7. Update status or delete as needed

## 📁 Project Structure

```
Clinic-Management-System/
├── app.py                    # Main Flask application
├── config.py                 # Configuration settings
├── run.py                    # Production runner
├── requirements.txt          # Python dependencies
├── build_executable.py       # PyInstaller build script
├── models/
│   └── database.py          # Database models and schema
├── templates/
│   ├── layout.html          # Base template
│   ├── login.html           # Login page
│   ├── dashboard.html       # Dashboard view
│   ├── patients.html        # Patient management
│   ├── vitals.html          # Vital signs tracking
│   └── appointments.html    # Appointment scheduling
└── clinical_management.db   # SQLite database (auto-generated)
```

## 🎨 Color Theme

The application uses a professional healthcare color scheme:

- **Primary**: Olive Green (#16a34a to #166534)
- **Secondary**: Warm Yellow (#eab308 to #ca8a04)
- **Accent**: Various shades of green for medical context

## 🔒 Security Features

- Password hashing using Werkzeug
- Session-based authentication
- Login required decorators for protected routes
- CSRF protection ready
- SQL injection prevention through parameterized queries

## 📊 Database Schema

### Users Table

- id, username, password (hashed), full_name, role, created_at

### Patients Table

- id, name, age, gender, blood_type, allergies, contact, address, created_at, updated_at

### Vitals Table

- id, patient_id, blood_pressure, heart_rate, temperature, respiratory_rate, oxygen_saturation, notes, recorded_by, recorded_at

### Appointments Table

- id, patient_id, date, time, reason, status, notes, created_at

## 🚀 Deployment

### Development

```bash
python app.py
```

Runs on `http://0.0.0.0:5000` with debug mode enabled.

### Production

```bash
python run.py
```

Or use a WSGI server like Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Build Executable (Optional)

```bash
python build_executable.py
```

Creates a standalone executable using PyInstaller.

## 🌐 Browser Compatibility

- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Microsoft Edge
- ✅ Safari
- ⚠️ Internet Explorer (not supported)

## 📝 Future Enhancements

- [ ] Export patient data to PDF/Excel
- [ ] Print prescription functionality
- [ ] SMS/Email appointment reminders
- [ ] Multi-user real-time updates
- [ ] Advanced reporting and analytics
- [ ] Medical history timeline
- [ ] Lab results integration
- [ ] Medication tracking
- [ ] Billing and invoicing module

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is created for educational purposes as a Nursing Project.

## 👨‍💻 Author

**Benson Rico Hermoso**

- GitHub: [@BensonRicohermoso](https://github.com/BensonRicohermoso)

## 🙏 Acknowledgments

- Flask framework and community
- Tailwind CSS for styling
- Font Awesome for icons
- All contributors and testers

## 📞 Support

For issues, questions, or suggestions:

- Open an issue on GitHub
- Contact the repository owner

---

**⚕️ Built with care for healthcare professionals**

_Last Updated: January 2026_
