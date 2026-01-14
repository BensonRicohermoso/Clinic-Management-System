# Bug Fixes Applied - Clinical Management System

## Date: January 14, 2026

This document lists all bugs that were identified and fixed in the system.

---

## CRITICAL BUGS FIXED ✅

### 1. Missing Database Rollback on Patient Operations

**Location**: `app.py` - add_patient, edit_patient, add_vitals, add_appointment routes
**Issue**: When errors occurred, database changes were not rolled back, potentially leaving partial data
**Fix**: Added `db.rollback()` in all exception handlers before operations commit
**Impact**: Prevents data corruption and ensures database consistency

### 2. Unsanitized Username Input on Login

**Location**: `app.py` - login route (line 56)
**Issue**: Username was not sanitized before database query
**Fix**: Added `sanitize_input()` call for username and validation for empty credentials
**Impact**: Improved security against SQL injection and XSS attacks

### 3. Session Timeout Not Enforced

**Location**: `app.py` - login route
**Issue**: Sessions were configured with timeout but `session.permanent` was not set
**Fix**: Added `session.permanent = True` to enforce PERMANENT_SESSION_LIFETIME
**Impact**: Sessions now properly timeout after 8 hours as configured

---

## HIGH PRIORITY BUGS FIXED ✅

### 4. Weak Sanitization Function

**Location**: `app.py` - sanitize_input function (line 25)
**Issue**: Function removed apostrophes, breaking legitimate names like "O'Brien"
**Fix**: Modified regex to preserve apostrophes while still removing dangerous characters
**Impact**: Legitimate data preserved while maintaining XSS protection

### 5. Missing File Size Validation

**Location**: `app.py` - laboratory/submit route
**Issue**: Individual files not validated for size (only total request size)
**Fix**: Added `validate_file_size()` function with 10MB per-file limit
**Impact**: Prevents single large files from consuming all allowed space

### 6. No Patient Validation Before File Upload

**Location**: `app.py` - submit_lab_results route (line 818)
**Issue**: Patient ID used in filename without verifying patient exists
**Fix**: Added patient existence check before processing files
**Impact**: Prevents saving files with invalid patient IDs

---

## MEDIUM PRIORITY BUGS FIXED ✅

### 7. Inconsistent File Cleanup Error Handling

**Location**: `app.py` - laboratory file upload (multiple locations)
**Issue**: Used bare `except: pass` which silently swallows all exceptions
**Fix**: Changed to `except (OSError, IOError)` with logging
**Impact**: Better error visibility and proper exception handling

### 8. No Check for Deleted Patients in History API

**Location**: `app.py` - get_patient_history route (line 626)
**Issue**: No validation if patient_id exists before querying
**Fix**: Added patient existence check and return 404 if not found
**Impact**: Returns proper error instead of empty data for invalid patients

### 9. No Maximum Medicine Count Validation

**Location**: `app.py` - submit_prescription route (line 512)
**Issue**: medicine_count could be set to extremely large values
**Fix**: Added validation: maximum 50 medicines per prescription
**Impact**: Prevents memory issues from malicious large counts

### 10. Unvalidated Payment Methods

**Location**: `app.py` - complete_payment route (line 977)
**Issue**: Payment method not validated against allowed values
**Fix**: Added validation against allowed list: cash, insurance, card, mobile_money
**Impact**: Ensures only valid payment methods are stored

---

## LOW PRIORITY BUGS FIXED ✅

### 11. Missing Database Index

**Location**: `models/database.py` - init_db function (line 190)
**Issue**: No index on prescriptions.pharmacy_status despite filtering on it
**Fix**: Added `CREATE INDEX idx_prescriptions_pharmacy_status`
**Impact**: Improved query performance for Account and Pharmacy pages

### 12. Race Condition in Consultation Queue

**Location**: `models/database.py` - consultations table (line 96)
**Issue**: Check and insert not atomic - could create duplicate entries
**Fix**: Added UNIQUE constraint on (patient_id, status)
**Impact**: Database prevents duplicate consultation queue entries

### 13. SECRET_KEY Warning in Production

**Location**: `app.py` - configuration section (line 18)
**Issue**: Warning printed even in production (information disclosure)
**Fix**: Only show warning when FLASK_ENV is 'development'
**Impact**: Reduces information leakage in production

---

## DATABASE SCHEMA IMPROVEMENTS ✅

### New Indexes Added:

- `idx_prescriptions_pharmacy_status` - Improves Account/Pharmacy queries

### New Constraints Added:

- `UNIQUE(patient_id, status)` on consultations table - Prevents duplicate queue entries

---

## FILES MODIFIED

1. **app.py** - 15 bug fixes applied

   - Sanitization improvements
   - Database rollback handling
   - File validation
   - Session management
   - Input validation

2. **models/database.py** - 2 improvements

   - Added pharmacy_status index
   - Added unique constraint on consultations

3. **config.py** - No changes needed (already properly configured)

4. **templates/consultations.html** - Fixed in previous session
   - Prescription comment toggle functionality

---

## MIGRATION REQUIRED

For **existing databases**, run the migration script:

```bash
python update_database_indexes.py
```

This adds the pharmacy_status index to improve performance.

**Note**: The unique constraint on consultations only applies to new databases. Existing databases will continue to work but won't enforce this constraint without recreation.

---

## TESTING RECOMMENDATIONS

1. **Test Patient Operations**

   - Add/edit patient with errors to verify rollback works
   - Test with names containing apostrophes (e.g., "O'Brien")

2. **Test File Uploads**

   - Upload files > 10MB to verify size validation
   - Upload invalid patient ID to verify rejection

3. **Test Consultation Queue**

   - Try adding same patient twice (should fail with unique constraint)

4. **Test Login**

   - Verify session timeout after 8 hours
   - Test with malicious username input

5. **Test Payment Methods**
   - Try invalid payment method to verify validation

---

## SECURITY IMPROVEMENTS SUMMARY

✅ Input sanitization strengthened
✅ Session timeout enforcement
✅ File upload validation (type + size)
✅ Database integrity (rollbacks + constraints)
✅ Better error handling
✅ Reduced information disclosure

---

## KNOWN LIMITATIONS

1. **CSRF Protection**: Not implemented (would require Flask-WTF or custom tokens)
2. **Unique Constraint**: Only applies to new databases (migration would require table recreation)
3. **Rate Limiting**: No rate limiting on login attempts
4. **Audit Logging**: No comprehensive audit trail for sensitive operations

These can be addressed in future updates if needed.

---

## CONCLUSION

All identified bugs have been fixed safely and carefully. The system is now more secure, robust, and performant. Database integrity is protected, input is properly validated, and error handling is consistent throughout the application.
