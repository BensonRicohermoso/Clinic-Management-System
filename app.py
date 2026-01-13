from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime, timedelta
import os
import re
import json
from models.database import init_db, get_db
from config import config

app = Flask(__name__)

# Load configuration from config.py
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Validate critical environment variables
if not os.environ.get('SECRET_KEY'):
    print("WARNING: Using default SECRET_KEY. Set SECRET_KEY environment variable in production!")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def sanitize_input(text):
    if not text:
        return text
    # Remove HTML tags and dangerous characters
    text = re.sub(r'<[^>]*>', '', str(text))
    text = re.sub(r'[<>"\']', '', text)
    return text.strip()

with app.app_context():
    init_db()

from models.database import close_db
app.teardown_appcontext(close_db)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash(f'Welcome back, {user["full_name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    
    total_patients = db.execute('SELECT COUNT(*) as count FROM patients').fetchone()['count']
    
    today = datetime.now().strftime('%Y-%m-%d')
    today_appointments = db.execute(
        'SELECT COUNT(*) as count FROM appointments WHERE date = ?', (today,)
    ).fetchone()['count']
    
    # last 24hrs vitals
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    recent_vitals = db.execute(
        'SELECT COUNT(*) as count FROM vitals WHERE recorded_at > ?', (yesterday,)
    ).fetchone()['count']
    

    upcoming = db.execute(
        '''SELECT a.*, p.name as patient_name 
           FROM appointments a
           JOIN patients p ON a.patient_id = p.id
           WHERE a.date >= ?
           ORDER BY a.date, a.time
           LIMIT 5''', (today,)
    ).fetchall()
    
    stats = {
        'total_patients': total_patients,
        'today_appointments': today_appointments,
        'recent_vitals': recent_vitals
    }
    
    return render_template('dashboard.html', stats=stats, upcoming=upcoming)

# Patient routes
@app.route('/patients')
@login_required
def patients():
    db = get_db()
    patients_list = db.execute(
        'SELECT * FROM patients ORDER BY name'
    ).fetchall()
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('patients.html', patients=patients_list, today=today)

@app.route('/patients/add', methods=['POST'])
@login_required
def add_patient():
    try:
        db = get_db()
        # Sanitize inputs
        name = sanitize_input(request.form['name'])
        allergies = sanitize_input(request.form.get('allergies', ''))
        address = sanitize_input(request.form.get('address', ''))
        
        db.execute(
            '''INSERT INTO patients (name, date_of_birth, gender, blood_type, allergies, contact, address, payment_method)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (name, request.form['date_of_birth'], request.form['gender'],
             request.form['blood_type'], allergies,
             request.form['contact'], address, request.form['payment_method'])
        )
        db.commit()
        flash('Patient added successfully!', 'success')
    except KeyError as e:
        flash(f'Missing field: {str(e)}. Please refresh the page and try again.', 'error')
    except Exception as e:
        flash(f'Error adding patient: {str(e)}', 'error')
    return redirect(url_for('patients'))

@app.route('/patients/edit/<int:id>', methods=['POST'])
@login_required
def edit_patient(id):
    try:
        db = get_db()
        # Sanitize inputs
        name = sanitize_input(request.form['name'])
        allergies = sanitize_input(request.form.get('allergies', ''))
        address = sanitize_input(request.form.get('address', ''))
        
        db.execute(
            '''UPDATE patients 
               SET name=?, date_of_birth=?, gender=?, blood_type=?, allergies=?, contact=?, address=?, payment_method=?
               WHERE id=?''',
            (name, request.form['date_of_birth'], request.form['gender'],
             request.form['blood_type'], allergies,
             request.form['contact'], address, request.form['payment_method'], id)
        )
        db.commit()
        flash('Patient updated successfully!', 'success')
    except KeyError as e:
        flash(f'Missing field: {str(e)}. Please refresh the page and try again.', 'error')
    except Exception as e:
        flash(f'Error updating patient: {str(e)}', 'error')
    return redirect(url_for('patients'))

@app.route('/patients/delete/<int:id>')
@login_required
def delete_patient(id):
    db = get_db()
    db.execute('DELETE FROM patients WHERE id=?', (id,))
    db.commit()
    flash('Patient deleted successfully!', 'info')
    return redirect(url_for('patients'))

# Vitals
@app.route('/vitals')
@login_required
def vitals():
    db = get_db()
    patients_list = db.execute('SELECT * FROM patients ORDER BY name').fetchall()
    
    recent_vitals = db.execute(
        '''SELECT v.*, p.name as patient_name
           FROM vitals v
           JOIN patients p ON v.patient_id = p.id
           ORDER BY v.recorded_at DESC
           LIMIT 20'''
    ).fetchall()
    
    return render_template('vitals.html', patients=patients_list, vitals=recent_vitals)

@app.route('/vitals/add', methods=['POST'])
@login_required
def add_vitals():
    try:
        db = get_db()
        # Sanitize notes input
        notes = sanitize_input(request.form.get('notes', ''))
        
        db.execute(
            '''INSERT INTO vitals (patient_id, blood_pressure, heart_rate, temperature, 
               respiratory_rate, oxygen_saturation, notes, recorded_by)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (request.form['patient_id'], request.form['blood_pressure'],
             request.form['heart_rate'], request.form['temperature'],
             request.form['respiratory_rate'], request.form.get('oxygen_saturation'),
             notes, session['username'])
        )
        db.commit()
        flash('Vital signs recorded successfully!', 'success')
    except KeyError as e:
        flash(f'Missing field: {str(e)}. Please refresh the page and try again.', 'error')
    except Exception as e:
        flash(f'Error recording vitals: {str(e)}', 'error')
    return redirect(url_for('vitals'))

@app.route('/appointments')
@login_required
def appointments():
    db = get_db()
    patients_list = db.execute('SELECT * FROM patients ORDER BY name').fetchall()
    
    all_appointments = db.execute(
        '''SELECT a.*, p.name as patient_name
           FROM appointments a
           JOIN patients p ON a.patient_id = p.id
           ORDER BY a.date DESC, a.time DESC'''
    ).fetchall()
    
    return render_template('appointments.html', patients=patients_list, appointments=all_appointments)

@app.route('/appointments/add', methods=['POST'])
@login_required
def add_appointment():
    appt_date = request.form['date']
    today = datetime.now().strftime('%Y-%m-%d')
    max_date = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
    
    if appt_date < today:
        flash('Cannot schedule appointments in the past!', 'error')
        return redirect(url_for('appointments'))
    
    if appt_date > max_date:
        flash('Cannot schedule appointments more than 1 year in advance!', 'error')
        return redirect(url_for('appointments'))
    
    db = get_db()
    db.execute(
        '''INSERT INTO appointments (patient_id, date, time, reason, status)
           VALUES (?, ?, ?, ?, ?)''',
        (request.form['patient_id'], request.form['date'],
         request.form['time'], request.form['reason'], 'scheduled')
    )
    db.commit()
    flash('Appointment scheduled successfully!', 'success')
    return redirect(url_for('appointments'))

@app.route('/appointments/update/<int:id>/<status>')
@login_required
def update_appointment_status(id, status):
    db = get_db()
    db.execute('UPDATE appointments SET status=? WHERE id=?', (status, id))
    db.commit()
    flash(f'Appointment marked as {status}!', 'success')
    return redirect(url_for('appointments'))

@app.route('/appointments/delete/<int:id>')
@login_required
def delete_appointment(id):
    db = get_db()
    db.execute('DELETE FROM appointments WHERE id=?', (id,))
    db.commit()
    flash('Appointment deleted successfully!', 'info')
    return redirect(url_for('appointments'))

@app.route('/consultations')
@login_required
def consultations():
    db = get_db()
    consultations_list = db.execute(
        '''SELECT c.*, p.name, p.date_of_birth, p.gender, p.blood_type, 
                  p.allergies, p.contact, p.address
           FROM consultations c
           JOIN patients p ON c.patient_id = p.id
           WHERE c.status = 'waiting'
           ORDER BY c.created_at ASC'''
    ).fetchall()
    
    # Check exam and diagnosis status for each consultation
    enhanced_consultations = []
    for consult in consultations_list:
        consult_dict = dict(consult)
        
        # Check if exam exists and its status
        exam = db.execute(
            'SELECT id, status FROM exams WHERE consultation_id = ? ORDER BY created_at DESC LIMIT 1',
            (consult['id'],)
        ).fetchone()
        consult_dict['has_exam'] = exam is not None
        consult_dict['exam_status'] = exam['status'] if exam else None
        
        # Check if diagnosis exists
        diagnosis = db.execute(
            'SELECT id FROM diagnoses WHERE consultation_id = ? LIMIT 1',
            (consult['id'],)
        ).fetchone()
        consult_dict['has_diagnosis'] = diagnosis is not None
        
        # Check if prescription exists
        prescription = db.execute(
            'SELECT id FROM prescriptions WHERE consultation_id = ? LIMIT 1',
            (consult['id'],)
        ).fetchone()
        consult_dict['has_prescription'] = prescription is not None
        
        enhanced_consultations.append(consult_dict)
    
    return render_template('consultations.html', consultations=enhanced_consultations)

@app.route('/consultations/add/<int:patient_id>')
@login_required
def add_to_consultation(patient_id):
    db = get_db()
    try:
        # Check if patient already in waiting queue
        existing = db.execute(
            'SELECT id FROM consultations WHERE patient_id = ? AND status = "waiting"',
            (patient_id,)
        ).fetchone()
        
        if existing:
            flash('Patient is already in consultation queue!', 'warning')
            return redirect(url_for('patients'))
        
        # Insert new consultation
        db.execute(
            'INSERT INTO consultations (patient_id, added_by) VALUES (?, ?)',
            (patient_id, session['username'])
        )
        db.commit()
        flash('Patient added to consultation queue!', 'success')
    except Exception as e:
        db.rollback()
        # Check if it's a duplicate entry
        existing = db.execute(
            'SELECT * FROM consultations WHERE patient_id = ? AND status = "waiting"',
            (patient_id,)
        ).fetchone()
        if existing:
            flash('Patient is already in consultation queue!', 'warning')
        else:
            flash(f'Error adding patient to queue: {str(e)}', 'error')
    return redirect(url_for('patients'))

@app.route('/consultations/remove/<int:id>')
@login_required
def remove_from_consultation(id):
    db = get_db()
    db.execute('DELETE FROM consultations WHERE id=?', (id,))
    db.commit()
    flash('Patient removed from consultation queue!', 'info')
    return redirect(url_for('consultations'))

@app.route('/consultations/complete/<int:id>')
@login_required
def complete_consultation(id):
    db = get_db()
    db.execute('UPDATE consultations SET status="completed" WHERE id=?', (id,))
    db.commit()
    flash('Consultation completed!', 'success')
    return redirect(url_for('consultations'))

@app.route('/laboratory/results/<int:patient_id>')
@login_required
def get_lab_results(patient_id):
    """Get laboratory results for a patient"""
    db = get_db()
    try:
        results = db.execute('''
            SELECT 
                l.id,
                l.test_name,
                l.test_result_image,
                l.clinical_details,
                l.general_comments,
                l.processed_by,
                l.processed_at
            FROM laboratory l
            WHERE l.patient_id = ? AND l.status = 'completed'
            ORDER BY l.processed_at DESC
        ''', (patient_id,)).fetchall()
        
        # Convert to list of dictionaries
        results_list = []
        for row in results:
            results_list.append({
                'id': row['id'],
                'test_name': row['test_name'],
                'test_result_image': row['test_result_image'],
                'clinical_details': row['clinical_details'],
                'general_comments': row['general_comments'],
                'processed_by': row['processed_by'],
                'processed_at': row['processed_at']
            })
        
        return jsonify({
            'success': True,
            'results': results_list
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/diagnosis/submit', methods=['POST'])
@login_required
def submit_diagnosis():
    """Submit diagnosis for a patient"""
    db = get_db()
    try:
        consultation_id = request.form.get('consultation_id')
        patient_id = request.form.get('patient_id')
        lab_tech_comment = sanitize_input(request.form.get('lab_tech_comment', ''))
        confirmed_diagnosis = sanitize_input(request.form.get('confirmed_diagnosis', ''))
        diagnosis_notes = sanitize_input(request.form.get('diagnosis_notes', ''))
        
        # Validate consultation exists
        consultation = db.execute(
            'SELECT id FROM consultations WHERE id = ? AND patient_id = ?',
            (consultation_id, patient_id)
        ).fetchone()
        
        if not consultation:
            flash('Invalid consultation!', 'error')
            return redirect(url_for('consultations'))
        
        # Validate required fields
        if not confirmed_diagnosis:
            flash('Please select a confirmed diagnosis!', 'error')
            return redirect(url_for('consultations'))
        
        # Collect test feedbacks
        test_feedbacks = []
        for key in request.form:
            if key.startswith('test_feedback_'):
                feedback = sanitize_input(request.form.get(key, ''))
                if feedback:
                    test_feedbacks.append(feedback)
        
        # Combine all feedbacks
        all_feedbacks = '\n---\n'.join(test_feedbacks) if test_feedbacks else ''
        
        # Insert diagnosis record
        db.execute('''
            INSERT INTO diagnoses (
                consultation_id, patient_id, confirmed_diagnosis,
                test_feedbacks, lab_tech_comment, diagnosis_notes,
                diagnosed_by, diagnosed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
        ''', (
            consultation_id, patient_id, confirmed_diagnosis,
            all_feedbacks, lab_tech_comment, diagnosis_notes,
            session['username']
        ))
        
        # Keep consultation status as 'waiting' so patient remains in consultation room
        db.execute('UPDATE consultations SET status=? WHERE id=?', ('waiting', consultation_id))
        
        db.commit()
        flash('Diagnosis submitted successfully! Patient remains in consultation queue.', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Error submitting diagnosis: {str(e)}', 'error')
    
    return redirect(url_for('consultations'))

@app.route('/prescription/submit', methods=['POST'])
@login_required
def submit_prescription():
    """Submit prescription for a patient"""
    db = get_db()
    try:
        consultation_id = request.form.get('consultation_id')
        patient_id = request.form.get('patient_id')
        medicine_count = int(request.form.get('medicine_count', 0))
        
        # Validate consultation exists
        consultation = db.execute(
            'SELECT id FROM consultations WHERE id = ? AND patient_id = ?',
            (consultation_id, patient_id)
        ).fetchone()
        
        if not consultation:
            flash('Invalid consultation!', 'error')
            return redirect(url_for('consultations'))
        
        # Validate required fields
        if not consultation_id or not patient_id or medicine_count < 1:
            flash('Invalid prescription data!', 'error')
            return redirect(url_for('consultations'))
        
        # Collect medicine data
        medicines = []
        for i in range(medicine_count):
            medicine_type = sanitize_input(request.form.get(f'medicine_type_{i}'))
            medicine_amount = sanitize_input(request.form.get(f'medicine_amount_{i}'))
            medicine_times = request.form.get(f'medicine_times_{i}')
            medicine_duration = request.form.get(f'medicine_duration_{i}')
            
            if medicine_type and medicine_amount and medicine_times and medicine_duration:
                try:
                    times = int(medicine_times)
                    duration = int(medicine_duration)
                    
                    # Validate ranges
                    if times < 1 or times > 10:
                        flash('Times per day must be between 1 and 10!', 'error')
                        return redirect(url_for('consultations'))
                    if duration < 1 or duration > 365:
                        flash('Duration must be between 1 and 365 days!', 'error')
                        return redirect(url_for('consultations'))
                    
                    medicines.append({
                        'type': medicine_type,
                        'amount': medicine_amount,
                        'times_per_day': times,
                        'duration_days': duration
                    })
                except ValueError:
                    flash('Invalid times per day or duration value!', 'error')
                    return redirect(url_for('consultations'))
        
        if not medicines:
            flash('Please add at least one complete medicine entry!', 'error')
            return redirect(url_for('consultations'))
        
        if len(medicines) != medicine_count:
            flash(f'Expected {medicine_count} medicines but only {len(medicines)} were complete!', 'error')
            return redirect(url_for('consultations'))
        
        # Get optional fields
        has_prescription_comment = request.form.get('has_prescription_comment', 'no')
        prescription_comment = ''
        if has_prescription_comment == 'yes':
            prescription_comment = sanitize_input(request.form.get('prescription_comment', ''))
            if not prescription_comment:
                flash('Prescription comment cannot be empty if selected!', 'error')
                return redirect(url_for('consultations'))
        
        has_management_plan = request.form.get('has_management_plan', 'no')
        management_plan = ''
        if has_management_plan == 'yes':
            management_plan = sanitize_input(request.form.get('management_plan', ''))
            if not management_plan:
                flash('Management plan cannot be empty if selected!', 'error')
                return redirect(url_for('consultations'))
        
        # Convert medicines list to JSON string
        medicines_json = json.dumps(medicines)
        
        # Insert prescription record with pharmacy_status
        db.execute('''
            INSERT INTO prescriptions (
                consultation_id, patient_id, medicines,
                prescription_comment, management_plan,
                prescribed_by, prescribed_at, status, pharmacy_status
            ) VALUES (?, ?, ?, ?, ?, ?, datetime('now'), 'pending', 'not_sent')
        ''', (
            consultation_id, patient_id, medicines_json,
            prescription_comment, management_plan,
            session['username']
        ))
        
        # Update consultation status to 'completed' since prescription is final step
        db.execute('UPDATE consultations SET status=? WHERE id=?', ('completed', consultation_id))
        
        db.commit()
        flash('Prescription submitted successfully! Patient sent to Account.', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Error submitting prescription: {str(e)}', 'error')
    
    return redirect(url_for('consultations'))

@app.route('/api/patient/<int:patient_id>/history')
@login_required
def get_patient_history(patient_id):
    db = get_db()
    
    # Get patient info
    patient = db.execute('SELECT * FROM patients WHERE id=?', (patient_id,)).fetchone()
    
    # Get vitals history
    vitals = db.execute(
        '''SELECT * FROM vitals 
           WHERE patient_id=? 
           ORDER BY recorded_at DESC''',
        (patient_id,)
    ).fetchall()
    
    # Get appointments history
    appointments = db.execute(
        '''SELECT * FROM appointments 
           WHERE patient_id=? 
           ORDER BY date DESC, time DESC''',
        (patient_id,)
    ).fetchall()
    
    # Get exams history (presenting complaints and history)
    exams = db.execute(
        '''SELECT 
            e.id,
            e.presenting_complaint,
            e.history_of_complaint,
            e.clinical_details,
            e.status,
            e.created_by,
            e.created_at
           FROM exams e
           WHERE e.patient_id=? 
           ORDER BY e.created_at DESC''',
        (patient_id,)
    ).fetchall()
    
    # Get diagnoses history
    diagnoses = db.execute(
        '''SELECT 
            d.id,
            d.confirmed_diagnosis,
            d.test_feedbacks,
            d.lab_tech_comment,
            d.diagnosis_notes,
            d.diagnosed_by,
            d.diagnosed_at
           FROM diagnoses d
           WHERE d.patient_id=? 
           ORDER BY d.diagnosed_at DESC''',
        (patient_id,)
    ).fetchall()
    
    return jsonify({
        'patient': dict(patient) if patient else None,
        'vitals': [dict(v) for v in vitals],
        'appointments': [dict(a) for a in appointments],
        'exams': [dict(e) for e in exams],
        'diagnoses': [dict(d) for d in diagnoses]
    })

@app.route('/api/patients')
@login_required
def api_patients():
    db = get_db()
    patients_list = db.execute('SELECT * FROM patients').fetchall()
    return jsonify([dict(p) for p in patients_list])

@app.route('/exams/add', methods=['POST'])
@login_required
def add_exam():
    db = get_db()
    try:
        consultation_id = request.form.get('consultation_id')
        patient_id = request.form.get('patient_id')
        presenting_complaint = sanitize_input(request.form.get('presenting_complaint', ''))
        history_of_complaint = sanitize_input(request.form.get('history_of_complaint', ''))
        
        # Validate consultation exists
        consultation = db.execute(
            'SELECT id FROM consultations WHERE id = ? AND patient_id = ?',
            (consultation_id, patient_id)
        ).fetchone()
        
        if not consultation:
            flash('Invalid consultation!', 'error')
            return redirect(url_for('consultations'))
        
        # Validate required fields
        if not presenting_complaint or not history_of_complaint:
            flash('Presenting complaint and history are required!', 'error')
            return redirect(url_for('consultations'))
        
        # Check if exam already exists for this consultation
        existing = db.execute(
            'SELECT id FROM exams WHERE consultation_id=? AND status="pending"', 
            (consultation_id,)
        ).fetchone()
        if existing:
            flash('An exam request already exists for this consultation!', 'warning')
            return redirect(url_for('consultations'))
        
        # Get test selections
        random_blood_sugar = 1 if request.form.get('random_blood_sugar') else 0
        fasting_blood_sugar = 1 if request.form.get('fasting_blood_sugar') else 0
        liver_function = 1 if request.form.get('liver_function') else 0
        full_blood_count = 1 if request.form.get('full_blood_count') else 0
        lipid_profile = 1 if request.form.get('lipid_profile') else 0
        kidney_function = 1 if request.form.get('kidney_function') else 0
        thyroid_function = 1 if request.form.get('thyroid_function') else 0
        urinalysis = 1 if request.form.get('urinalysis') else 0
        stool_examination = 1 if request.form.get('stool_examination') else 0
        chest_xray = 1 if request.form.get('chest_xray') else 0
        ecg = 1 if request.form.get('ecg') else 0
        ultrasound = 1 if request.form.get('ultrasound') else 0
        
        # Get diagnosis recommendation
        recommend_diagnosis = 1 if request.form.get('recommend_diagnosis') else 0
        clinical_details = sanitize_input(request.form.get('clinical_details', ''))
        
        # Validate at least one test is selected
        tests_selected = any([
            random_blood_sugar, fasting_blood_sugar, liver_function, full_blood_count,
            lipid_profile, kidney_function, thyroid_function, urinalysis,
            stool_examination, chest_xray, ecg, ultrasound
        ])
        if not tests_selected:
            flash('Please select at least one test!', 'error')
            return redirect(url_for('consultations'))
        
        # Insert exam record
        cursor = db.execute('''
            INSERT INTO exams (
                consultation_id, patient_id, presenting_complaint, history_of_complaint,
                random_blood_sugar, fasting_blood_sugar, liver_function, full_blood_count,
                lipid_profile, kidney_function, thyroid_function, urinalysis,
                stool_examination, chest_xray, ecg, ultrasound,
                recommend_diagnosis, clinical_details, status, created_by, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        ''', (
            consultation_id, patient_id, presenting_complaint, history_of_complaint,
            random_blood_sugar, fasting_blood_sugar, liver_function, full_blood_count,
            lipid_profile, kidney_function, thyroid_function, urinalysis,
            stool_examination, chest_xray, ecg, ultrasound,
            recommend_diagnosis, clinical_details, 'pending', session['username']
        ))
        
        exam_id = cursor.lastrowid
        
        # Update consultation status instead of deleting (prevents CASCADE delete of exam)
        db.execute('UPDATE consultations SET status=? WHERE id=?', ('sent_to_lab', consultation_id))
        
        db.commit()
        flash('Exam request sent to laboratory successfully!', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Error submitting exam: {str(e)}', 'error')
    
    return redirect(url_for('consultations'))

@app.route('/laboratory')
@login_required
def laboratory():
    db = get_db()
    
    lab_patients = db.execute('''
        SELECT 
            e.id as exam_id,
            e.patient_id,
            p.name,
            p.gender,
            p.date_of_birth,
            e.presenting_complaint,
            e.history_of_complaint,
            e.random_blood_sugar,
            e.fasting_blood_sugar,
            e.liver_function,
            e.full_blood_count,
            e.lipid_profile,
            e.kidney_function,
            e.thyroid_function,
            e.urinalysis,
            e.stool_examination,
            e.chest_xray,
            e.ecg,
            e.ultrasound,
            e.clinical_details,
            e.created_at
        FROM exams e
        JOIN patients p ON e.patient_id = p.id
        WHERE e.status IN ('pending', 'in_progress')
        ORDER BY e.created_at ASC
    ''').fetchall()
    
    return render_template('laboratory.html', lab_patients=lab_patients)

@app.route('/laboratory/submit', methods=['POST'])
@login_required
def submit_lab_results():
    db = get_db()
    try:
        exam_id = request.form.get('exam_id')
        patient_id = request.form.get('patient_id')
        general_comments = sanitize_input(request.form.get('general_comments', ''))
        
        # Get the exam details to know which tests were requested
        exam = db.execute('SELECT * FROM exams WHERE id=?', (exam_id,)).fetchone()
        
        if not exam:
            flash('Exam not found!', 'error')
            return redirect(url_for('laboratory'))
        
        # Mark exam as in progress
        db.execute('UPDATE exams SET status=? WHERE id=?', ('in_progress', exam_id))
        
        # Process uploaded test images
        test_fields = [
            ('rbs', 'random_blood_sugar', 'Random Blood Sugar'),
            ('fbs', 'fasting_blood_sugar', 'Fasting Blood Sugar'),
            ('lft', 'liver_function', 'Liver Function Test'),
            ('cbc', 'full_blood_count', 'Complete Blood Count'),
            ('lipid', 'lipid_profile', 'Lipid Profile'),
            ('kft', 'kidney_function', 'Kidney Function Test'),
            ('thyroid', 'thyroid_function', 'Thyroid Function Test'),
            ('urine', 'urinalysis', 'Urinalysis'),
            ('stool', 'stool_examination', 'Stool Examination'),
            ('xray', 'chest_xray', 'Chest X-Ray'),
            ('ecg', 'ecg', 'Electrocardiogram'),
            ('ultrasound', 'ultrasound', 'Ultrasound')
        ]
        
        # Create uploads directory if it doesn't exist
        upload_folder = app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        results_saved = False
        saved_files = []  # Track saved files for rollback
        
        for test_key, db_field, test_name in test_fields:
            if exam[db_field] == 1:
                file_key = f'test_{test_key}_image'
                
                # Check if image was uploaded for this test
                if file_key in request.files:
                    file = request.files[file_key]
                    if file and file.filename:
                        # Validate file
                        if not allowed_file(file.filename):
                            # Rollback: delete already saved files
                            for saved_file in saved_files:
                                try:
                                    os.remove(saved_file)
                                except:
                                    pass
                            flash(f'Invalid file type for {test_name}. Allowed types: png, jpg, jpeg, gif, pdf', 'error')
                            return redirect(url_for('laboratory'))
                        
                        try:
                            # Secure the filename
                            original_filename = secure_filename(file.filename)
                            
                            # Check if file has extension
                            if '.' not in original_filename:
                                flash(f'File must have an extension for {test_name}', 'error')
                                continue
                            
                            # Generate unique filename
                            ext = original_filename.rsplit('.', 1)[1].lower()
                            filename = f"{patient_id}_{test_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
                            filepath = os.path.join(upload_folder, filename)
                            
                            # Save file with error handling
                            file.save(filepath)
                            saved_files.append(filepath)
                            
                            # Store relative path for web access
                            relative_path = f"/static/lab_results/{filename}"
                            
                            # Insert laboratory record
                            db.execute('''
                                INSERT INTO laboratory (
                                    exam_id, patient_id, test_name, test_result_image,
                                    clinical_details, general_comments, status,
                                    processed_by, processed_at
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
                            ''', (
                                exam_id, patient_id, test_name, relative_path,
                                exam['clinical_details'], general_comments, 'completed',
                                session['username']
                            ))
                            results_saved = True
                        except Exception as file_error:
                            # Rollback: delete already saved files
                            for saved_file in saved_files:
                                try:
                                    os.remove(saved_file)
                                except:
                                    pass
                            raise Exception(f"Error saving file for {test_name}: {str(file_error)}")
        
        # Update exam status
        if results_saved:
            db.execute('UPDATE exams SET status=? WHERE id=?', ('completed', exam_id))
            
            # Send patient back to consultation queue after lab work is completed
            db.execute('UPDATE consultations SET status=? WHERE id=?', ('waiting', exam['consultation_id']))
            
            db.commit()
            flash('Laboratory results submitted successfully! Patient sent back to consultation queue.', 'success')
        else:
            db.rollback()
            flash('No test results were uploaded. Please upload at least one result.', 'warning')
            
    except Exception as e:
        db.rollback()
        flash(f'Error submitting results: {str(e)}', 'error')
    
    return redirect(url_for('laboratory'))

@app.route('/account')
@login_required
def account():
    """Display patients with prescriptions pending payment"""
    db = get_db()
    
    account_patients = db.execute('''
        SELECT 
            pr.id as prescription_id,
            pr.patient_id,
            p.name,
            p.gender,
            p.payment_method,
            pr.medicines,
            pr.prescription_comment,
            pr.management_plan,
            pr.prescribed_by,
            pr.prescribed_at,
            pr.status,
            pr.pharmacy_status,
            c.id as consultation_id
        FROM prescriptions pr
        JOIN patients p ON pr.patient_id = p.id
        JOIN consultations c ON pr.consultation_id = c.id
        WHERE pr.pharmacy_status = 'not_sent'
        ORDER BY pr.prescribed_at DESC
    ''').fetchall()
    
    return render_template('account.html', patients=account_patients)

@app.route('/account/complete/<int:prescription_id>', methods=['POST'])
@login_required
def complete_payment(prescription_id):
    """Mark prescription as paid"""
    db = get_db()
    try:
        payment_method = request.form.get('payment_method')
        
        if not payment_method:
            flash('Please select a payment method!', 'error')
            return redirect(url_for('account'))
        
        # Update payment method in patients table
        prescription = db.execute('SELECT patient_id FROM prescriptions WHERE id=?', (prescription_id,)).fetchone()
        
        if prescription:
            db.execute('UPDATE patients SET payment_method=? WHERE id=?', 
                      (sanitize_input(payment_method), prescription['patient_id']))
            
            # Update prescription status
            db.execute('UPDATE prescriptions SET status=? WHERE id=?', ('paid', prescription_id))
            
            db.commit()
            flash('Payment completed successfully!', 'success')
        else:
            flash('Prescription not found!', 'error')
            
    except Exception as e:
        db.rollback()
        flash(f'Error processing payment: {str(e)}', 'error')
    
    return redirect(url_for('account'))

@app.route('/account/send-to-pharmacy/<int:prescription_id>', methods=['POST'])
@login_required
def send_to_pharmacy(prescription_id):
    """Send paid prescription to pharmacy"""
    db = get_db()
    try:
        # Verify prescription is paid
        prescription = db.execute('SELECT status FROM prescriptions WHERE id=?', (prescription_id,)).fetchone()
        
        if not prescription:
            flash('Prescription not found!', 'error')
        elif prescription['status'] != 'paid':
            flash('Payment must be completed before sending to pharmacy!', 'error')
        else:
            # Update pharmacy status
            db.execute('UPDATE prescriptions SET pharmacy_status=? WHERE id=?', ('sent', prescription_id))
            db.commit()
            flash('Patient sent to Pharmacy successfully!', 'success')
            
    except Exception as e:
        db.rollback()
        flash(f'Error sending to pharmacy: {str(e)}', 'error')
    
    return redirect(url_for('account'))

@app.route('/pharmacy')
@login_required
def pharmacy():
    """Display patients sent to pharmacy"""
    db = get_db()
    
    pharmacy_patients = db.execute('''
        SELECT 
            pr.id as prescription_id,
            pr.patient_id,
            p.name,
            p.gender,
            p.date_of_birth,
            p.contact,
            p.payment_method,
            pr.medicines,
            pr.prescription_comment,
            pr.management_plan,
            pr.prescribed_by,
            pr.prescribed_at,
            pr.status
        FROM prescriptions pr
        JOIN patients p ON pr.patient_id = p.id
        WHERE pr.pharmacy_status = 'sent'
        ORDER BY pr.prescribed_at DESC
    ''').fetchall()
    
    return render_template('pharmacy.html', patients=pharmacy_patients)

@app.route('/pharmacy/complete/<int:prescription_id>', methods=['POST'])
@login_required
def complete_pharmacy(prescription_id):
    """Complete pharmacy service and remove all patient records"""
    db = get_db()
    try:
        # Get patient information before deletion
        prescription = db.execute(
            'SELECT patient_id FROM prescriptions WHERE id=?', 
            (prescription_id,)
        ).fetchone()
        
        if prescription:
            patient_id = prescription['patient_id']
            
            # Delete patient record - this will cascade delete all related records
            # (prescriptions, consultations, exams, laboratory, diagnoses, vitals, appointments)
            db.execute('DELETE FROM patients WHERE id=?', (patient_id,))
            db.commit()
            
            flash('Patient completed successfully! All records removed.', 'success')
        else:
            flash('Prescription not found!', 'error')
            
    except Exception as e:
        db.rollback()
        flash(f'Error completing pharmacy service: {str(e)}', 'error')
    
    return redirect(url_for('pharmacy'))

@app.route('/pharmacy/cancel/<int:prescription_id>', methods=['POST'])
@login_required
def cancel_pharmacy(prescription_id):
    """Cancel pharmacy service and send back to account"""
    db = get_db()
    try:
        # Update pharmacy status back to not_sent
        db.execute('UPDATE prescriptions SET pharmacy_status=? WHERE id=?', ('not_sent', prescription_id))
        db.commit()
        flash('Pharmacy service cancelled. Patient sent back to Account.', 'info')
            
    except Exception as e:
        db.rollback()
        flash(f'Error cancelling pharmacy service: {str(e)}', 'error')
    
    return redirect(url_for('pharmacy'))

@app.route('/exams/cancel/<int:exam_id>', methods=['POST'])
@login_required
def cancel_exam(exam_id):
    """Cancel a pending exam request"""
    db = get_db()
    try:
        # Check if exam exists and is cancellable
        exam = db.execute('SELECT * FROM exams WHERE id=?', (exam_id,)).fetchone()
        
        if not exam:
            flash('Exam not found!', 'error')
            return redirect(url_for('laboratory'))
        
        # Only allow cancellation if status is pending or in_progress
        if exam['status'] not in ('pending', 'in_progress'):
            flash('Cannot cancel exam with status: ' + exam['status'], 'error')
            return redirect(url_for('laboratory'))
        
        # Update status to cancelled
        db.execute('UPDATE exams SET status=? WHERE id=?', ('cancelled', exam_id))
        
        # Also update associated consultation status back to waiting
        db.execute('UPDATE consultations SET status=? WHERE id=?', ('waiting', exam['consultation_id']))
        
        db.commit()
        flash('Exam cancelled successfully!', 'success')
        
    except Exception as e:
        db.rollback()
        flash(f'Error cancelling exam: {str(e)}', 'error')
    
    return redirect(url_for('laboratory'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)