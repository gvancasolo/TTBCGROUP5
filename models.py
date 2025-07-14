from ext import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer(), primary_key=True)
    name  = db.Column(db.String(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    img = db.Column(db.String, nullable=False, default="default_image.jbg")

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    gender = db.Column(db.String)
    birthday = db.Column(db.String)
    role = db.Column(db.String(), nullable=False, default="Guest")

    def __init__(self, username, password, gender=None, birthday=None, role="Guest"):
        self.username = username
        self.password = generate_password_hash(password)
        self.gender = gender
        self.birthday = birthday
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
