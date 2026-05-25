from app.db.database import SessionLocal
from app.models.user import User

# connect to Neon DB
db = SessionLocal()

# users to insert
users = [
    # 1️⃣ Admin user (Google login)
    User(
        email="manishkt52@gmail.com",
        name="Manish Kumar",
        role="admin",
    ),

    # 2️⃣ Manual student
    User(
        email="student1@gmail.com",
        name="Student One",
        role="student",
        student_id="stu101",
        password="pass123",
    ),

    # 3️⃣ Manual student
    User(
        email="student2@gmail.com",
        name="Student Two",
        role="student",
        student_id="stu102",
        password="pass456",
    ),
]

# insert only if user doesn't already exist
for new_user in users:

    existing = (
        db.query(User)
        .filter(User.email == new_user.email)
        .first()
    )

    if not existing:
        db.add(new_user)

# save changes
db.commit()

# verify data
rows = db.query(User).all()

print("Users in DB:")

for user in rows:
    print(
        user.id,
        user.email,
        user.name,
        user.role,
        user.student_id,
        user.password,
    )

# close DB
db.close()