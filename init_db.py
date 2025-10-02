import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    grade TEXT,
    attendance INTEGER,
    assignments_done INTEGER,
    assignments_total INTEGER,
    risk_score INTEGER
)
''')

cursor.execute('''
CREATE TABLE prescriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    item TEXT,
    completed BOOLEAN
)
''')

cursor.execute('''
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    teacher_note TEXT
)
''')


# Insert sample users
cursor.execute("INSERT INTO users (email, password, role) VALUES ('student@example.com', 'pass123', 'Student')")
cursor.execute("INSERT INTO users (email, password, role) VALUES ('teacher@example.com', 'pass456', 'Teacher')")

# Insert sample student
cursor.execute('''
INSERT INTO students (user_id, name, grade, attendance, assignments_done, assignments_total, risk_score)
VALUES (1, 'Aishwarya', 'Grade 10', 85, 7, 10, 40)

''')


# Insert sample prescriptions
cursor.execute("INSERT INTO prescriptions (student_id, item, completed) VALUES (1, 'Attend extra math sessions', 0)")
cursor.execute("INSERT INTO prescriptions (student_id, item, completed) VALUES (1, 'Complete science worksheet', 0)")

# Insert sample note
cursor.execute("INSERT INTO notes (student_id, teacher_note) VALUES (1, 'Needs help with algebra and time management.')")

conn.commit()
conn.close()

print("✅ Database created and populated successfully.")
