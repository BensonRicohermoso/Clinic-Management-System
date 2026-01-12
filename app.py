# Clinical Management System
# Patient tracking and vitals monitoring for nursing staff

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta
import os
from models.database import init_db, get_db

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'nursing-cms-secret-key-2026')
app.config['DATABASE'] = 'clinical_management.db'

# init db
with app.app_context():
    init_db()

# login required decorator
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
    
    # get stats
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
    return render_template('patients.html', patients=patients_list)

@app.route('/patients/add', methods=['POST'])
@login_required
def add_patient():
    try:
        db = get_db()
        db.execute(
            '''INSERT INTO patients (name, date_of_birth, gender, blood_type, allergies, contact, address)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (request.form['name'], request.form['date_of_birth'], request.form['gender'],
             request.form['blood_type'], request.form['allergies'],
             request.form['contact'], request.form['address'])
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
    db = get_db()
    db.execute(
        '''UPDATE patients 
           SET name=?, date_of_birth=?, gender=?, blood_type=?, allergies=?, contact=?, address=?
           WHERE id=?''',
        (request.form['name'], request.form['date_of_birth'], request.form['gender'],
         request.form['blood_type'], request.form['allergies'],
         request.form['contact'], request.form['address'], id)
    )
    db.commit()
    flash('Patient updated successfully!', 'success')
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
    db = get_db()
    db.execute(
        '''INSERT INTO vitals (patient_id, blood_pressure, heart_rate, temperature, 
           respiratory_rate, oxygen_saturation, notes, recorded_by)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (request.form['patient_id'], request.form['blood_pressure'],
         request.form['heart_rate'], request.form['temperature'],
         request.form['respiratory_rate'], request.form.get('oxygen_saturation'),
         request.form.get('notes'), session['username'])
    )
    db.commit()
    flash('Vital signs recorded successfully!', 'success')
    return redirect(url_for('vitals'))

# Appointments
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

# TODO: add more api endpoints later
@app.route('/api/patients')
@login_required
def api_patients():
    db = get_db()
    patients_list = db.execute('SELECT * FROM patients').fetchall()
    return jsonify([dict(p) for p in patients_list])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)