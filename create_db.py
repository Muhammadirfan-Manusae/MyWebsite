from app import app
from models import db, Admin, Content
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()

    admin = Admin(username="admin", password=generate_password_hash("1234"))
    db.session.add(admin)

    db.session.add(Content(title="Welcome", body="ยินดีต้อนรับสู่เว็บไซต์"))
    db.session.add(Content(title="About Us", body="นี่คือหน้าข้อมูลเกี่ยวกับเรา"))

    db.session.commit()
    print("Database created successfully!")
