import sqlite3

# 🔐 Credentials to test
email = 'student@example.com'
password = 'pass123'
role = 'student'  # Make sure this matches exactly what's in the DB

# 🔍 Connect to database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# 🧠 Run login query
cursor.execute("SELECT id FROM users WHERE email=? AND password=? AND role=?", (email, password, role))
user = cursor.fetchone()

# ✅ Result
if user:
    print("✅ Login successful! User ID:", user[0])
else:
    print("❌ Login failed. No matching user found.")

conn.close()
