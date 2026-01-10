# 📘 Clinical Management System - User Manual

## Simple Guide for Healthcare Staff

---

## 🔐 1. LOGGING IN

**Step 1:** Open your web browser (Chrome, Firefox, or Edge)

**Step 2:** Type this address: `http://127.0.0.1:5000`

**Step 3:** You'll see the login page with a green and yellow design

**Step 4:** Enter your username and password:

- **Admin User**: Username: `admin` / Password: `admin123`
- **Nurse User**: Username: `nurse1` / Password: `nurse123`

**Step 5:** Click the "Sign In" button

✅ **Success!** You'll be taken to the Dashboard

---

## 🏠 2. UNDERSTANDING THE DASHBOARD

When you log in, you'll see:

### Top Section - Statistics Cards

- **Green Card (Left)**: Total number of patients
- **Yellow Card (Middle)**: Today's appointments
- **Green Card (Right)**: Vital signs recorded in last 24 hours

### Middle Section - Upcoming Appointments

- Shows the next 5 appointments
- Displays patient name, date, time, and reason

### Bottom Section - Quick Actions

Four colored buttons for fast access:

- **Add Patient** - Register new patients
- **Record Vitals** - Take vital signs
- **Schedule Visit** - Book appointments
- **Find Patient** - Search patient records

---

## 👥 3. MANAGING PATIENTS

### How to Add a New Patient

**Step 1:** Click **"Patients"** in the top menu OR click **"Add Patient"** on the dashboard

**Step 2:** Click the green **"Add Patient"** button

**Step 3:** Fill in the form:

- **Full Name** ⭐ (Required) - Patient's complete name
- **Age** ⭐ (Required) - Patient's age in years
- **Gender** ⭐ (Required) - Select Male, Female, or Other
- **Blood Type** (Optional) - Select from dropdown (A+, O-, etc.)
- **Allergies** (Optional) - List any allergies (e.g., "Penicillin, Peanuts")
- **Contact** (Optional) - Phone number
- **Address** (Optional) - Home address

**Step 4:** Click **"Add Patient"** button at the bottom

✅ **Success!** Green message appears: "Patient added successfully!"

### How to Edit a Patient

**Step 1:** Go to **"Patients"** page

**Step 2:** Find the patient in the list

**Step 3:** Click the **blue pencil icon** (✏️) next to their name

**Step 4:** Update the information you want to change

**Step 5:** Click **"Update Patient"**

✅ **Success!** Patient information updated!

### How to Delete a Patient

**Step 1:** Go to **"Patients"** page

**Step 2:** Find the patient in the list

**Step 3:** Click the **red trash icon** (🗑️) next to their name

**Step 4:** Confirm you want to delete

⚠️ **Warning**: This will also delete all their vital signs and appointments!

---

## 💓 4. RECORDING VITAL SIGNS

### How to Record Vitals

**Step 1:** Click **"Vitals"** in the top menu

**Step 2:** Click the green **"Record Vitals"** button

**Step 3:** Select the patient from the dropdown list

**Step 4:** Enter the vital signs:

#### Blood Pressure ⭐ (Required)

- Format: `120/80`
- First number (systolic) / Second number (diastolic)
- Example: Type `110/70`

#### Heart Rate ⭐ (Required)

- In beats per minute (bpm)
- Example: Type `72`
- Normal range: 60-100 bpm

#### Temperature ⭐ (Required)

- In degrees Celsius (°C)
- Example: Type `36.6`
- Normal range: 36.1-37.2°C

#### Respiratory Rate ⭐ (Required)

- Breaths per minute
- Example: Type `16`
- Normal range: 12-20 per minute

#### Oxygen Saturation (Optional)

- Percentage (%)
- Example: Type `98`
- Normal range: 95-100%

**Step 5:** Add any notes (Optional)

- Example: "Patient complains of headache"

**Step 6:** Click **"Record Vitals"**

✅ **Success!** Vitals recorded and saved!

### Understanding the Colors

- **Red numbers** = Abnormal/Warning (too high or too low)
- **Black numbers** = Normal range
- **Blue numbers** = Below normal (temperature)

---

## 📅 5. SCHEDULING APPOINTMENTS

### How to Schedule an Appointment

