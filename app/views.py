# This is Main Controller of the webapp
from flask import Flask
from flask_nav.elements import Navbar, Subgroup, View, Link, Text, Separator
from flask import render_template
from flask import url_for, redirect, request, make_response,flash
import sqlalchemy
from app import app, db, nav

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_
from flask_login import current_user, login_user
from flask_wtf import FlaskForm
from flask_login import logout_user
from sqlalchemy import update
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import func
from sqlalchemy import desc
import json
from app.models import User, Credentials, Product

# Use SQLAlchemy for SQLite queries, install and import packages here as and when required.

## VIEW 1 ROUTE
@app.route('/')
def firstpage():
    return render_template('FirstPage.html',title='First Page')

## VIEW 2 ROUTE
@app.route('/Registration')
def Registration():
    return render_template('Register.html',title='Registration Page')

## VIEW 3 ROUTE
@app.route('/Register', methods = ['GET', 'POST'])
def Register():
    # Use post method as User Info should not be passed through URL.
    # 1. Get Form content (User info) by POST method.
    # 2. Encrypt Password and Add entry in Credentials table with EmailID and encrypted password.
    # 3. Add entry in User table with user info.
    # 4. Commit database changes.
    # 5. render Login page if successfully registered else display error message.

    if request.method == 'POST':
       if not request.form['name'] or not request.form['email'] or not request.form['password'] or not request.form['gender'] or not request.form['age']:
          flash('Please enter all the fields', 'error')
       else:
          password = request.form['password']
          pw_hash = generate_password_hash(password)
          User.Num_Users += 1
          user1 = User(user_id = User.Num_Users , name = request.form['name'], email_id = request.form['email'], gender = request.form['gender'], age = request.form['age'])
          Credential1 = Credentials(email_id = request.form['email'], password = pw_hash)

          db.session.add(user1)
          db.session.add(Credential1)
          db.session.commit()

          flash('Record was successfully added')
    return render_template('Login.html')

@app.route('/Logging', methods = ['GET', 'POST'])
def Logging():
    return render_template('Login.html')

@app.route('/Home', methods = ['GET', 'POST'])
def ViewAllProducts():
    # 1. Database query to get all products from Products table. [ProductID, Name as key:val pair if required]
    # 2. render HomePage page with parameter value = above queried list.

    Product_List = Product.query.with_entities(Product.name, Product.price).all()
    print("Product_List", Product_List)

    return render_template('HomePage.html', ProductList=json.dumps(Product_List))

## VIEW 3 ROUTE
@app.route('/Login', methods = ['POST'])
def Login():
    # Use post method as User credentials should not be passed through URL.
    # 1. Get Form content (User credentials) by POST method.
    # 2. Authenticate user from database. Do below steps if authenticated else show error msg.
    # 3. Call ViewAllProducts()

    form = FlaskForm()
    Authenticate = False

    if request.method == 'POST':
        emailid=request.form['email']
        password=request.form['password']

        user = User.query.filter(User.email_id==emailid).first()
        Cred = Credentials.query.filter(Credentials.email_id==emailid).first()

        if user and Cred and check_password_hash(Cred.password, password):
            login_user(user)
            user.is_authenticated = True
            Authenticate = True
            flash('Successful login!')

    if Authenticate == True :
        return redirect('/Home')
    else :
        return render_template('Login.html')

@app.route('/AddToCart/<ProductID>', methods = ['GET', 'POST'])
def AddToCart(ProductID):
    # 1. Get current User's ID to add product in particular user's cart.
    # 2. Get ProductID as a parameter.
    # 3. Add new entry in Cart table with above UserID and ProductID.
    # 4. Commit database after above entry.
    # 5. return some boolean value which will be used in HomePage view to decide whether enable or disable "Add to Cart" button.
    # 6. You can check other alternative OR refer add to favorites functionality in sample Gaana app.

    uid = current_user.get_id()
    CartObject = Cart(user_id = uid, product_id = ProductID)
    db.session.add(CartObject)
    db.session.commit()
    return

