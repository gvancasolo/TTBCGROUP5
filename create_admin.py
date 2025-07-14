from ext import app, db
from models import User

with app.app_context():
    admin = User(
        username="Admin",
        password="dzegviontop",
        gender="ქალი",
        birthday="2008-09-15",
        role="Admin"
    )
    db.session.add(admin)
    db.session.commit()
    print("Admin user created!")
