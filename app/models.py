from app import db
from app import login_manager
from flask_login import UserMixin
from sqlalchemy import and_

# Add classes corresponding to sqlite database tables

class User(db.Model):
    __tablename__ = 'User'
    Num_Users = 0;
    user_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email_id = db.Column(db.String(60), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "User('{self.user_id}', '{self.name}', '{self.email_id}', '{self.gender}', '{self.age}')"

    def is_active(self):
        return True

    def is_authenticated(self):
        """email=request.form['email']
        password=request.form['password']
        print email
        print password
        data= User.query.filter(and_(User.email_id == email, User.password == password)).first()
        print data
        if data:
            return True
        else:
            return False"""
        return self.is_authenticated

    def get_id(self):
        return self.user_id

    def is_anonymous():
        return False


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Credentials(db.Model):
    __tablename__ = 'Credentials'
    email_id = db.Column(db.String(60), nullable=False, primary_key=True)
    password = db.Column(db.String(60), nullable=False, unique=True)

    def __repr__(self):
        return "Credentials('{self.email_id}', '{self.password}')"

class Product(db.Model):
    __tablename__ = 'Product'
    product_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, nullable=False, )
    product_name = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return "Credentials('{self.product_id}', '{self.category_id}', '{self.product_name}')"
