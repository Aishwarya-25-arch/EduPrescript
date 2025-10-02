from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

import os

app = Flask(__name__)
app.secret_key = "super_secret_key_123"  


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role'].strip().lower()

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email=? AND password=? AND role=?", (email, password, role))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['role'] = role
            if role == 'student':
                return redirect(url_for('student_dashboard'))
            else:
                return redirect(url_for('teacher_dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials. Try again.")

    return render_template('login.html')





@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role'].strip().lower()

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password, role) VALUES (?, ?, ?)", (email, password, role))
        user_id = cursor.lastrowid

        # If new user is a student, add them to students table
        if role == 'student':
            cursor.execute('''
                INSERT INTO students (user_id, name, grade, attendance, assignments_done, assignments_total, risk_score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, "New Student", "Grade 10", 0, 0, 0, 0))

        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')




@app.route('/student/dashboard')
def student_dashboard():
    print("Session user_id:", session.get('user_id'))
    print("Session role:", session.get('role'))

    if session.get('role') != 'student':
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, grade, attendance, assignments_done, assignments_total, risk_score FROM students WHERE user_id=?", (user_id,))
    student = cursor.fetchone()
    conn.close()

    return render_template('student_dashboard.html', student=student, show_sidebar=True)


@app.route('/teacher/dashboard')
def teacher_dashboard():
    if session.get('role') != 'teacher':
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, grade, attendance, risk_score FROM students")
    students = cursor.fetchall()
    conn.close()

    return render_template('teacher_dashboard.html', students=students, show_sidebar=True)



@app.route('/teacher/student/<int:student_id>')
def student_profile(student_id):
    if session.get('role') != 'teacher':
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, grade, attendance, assignments_done, assignments_total, risk_score FROM students WHERE id=?", (student_id,))


    student = cursor.fetchone()

    cursor.execute("SELECT item, completed FROM prescriptions WHERE student_id=?", (student_id,))
    prescriptions = cursor.fetchall()

    cursor.execute("SELECT teacher_note FROM notes WHERE student_id=?", (student_id,))
    note = cursor.fetchone()

    conn.close()

    return render_template('student_profile.html', student=student, prescriptions=prescriptions, note=note, show_sidebar=True)


@app.route('/student/prescriptions')
def prescriptions():
    if session.get('role') != 'student':
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM students WHERE user_id=?", (user_id,))
    student_row = cursor.fetchone()

    if student_row:
        student_id = student_row[0]
        cursor.execute("SELECT item, completed FROM prescriptions WHERE student_id=?", (student_id,))
        items = cursor.fetchall()
    else:
        items = []

    conn.close()
    return render_template('prescriptions.html', items=items, show_sidebar=True)



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
