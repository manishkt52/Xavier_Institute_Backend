import sqlite3

# connect to DB
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# 1️⃣ Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    email TEXT UNIQUE,

    name TEXT,

    role TEXT DEFAULT 'user',

    student_id TEXT UNIQUE,

    password TEXT
)
""")

# 2️⃣ Insert admin user (Google login)
cursor.execute("""
INSERT OR IGNORE INTO users
(email, name, role)
VALUES (?, ?, ?)
""", (
    "manishkt52@gmail.com",
    "Manish Kumar",
    "admin"
))

# 3️⃣ Insert manual student users
cursor.execute("""
INSERT OR IGNORE INTO users
(email, name, role, student_id, password)
VALUES (?, ?, ?, ?, ?)
""", (
    "student1@gmail.com",
    "Student One",
    "student",
    "stu101",
    "pass123"
))

cursor.execute("""
INSERT OR IGNORE INTO users
(email, name, role, student_id, password)
VALUES (?, ?, ?, ?, ?)
""", (
    "student2@gmail.com",
    "Student Two",
    "student",
    "stu102",
    "pass456"
))

# 4️⃣ Save
conn.commit()

# 5️⃣ Verify
cursor.execute("""
SELECT
    id,
    email,
    name,
    role,
    student_id,
    password
FROM users
""")

rows = cursor.fetchall()

print("Users in DB:")

for row in rows:
    print(row)

# close
conn.close()