# User Guide

Complete guide for using the Clinical Management System.

## Getting Started

1. Open browser to `http://127.0.0.1:5000`
2. Login with default credentials:
   - **Admin:** `admin` / `admin123`
   - **Nurse:** `nurse1` / `nurse123`
3. **⚠️ Change passwords immediately after first login**

## Dashboard

The main dashboard displays:

- Total number of registered patients
- Today's scheduled appointments
- Recent vital signs (last 24 hours)
- Upcoming appointments with patient details

## Navigation

Use the left sidebar to access:

- **Dashboard** - Overview and statistics
- **Patients** - Patient management
- **Vitals** - Record vital signs
- **Consultations** - Consultation queue
- **Laboratory** - Lab test processing
- **Account** - Payment processing
- **Pharmacy** - Medicine dispensing
- **Appointments** - Appointment scheduling

---

## 1. Patient Management

### Add New Patient

1. Click **Patients** in sidebar
2. Click **"Add New Patient"** button
3. Fill required fields:
   - Name (required)
   - Date of Birth (required)
   - Gender (required)
   - Blood Type (optional)
   - Known Allergies (optional)
   - Contact Number (optional)
   - Address (optional)
4. Click **"Add Patient"**

### Edit Patient Information

1. Find patient in the list
2. Click **Profile** button (blue)
3. Update information
4. Click **"Update Patient"**

### Add to Consultation

- Click **"Add to Consultation"** button (green)
- Patient will appear in Consultations queue
- Cannot add same patient twice to active queue

### View Patient History

- Click **History** button to view:
  - All vital signs records
  - Past appointments
  - Previous examinations
  - Diagnosis history

---

## 2. Recording Vital Signs

1. Go to **Vitals** page
2. Click **"Record Vitals"**
3. Select patient from dropdown
4. Enter measurements:
   - **Blood Pressure:** Format: 120/80 (systolic/diastolic)
   - **Heart Rate:** Beats per minute (bpm)
   - **Temperature:** Celsius (°C)
   - **Respiratory Rate:** Breaths per minute
   - **Oxygen Saturation:** Percentage (optional)
5. Add clinical notes (optional)
6. Click **"Record Vitals"**

**Normal Ranges:**

- BP: 90-120 / 60-80 mmHg
- Heart Rate: 60-100 bpm
- Temperature: 36.1-37.2°C
- Respiratory Rate: 12-20 per minute
- SpO2: 95-100%

---

## 3. Appointments

### Schedule Appointment

1. Click **Appointments**
2. Click **"Schedule New Appointment"**
3. Select patient
4. Choose date and time
5. Enter reason for visit
6. Select type (Checkup, Follow-up, Emergency, etc.)
7. Click **"Schedule Appointment"**

### Manage Appointments

- **Mark Completed:** Green checkmark icon
- **Cancel:** Red X icon
- **Delete:** Trash icon

### Filter Appointments

Use filter buttons:

- **All** - Show all appointments
- **Scheduled** - Upcoming appointments
- **Completed** - Finished appointments
- **Cancelled** - Cancelled appointments

---

## 4. Consultation Workflow

### Consultation Queue

1. Go to **Consultations** page
2. View all patients waiting for consultation
3. Each patient shows:
   - Profile button (blue) - View patient details
   - History button (teal) - View medical history
   - Exam button (orange/green) - Order tests
   - Diagnose button (teal/green) - Review results and diagnose
   - Prescribe button (blue/green) - Write prescription

### Conducting Examination

1. Click **"Exam"** button
2. Enter:
   - Presenting Complaint (required)
   - History of Complaint (required)
   - Clinical Details (optional)
3. Select laboratory tests needed:
   - Blood Tests (RBS, FBS, LFT, CBC, Lipid, KFT, Thyroid)
   - Urine & Stool Tests
   - Imaging (Chest X-Ray, Ultrasound)
   - ECG
4. Click **"Send to Laboratory"**
5. Patient is sent to Laboratory queue

### Remove from Queue

- Click **"Remove"** (red button) to remove patient from consultation
- Use **"Complete Consultation"** when finished

---

## 5. Laboratory

### Processing Lab Tests

1. Go to **Laboratory** page
2. View pending exam requests
3. Click **"Upload Results"** button
4. Upload test result images:
   - Supported formats: PNG, JPG, JPEG, GIF, PDF
   - Max size: 16MB per file
   - Upload one image per requested test
5. Enter clinical details for each test
6. Add general laboratory comments
7. Click **"Submit Results"**
8. Patient returns to Consultation queue automatically

### Cancel Exam Request

