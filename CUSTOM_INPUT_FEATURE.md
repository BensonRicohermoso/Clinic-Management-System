# Custom Input Feature - User Manual

## Overview

Users can now manually type custom options if they don't find what they need in dropdown selections for:

1. **Diagnosis** (in Diagnose modal)
2. **Medicine Type** (in Prescribe modal)
3. **Department/Ward** (in Add/Edit Patient forms)

---

## How to Use

### 1. Custom Diagnosis Entry

**Location**: Consultations page → Diagnose button

**Steps**:

1. Click "Diagnose" button for a patient
2. In the "Confirmed Diagnosis" dropdown, scroll to the bottom
3. Select **"Other (Type in the box below)"**
4. A text input field will appear below the dropdown
5. Type your custom diagnosis
6. Submit the form

**Example**:

- If the patient has "Chronic Sinusitis" which isn't in the list
- Select "Other (Type your own)"
- Type "Chronic Sinusitis" in the text box
- The custom diagnosis will be saved

---

### 2. Custom Medicine Entry

**Location**: Consultations page → Prescribe button

**Steps**:

1. Click "Prescribe" button for a patient
2. Enter the number of medicines
3. For each medicine dropdown, scroll to the bottom
4. Select **"Other (Type in the box below)"**
5. A text input field will appear below the dropdown
6. Type your custom medicine name
7. Fill in amount, frequency, and duration as usual

**Example**:

- If prescribing "Azithromycin 500mg" which isn't in the list
- Select "Other (Type your own)" in medicine type
- Type "Azithromycin"
- Enter amount: "500mg"
- Continue with other details

---

### 3. Custom Department/Ward Entry

**Location**: Patients page → Add Patient / Edit Patient

**Steps**:

1. Click "Add New Patient" or "Edit" button
2. In the "Department / Ward" dropdown, scroll to the bottom
3. Select **"Other (Type in the box below)"**
4. A text input field will appear below the dropdown
5. Type your custom department/ward name
6. Save the patient

**Example**:

- If patient is in "Dialysis Unit" which isn't in the list
- Select "Other (Type your own)"
- Type "Dialysis Unit"
- The custom department will be saved

---

## Visual Indicators

- The **"Other (Type in the box below)"** option appears at the bottom of each dropdown
- When selected, a text input box appears with placeholder text:
  - "Type your custom diagnosis here..."
  - "Type your custom medicine here..."
  - "Type your custom department here..."

---

## Technical Details

### Frontend Changes

- Added **"**OTHER**"** option to all relevant dropdowns
- Created toggle functions:
  - `toggleCustomDiagnosis()` - Shows/hides diagnosis custom input
  - `toggleCustomMedicine(index)` - Shows/hides medicine custom input
  - `toggleCustomDepartmentAdd()` - Shows/hides department custom input (Add form)
  - `toggleCustomDepartmentEdit()` - Shows/hides department custom input (Edit form)

### Behavior

- When "Other" is selected:
  - The text input field appears
  - The input becomes required
  - The dropdown's `name` attribute is removed
  - The text input gets the `name` attribute (so form submits the custom value)
- When switching back to a dropdown option:
  - The text input is hidden
  - The input is no longer required
  - The dropdown's `name` attribute is restored
  - Any typed text is cleared

### Backend Handling

- No changes needed to backend code
- The existing `request.form.get()` calls work with both dropdown and custom inputs
- Values are sanitized using existing `sanitize_input()` function

---

## Files Modified

1. **templates/consultations.html**

   - Added custom diagnosis input field
   - Added custom medicine input fields (dynamic)
   - Added JavaScript toggle functions

2. **templates/patients.html**
   - Added custom department input fields (Add and Edit forms)
   - Added JavaScript toggle functions
   - Updated `openEditPatientModal()` to handle existing custom departments

---

## Compatibility

- ✅ Works with all existing features
- ✅ Custom values are properly saved to database
- ✅ Custom departments display correctly in patient edit form
- ✅ Custom values appear in all reports and displays
- ✅ No backend changes required

---

## Benefits

1. **Flexibility**: Users aren't limited to predefined lists
2. **Completeness**: Can record any diagnosis, medicine, or department
3. **User-Friendly**: Simple toggle between dropdown and custom input
4. **Data Integrity**: Custom inputs are sanitized like all other inputs
5. **No Training Required**: Intuitive interface with clear labels

---

## Examples in Practice

### Scenario 1: Rare Disease

- Doctor needs to diagnose "Behçet's Disease"
- Not in standard dropdown
- Selects "Other" and types the exact diagnosis
- System saves it correctly

### Scenario 2: Specialized Medicine

- Prescribing "Tocilizumab" for rheumatoid arthritis
- Not in common medicines list
- Selects "Other" and types the medicine name
- Prescription is created with correct medicine

### Scenario 3: New Department

- Hospital opens a "COVID Recovery Ward"
- Not yet in the system
- Admin selects "Other" and types the new department
- Patients can be assigned to this new department

---

## Future Enhancements (Optional)

- Could add "Recently Used Custom Values" to make repeat entries faster
- Could populate dropdown with frequently used custom entries
- Could add admin panel to manage dropdown options

---

**Implementation Date**: January 14, 2026  
**Version**: 1.1  
**Status**: ✅ Production Ready
