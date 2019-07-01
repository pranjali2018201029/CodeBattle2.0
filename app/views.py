# This is Main Controller of the webapp

from flask import Flask
from flask import render_template, url_for, redirect, request, make_response
import sqlalchemy

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_

# Use SQLAlchemy for SQLite queries, install and import packages here as and when required.

## VIEW 1 ROUTE
@app.route('/')
def firstpage():
    return render_template('FirstPage.html',title='First Page')

## VIEW 2 ROUTE
@app.route('/Register', methods = ['GET', 'POST'])
def Register():
    # Use post method as User Info should not be passed through URL.
    # 1. Get Form content (User info) by POST method.
    # 2. Encrypt Password and Add entry in Credentials table with EmailID and encrypted password.
    # 3. Add entry in User table with user info.
    # 4. Commit database changes.
    # 5. render Login page if successfully registered else display error message.
    return render_template('Login.html')

## VIEW 3 ROUTE
@app.route('/Login', methods = ['GET', 'POST'])
def Login():
    # Use post method as User credentials should not be passed through URL.
    # 1. Get Form content (User credentials) by POST method.
    # 2. Authenticate user from database. Do below steps if authenticated else show error msg.
    # 3. Database query to get all products from Products table. [ProductID, Name as key:val pair if required]
    # 4. render HomePage page with parameter value = above queried list.
    return render_template('HomePage.html', ProductList=[])

@app.route('/AddToCart/<ProductID>', methods = ['GET', 'POST'])
def AddToCart(ProductID):
    # 1. Get current User's ID to add product in particular user's cart.
    # 2. Get ProductID as a parameter.
    # 3. Add new entry in Cart table with above UserID and ProductID.
    # 4. Commit database after above entry.
    # 5. return some boolean value which will be used in HomePage view to decide whether enable or disable "Add to Cart" button.
    # 6. You can check other alternative OR refer add to favorites functionality in sample Gaana app.
    return AddedToCart

@app.route('/ViewCart', methods = ['GET', 'POST'])
def ViewCart():
    # 1. Get current User's ID to display products in particular user's cart.
    # 2. Get all products in cart from cart table using above user ID.
    # 3. Get corresponding product names from product detail table.
    # 4. render CartDetailPage with parameter = List of product names in cart.
    # 5. You can pass ProductID list along with is as list of key:value pair if ids are also required.
    return render_template('CartDetailPage.html', CartList=[])

@app.route('/ViewRecommendation', methods = ['GET', 'POST'])
def ViewRecommendation():
    # 1. Get current User's ID to display products in particular user's cart.
    # 2. Get all products in cart from cart table using above user ID.
    # 3. Send above UserID and list of cart productIDs in appropriate format to Tensoflow-serving which is serving Meal Recommendation ML model.
    # 4. Get response from TF-Serving : List of ProductIDs user id most likely to buy next.
    # 5. Database query to find most suitable MealIDs from above two lists : cartlist and predicted list. [Top 5 meals]
    # 6. Render MealRecommendation page with List of Meal names as parameter (MealIDs can be passed if required as key:val pairs).
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
