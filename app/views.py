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
from sqlalchemy.orm import load_only
import json
from app.models import User, Credentials, Product, Meal, MealDetails, Cart

# Use SQLAlchemy for SQLite queries, install and import packages here as and when required.

## VIEW 1 ROUTE
@app.route('/')
def firstpage():
    # Encrypt_Password()
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
          # pw_hash = generate_password_hash(password)

          Num_Users = len(User.query.all())
          user1 = User(user_id = Num_Users+1 , name = request.form['name'], email_id = request.form['email'], gender = request.form['gender'], age = request.form['age'])
          # Credential1 = Credentials(user_id = Num_Users+1, email_id = request.form['email'], password = pw_hash)
          Credential1 = Credentials(user_id = Num_Users+1, email_id = request.form['email'], password = password)

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
    # 3. Send list of products already in cart as parameter

    Product_Tuples = Product.query.with_entities(Product.product_id, Product.name, Product.price).all()
    Product_List = []
    for i in range(1,len(Product_Tuples)):
        Product_List.append(list(Product_Tuples[i]))

    uid = current_user.get_id()
    Cart_Products = Cart.query.filter(Cart.user_id == uid).all()

    Already_Cart = []
    for product in Cart_Products:
        Already_Cart.append(product.product_id)

    return render_template('HomePage.html', ProductList=Product_List, Cart_Products=Already_Cart, Heading="All Products", Current_meal = -1)

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

        print("Creds: ", emailid, password)

        users = User.query.filter(User.email_id==emailid).all()
        Creds = Credentials.query.filter(Credentials.email_id==emailid).all()

        # if user and Cred and check_password_hash(Cred.password, password):
        #     login_user(user)
        #     user.is_authenticated = True
        #     Authenticate = True
        #     flash('Successful login!')

        Check = False
        for user1 in Creds :
            if (user1.password == password):
                Check = True
                Auth_User = User.query.filter(User.user_id == user1.user_id).first()
                Cred = user1

        print("User found: ", Cred.email_id, Cred.password)
        print("Check Password : ",Cred.password, password, (Cred.password == password))

        if Check and Cred and (Cred.password == password):
            login_user(Auth_User)
            Auth_User.is_authenticated = True
            print("Authenticated")
            Authenticate = True
            flash('Successful login!')

    if Authenticate == True :
        return redirect('/Home')
    else :
        return render_template('Login.html')

@app.route('/AddToCart/<ProductID>/<MealID>', methods = ['GET', 'POST'])
def AddToCart(ProductID, MealID):
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

    print("ProductID: ", ProductID)
    print("MealID: ", MealID)
    if int(MealID) == -1 :
        return redirect('/Home')
    else :
        return redirect('/AddMissingProduct/' + str(MealID))

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
        Product_obj = Product.query.filter(Product.product_id == entry.product_id).first()
        cart_product_obj = [Product_obj.product_id, Product_obj.name, Product_obj.price]
        Cart_Product_Names.append(cart_product_obj)

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
    Cart_Products = Cart.query.filter(Cart.user_id == uid).all()
    Cart_Product_Ids = []
    for product in Cart_Products:
        Cart_Product_Ids.append(product.product_id)

    Obj_To_ML_Algo = {}
    Obj_To_ML_Algo['CustomerID'] = uid
    Obj_To_ML_Algo['ProductID'] = list(Cart_Product_Ids)

    print Obj_To_ML_Algo

    # Call ML Algo with above object and get list of product IDs user will most likely to buy next.

    Next_To_Buy_Ids = [3,6,7,14,16,34,58,76,98,374]
    print("Current Cart :", Cart_Product_Ids)
    print("Next to buy: ", Next_To_Buy_Ids)

    # Product list will contain product Ids in priority : 1. Common in cart and next to buy 2. Only in Cart 3. Only in Next to buy
    Products_List = []
    marked_indices = []

    ## Add Common Ids in both lists as per order in Next to buy list
    for i in range(len(Next_To_Buy_Ids)):
        if Next_To_Buy_Ids[i] in Cart_Product_Ids :
            Products_List.append(Next_To_Buy_Ids[i])
            marked_indices.append(i)
            Cart_Product_Ids.remove(Next_To_Buy_Ids[i])

    ## Add remaining productIds from cart list
    Products_List.extend(Cart_Product_Ids)

    ## Add remaining products from Next to but list
    for i in range(len(Next_To_Buy_Ids)):
        if i not in marked_indices:
            Products_List.append(Next_To_Buy_Ids[i])

    print("Combined list : ", Products_List)

    ## Intersection query to get most suitable meals from above list of products

    Filter_Meals1 = Meal.query.filter(Meal.product_id == Products_List[0]).all()
    print("Filter_Meals1 0 : ", Filter_Meals1)

    index = 1
    while len(Filter_Meals1)==0 and index<len(Products_List):
        Filter_Meals1 = Meal.query.filter(Meal.product_id == Products_List[index]).all()
        print("Filter_Meals1 " + str(index) +": ", Filter_Meals1)
        index += 1

    Filter_meals = []
    for meal in Filter_Meals1:
        Filter_meals.append(meal.meal_id)
    print("Filter_meals first : ", Filter_meals)

    while len(Filter_meals)>5 and index<len(Products_List):
        Subquery1 = Meal.query.filter(Meal.product_id == Products_List[index]).all()
        Subquery1_results = []
        for meal in Subquery1:
            Subquery1_results.append(meal.meal_id)
        Filter_meals = Filter_meals.intersect(Subquery1)
        index += 1

    print("Filter meals final : ", Filter_meals)
    ## Get Meal names from mealdetail table from above meal ids (top 5)
    Meal_List = []
    for mealID in Filter_meals:
        meal = MealDetails.query.filter(MealDetails.meal_id == mealID).first()
        Meal_List.append([mealID, meal.name])

    print("Meal_List sent : ",  Meal_List)
    return render_template('MealRecommendation.html', MealList=Meal_List)

