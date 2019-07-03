from app import db
from app import login_manager
from flask_login import UserMixin
from sqlalchemy import and_

# Add classes corresponding to sqlite database tables

class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    gender = db.Column(db.String(10))
    email_id = db.Column(db.String(60))
    age = db.Column(db.Integer)

    Cart_List = db.relationship("Cart")

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
    user_id = db.Column(db.String(60), primary_key=True)
    email_id = db.Column(db.String(60))
    password = db.Column(db.String(60))

    def __repr__(self):
        return "Credentials('{self.email_id}', '{self.password}')"

class Product(db.Model):
    __tablename__ = 'Product'
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer)
    name = db.Column(db.String(60))
    price = db.Column(db.Integer)

    Cart_Product_List = db.relationship("Cart")
    Meal_Product_List = db.relationship("Meal")

    def __repr__(self):
        return "Product('{self.product_id}', '{self.category_id}', '{self.product_name}', '{self.price}')"

class Meal(db.Model):
    __tablename__ = 'Meal'
    meal_id = db.Column(db.Integer, db.ForeignKey('MealDetails.meal_id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.product_id'), primary_key=True)

    def __repr__(self):
        return "Meal('{self.meal_id}', '{self.product_id}')"

class MealDetails(db.Model):
    __tablename__ = 'MealDetails'
    meal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60))
    availability = db.Column(db.String(60))
    price =db.Column(db.Integer)

    Meal_list = db.relationship("Meal")

    def __repr__(self):
        return "MealDetails('{self.meal_id}', '{self.meal_name}', '{self.meal_availability}', '{self.meal_price}')"

class Cart(db.Model):
    __tablename__ = 'Cart'
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.product_id'), nullable=False, primary_key=True)

    def __repr__(self):
        return "Meal('{self.user_id}', '{self.product_id}')"