**Step 1:** Click **"Appointments"** in the top menu

**Step 2:** Click the yellow **"New Appointment"** button

**Step 3:** Fill in the details:

- **Patient** ⭐ (Required) - Select from dropdown
- **Date** ⭐ (Required) - Click calendar icon to choose date
- **Time** ⭐ (Required) - Select time (e.g., 09:00 AM)
- **Reason** ⭐ (Required) - Why is the patient visiting?
  - Example: "Follow-up checkup" or "Vaccination"

**Step 4:** Click **"Schedule Appointment"**

✅ **Success!** Appointment scheduled!

### How to Update Appointment Status

You can mark appointments as:

- **Scheduled** (Blue) - Appointment is confirmed
- **Completed** (Green) - Patient came and was seen
- **Cancelled** (Red) - Appointment was cancelled

**To mark as completed:**

- Click the **green check icon** (✓) next to the appointment

**To cancel:**

- Click the **red X icon** next to the appointment

### How to Delete an Appointment

**Step 1:** Find the appointment in the list

**Step 2:** Click the **trash icon** (🗑️)

**Step 3:** Confirm deletion

---

## 🔍 6. FILTERING AND VIEWING

### Filter Appointments by Status

At the top of the Appointments page, click:

- **All** - See all appointments
- **Scheduled** - See only upcoming appointments
- **Completed** - See only finished appointments
- **Cancelled** - See only cancelled appointments

### View Patient Information

On the Patients page, you can see:

- Patient name and photo icon
- Age and gender (♂️ male / ♀️ female symbols)
- Blood type in red badge
- Contact phone number
- Red warning if patient has allergies

---

## 🚪 7. LOGGING OUT

**Step 1:** Click your username in the top-right corner

**Step 2:** Click the red **"Logout"** button

✅ **Success!** You're logged out and back to login page

---

## 💡 8. HELPFUL TIPS

### ✅ Best Practices

1. **Always double-check vital signs** before saving
2. **Record vitals immediately** after taking measurements
3. **Add notes** for unusual readings or symptoms
4. **Update appointments** right after patient visits
5. **Keep patient information current** - update as needed

### ⚠️ Important Reminders

- The system saves automatically when you click "Save" buttons
- You cannot undo deletions - be careful!
- If you see red numbers in vitals, check the patient
- Always log out when leaving your computer
- Change default passwords for security

### 📱 Normal Vital Signs Reference

Keep this handy when recording vitals:

| Vital Sign        | Normal Range        |
| ----------------- | ------------------- |
| Blood Pressure    | 90-120 / 60-80 mmHg |
| Heart Rate        | 60-100 bpm          |
| Temperature       | 36.1-37.2°C         |
| Respiratory Rate  | 12-20 breaths/min   |
| Oxygen Saturation | 95-100%             |

---

## 🆘 9. COMMON PROBLEMS & SOLUTIONS

### Problem: "Can't log in"

**Solution:**

- Check your username and password
- Make sure Caps Lock is OFF
- Try: admin / admin123

### Problem: "Page is blank or white"

**Solution:**

- Refresh the page (press F5)
- Clear your browser cache
- Try a different browser

### Problem: "Can't find a patient"

**Solution:**

- Check the spelling of the name
- Scroll through the patient list
- Patient might have been deleted

### Problem: "Forgot to log out"

**Solution:**

- Open the website again
- Click your name in top-right
- Click Logout button

### Problem: "Server not running"

**Solution:**

- Ask your IT guy
- The application needs to be started first

---

## 📞 10. GETTING HELP

If you need assistance:

1. **Check this manual first** - most answers are here
2. **Ask your supervisor** - they may have encountered the issue
3. **Contact IT support** - for technical problems
4. **Take a screenshot** - helps explain the problem

---

## 🎓 Quick Start Checklist

For new users, follow this checklist:

- [ ] Successfully logged in
- [ ] Explored the Dashboard
- [ ] Added a test patient
- [ ] Recorded test vital signs
- [ ] Scheduled a test appointment
- [ ] Filtered appointments by status
- [ ] Successfully logged out

---

**📌 Remember**: This system helps you work efficiently, but always prioritize patient care and accuracy!

**Last Updated**: January 2026

---

**Need more help?** Contact your IT guy, Benson.