@app.route('/ViewCart', methods = ['GET', 'POST'])
def ViewCart():
    # 1. Get current User's ID to display products in particular user's cart.
    # 2. Get all products in cart from cart table using above user ID.
    # 3. Get corresponding product names from product detail table.
    # 4. render CartDetailPage with parameter = List of product names in cart.
    # 5. You can pass ProductID list along with is as list of key:value pair if ids are also required.

    uid = current_user.get_id()
    Cart_Entries = Cart.query.filter(Cart.user_id == uid).all()

    Cart_Product_Names = []
    for entry in Cart_Entries:
        Cart_Product_Id = entry.product_id
        Product_obj = Product.query.filter(Product.product_id == entry.product_id).first()
        Cart_Product_Names.append(Product_obj.product_name)

    return render_template('CartDetailPage.html', CartList=Cart_Product_Names)

@app.route('/ViewRecommendation', methods = ['GET', 'POST'])
def ViewRecommendation():
    # 1. Get current User's ID to display products in particular user's cart.
    # 2. Get all products in cart from cart table using above user ID.
    # 3. Send above UserID and list of cart productIDs in appropriate format to Tensoflow-serving which is serving Meal Recommendation ML model.
    # 4. Get response from TF-Serving : List of ProductIDs user id most likely to buy next.
    # 5. Database query to find most suitable MealIDs from above two lists : cartlist and predicted list. [Top 5 meals]
    # 6. Render MealRecommendation page with List of Meal names as parameter (MealIDs can be passed if required as key:val pairs).

    uid = current_user.get_id()
    Cart_Entries = Cart.query.filter(Cart.user_id == uid).all()

    Cart_Product_Ids = []
    for entry in Cart_Entries :
        Cart_Product_Ids.append(Cart_Entries.product_id)

    Obj_To_ML_Algo = {}
    Obj_To_ML_Algo['CustomerID'] = uid
    Obj_To_ML_Algo['ProductID'] = Cart_Product_Ids

    # Call ML Algo with above object and get list of product IDs user will most likely to buy next.

    Next_To_Buy_Ids = []

    # Product list will contain product Ids in priority : 1. Common in cart and next to buy 2. Only in Cart 3. Only in Next to buy
    Products_List = []
    for cart_product in Cart_Product_Ids :
        if cart_product in Next_To_Buy_Ids :
            Products_List.append(cart_product)
            Next_To_Buy_Ids.remove(cart_product)
            Cart_Product_Ids.remove(cart_product)

    for cart_product in Cart_Product_Ids :
        Products_List.append(cart_product)

    for next_id in Next_To_Buy_Ids:
        Products_List.append(next_id)




    return render_template('MealRecommendation.html', MealList=[])

@app.route('/AddMissingProduct/<MealID>', methods = ['GET', 'POST'])
def AddMissingProduct(MealID):
    # 1. Get current User's ID to get products in particular user's cart.
    # 2. Get all products in cart from cart table using above user ID.
    # 3. Get MealID as paramter.
    # 4. DB query to get missing productIDs using above MealID and List of Cart ProductIDs.
    # 5. DB Query to get corresponding Product Names from Product Detail table. [ProductID, Name as key:val pair if required]
    # 4. render HomePage page with parameter value = above queried list.
    return render_template('HomePage.html', ProductList=[])

@app.route('/logout', methods = ['GET', 'POST'])
def logout_Dummy():
    user = current_user
    user.is_authenticated = False
    logout_user()
    return render_template('firstpage.html', message = "Logged out successfully")

# Future Scope :
# 1. Product Details page
# 2. Meal Details Page
# 3. Quantity of Products
# 4. Invoice generation
# 5. Once checkout is done, meals/products purchased then add it as historic purchase in DB.
# 6. Dynamic Meals Recommendation as cart content changes
# 7. Analysis according to no. of clicks on checkout without viewing recommendations,
# no. of clicks on meal links but meal not purchased, Meals or missing ingredients are prefered,
# Missing ingredients are only viewed or purchased --> this will help to measure how successful is recommeder system.
