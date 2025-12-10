"""
This is the routes.py script will contain the routes/path for our application
"""
from flask import Blueprint, render_template, request, session, redirect  ## Blueprint is a way to organize a group of related routes and other code. render_template is used to render html templates
from .db import query_test  ## import the query_test function from the db.py file
from .login import handle_login ## import the login functions from the login.py file
from .register import handle_registration ## import the register functions from the register.py file
from .feedback import handle_feedback # import feedback functions from feedback.py


bp = Blueprint("main", __name__)  ## create a blueprint object. 'main' is the name of the blueprint, __name__ is the name of the current module

@bp.route("/")  ## this is the route for the home page
def index():
    """
    this is the route for the home page
    """
    
    ok = query_test("SELECT 1")  ## test the database connection
    if ok:
        return render_template("index.html")
    else:
        return "<h1>Flask is running! Database test query returned no results!</h1>"
   
## add the route for the login

@bp.route("/login", methods=["GET", "POST"]) ## localhost/login
def login():
    """
    this is the route for the login page
    """
    if request.method == "POST":
       return handle_login(request)
    return render_template("login.html") ## handle the login form submission
    
@bp.route("/registration", methods=["GET", "POST"]) ## localhost/register
def registration():
    """
    this is the route for the registration page
    """
    if request.method == "POST":
       return handle_registration(request) # handle_registration is in register.py
    return render_template("registration.html") ## handle the registration form submission  

@bp.route("/feedback", methods=["GET", "POST"]) ## localhost/register
def feedback():
    if request.method == "POST":
        return handle_feedback(request)
    return render_template("feedback.html") ##

@bp.route("/menu", methods=["GET", "POST"]) ## localhost/register
def menu():
    if request.method == "POST":
        print("hi") # prevents error
    return render_template("menu.html") ##

@bp.route("/logout")
def logout():
    session.clear() ## clears the users data before redirecting
    return redirect("/")