- Click **"Cancel Exam"** (red button)
- Confirm cancellation

---

## 6. Diagnosis

### Making Diagnosis

1. In **Consultations**, click **"Diagnose"** (teal button with folder icon)
2. Review laboratory results:
   - View all test result images (click to enlarge)
   - Read clinical details
3. Provide feedback for each test result
4. Add laboratory technician comments
5. Select **Confirmed Diagnosis** from dropdown:
   - Malaria, Typhoid Fever, Dengue Fever
   - Bacterial/Viral Infections
   - Diabetes (Type 1/2), Hypertension
   - Tuberculosis, Pneumonia, Asthma
   - Anemia, Hepatitis, Gastritis
   - UTI, Kidney Disease, Thyroid Disorders
   - And more...
6. Add diagnosis notes (optional)
7. Click **"Confirm Diagnosis"**
8. Patient remains in consultation for prescription

---

## 7. Prescription

### Writing Prescription

1. Click **"Prescribe"** button (blue/purple)
2. Enter **number of medicines** (1-20)
3. For each medicine, enter:
   - **Type:** Select from dropdown (Paracetamol, Ibuprofen, Amoxicillin, etc.)
   - **Amount:** e.g., 500mg, 10ml
   - **Times per Day:** 1-10 times
   - **Duration:** 1-365 days
4. **Optional additions:**
   - Prescription Comment: Additional instructions
   - Management Plan: Follow-up care instructions
5. Click **"Send to Account"**
6. Patient moves to Account page
7. Consultation marked as completed

---

## 8. Account & Payment

### Processing Payments

1. Go to **Account** page
2. View patients with pending prescriptions
3. Check **Payment Status**:
   - **Pending** (yellow badge) - Awaiting payment
   - **Paid** (green badge) - Payment confirmed
4. Select **Payment Method:**
   - Cash
   - Credit Card
   - Debit Card
   - Insurance
   - Mobile Payment
5. Click **"Confirm"** to process payment

### View Receipt

- Click **"Receipt"** button to view:
  - Patient information
  - Prescribed medicines with dosage
  - Prescription comments
  - Management plan
  - Prescribing doctor
  - Date and time
- Print receipt for patient records

### Send to Pharmacy

1. After payment is confirmed
2. Click **"Send to Pharmacy"** button (purple)
3. Patient appears in Pharmacy queue

---

## 9. Pharmacy

### Dispensing Medicines

1. Go to **Pharmacy** page
2. View patients ready for medicine dispensing
3. Click buttons to:
   - **Profile** (blue) - View patient information
   - **Prescription** (teal) - View full prescription details
   - **Complete** (green) - Dispense medicines and finish
   - **Cancel** (red) - Send back to Account

### Completing Service

1. Click **"Complete"** button
2. Confirm in the modal
3. System will:
   - Mark prescription as completed
   - Remove patient and ALL records from database
   - Display success message

### Cancelling Service

1. Click **"Cancel"** button
2. Confirm cancellation
3. Patient returns to Account page

---

## Tips & Best Practices

### Data Entry

- Always double-check vital signs before saving
- Use clear, concise clinical notes
- Complete all required fields marked with asterisks
- Upload clear, readable test result images

### Patient Safety

- Verify patient identity before each step
- Review allergies before prescribing
- Check payment status before dispensing medicines
- Keep patient information confidential

### Workflow

- Add patients to consultation only when ready to see them
- Process laboratory results promptly
- Ensure payment before sending to pharmacy
- Complete pharmacy service to remove patient records

### System Maintenance

- Log out when finished using the system
- Run database backups regularly: `python backup_database.py`
- Change default passwords immediately
- Report any errors or issues

---

## Troubleshooting

**Can't log in?**

- Check username and password spelling
- Ensure Caps Lock is off
- Try refreshing the page (F5)

**Patient not showing in queue?**

- Check if already in consultation
- Refresh the page
- Verify patient was added correctly

**Cannot upload lab results?**

- Check file format (PNG, JPG, JPEG, GIF, PDF only)
- Ensure file size is under 16MB
- Try a different file

**Prescription won't submit?**

- Fill all medicine fields completely
- Check medicine count matches entries
- Ensure times per day and duration are valid

**Payment method disabled?**

- Payment may already be confirmed
- Check payment status badge

---

## Keyboard Shortcuts

- **F5** - Refresh page
- **Ctrl + P** - Print receipt
- **Esc** - Close modal windows

---

## Contact Support

For technical assistance or questions, contact your IT administrator.

**System Version:** 1.0
**Last Updated:** January 2026