@app.route('/AddMissingProduct/<MealID>', methods = ['GET', 'POST'])
def AddMissingProduct(MealID):
    # 1. Get current User's ID to get products in particular user's cart.
    # 2. Get all products in cart from cart table using above user ID.
    # 3. Get MealID as paramter.
    # 4. DB query to get missing productIDs using above MealID and List of Cart ProductIDs.
    # 5. DB Query to get corresponding Product Names from Product Detail table. [ProductID, Name as key:val pair if required]
    # 4. render HomePage page with parameter value = above queried list.
    MealID = int(MealID)

    uid = current_user.get_id()
    Cart_Products = Cart.query.filter(Cart.user_id == uid).all()
    Cart_Product_Ids = []
    for product in Cart_Products:
        Cart_Product_Ids.append(product.product_id)

    Meal_Products = Meal.query.filter(Meal.meal_id == MealID).all()
    Meal_Product_Ids = []
    for product in Meal_Products:
        Meal_Product_Ids.append(product.product_id)

    Missing_products = []

    ## Implementation 1
    # Common_products = Cart_Product_Ids.intersect(Meal_Product_Ids)
    # Missing_products_Ids = Meal_Product_Ids.remove(Common_products)
    #
    # for missing_product_id in Missing_products_Ids:
    #     Missing_product = Product.query.filter(Product.product_id==missing_product_id).first()
    #     Missing_products.append(Missing_product.name)

    ## Implementation 2
    for meal_product in Meal_Product_Ids :
        if meal_product not in Cart_Product_Ids:
            Missing_product = Product.query.filter(Product.product_id==meal_product).first()
            Missing_products.append([Missing_product.product_id, Missing_product.name, Missing_product.price])

    return render_template('HomePage.html', ProductList=Missing_products, Cart_Products=Cart_Product_Ids, Heading="Missing Products", Current_meal = MealID)

@app.route('/logout', methods = ['GET', 'POST'])
def logout_Dummy():
    user = current_user
    user.is_authenticated = False
    logout_user()
    return render_template('firstpage.html', message = "Logged out successfully")

def Encrypt_Password():
    Users = Credentials.query.all()
    for user in Users :
        user_password = user.password
        pw_hash = generate_password_hash(user_password)
        NewUser = Credentials(user_id = user.user_id, email_id = user.email_id, password = pw_hash)
        db.session.delete(user)
        db.session.add(NewUser)
        db.session.commit()


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
