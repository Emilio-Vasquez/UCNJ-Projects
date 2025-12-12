from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from .dashboard import dashboard
from .db import query_test
from .feedback import handle_feedback
from .login import handle_login
from .register import handle_registration
import plotly.express as px
import pandas as pd

bp = Blueprint("main", __name__)

"""

This the routes.py script

this controlls the  'routes of our page'
this is the / dir of our website in a way

/dashboard -> when a browser requests this page it'll send a GET
request to www.(our.website.domain).com/dashboard

.com resolves to the dns server then from the dns server it'll resolve our ip address
then our ip address will recieve a GET request 

what we return (or give back) to the client is the render_template("page.html")
render_template is a flask/jinja2 compiler that renders the full template tree of our page

this allows us to have a consistent design while not copy and pasting pages multiple times.

GET request -> means data retriveal we request data from a server
POST request -> means data send we send data to the server

---------------------------------------------------------------------------------

@bp.route()
is the route controller of flask

it's main param is  ("(route)")

optional params are methods=("GET"...) which we can dictatee what methods this route should accept

"""


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        return dashboard()

    # Line chart: Price & Stock Amount over Days
    fig1 = px.line(df, x="Day", y=["Price", "Stock Amount"], title="Stock Over Price")

    # Pie chart: Sample feature distribution (matching stock theme)
    fig2 = px.pie(
        names=["Feature A", "Feature B", "Feature C"],
        values=[50, 30, 20],
        title="Feature 1 vs Stock Amount",
    )

    # Bar chart: Sentiment over stock amounts
    fig3 = px.bar(
        x=["Good", "Neutral", "Bad"],
        y=[60, 25, 15],
        title="Sentiment over Stock Amount",
    )
    # Convert plots to HTML
    graph1 = fig1.to_html(full_html=False)
    graph2 = fig2.to_html(full_html=False)
    graph3 = fig3.to_html(full_html=False)

    return render_template(
        "dashboard.html",
        active="dashboard",
        graph1=graph1,
        graph2=graph2,
        graph3=graph3,
    )


@bp.route("/login", methods=["GET", "POST"])  ## local host / login
def login():
    if request.method == "POST":
        return handle_login()  # the backend for the /login reciever is in app/login.py
    return render_template("login.html", active="login")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        handle_registration()  # the backend for the /register POST event is in app/register.py
    return render_template("register.html", active="login")


@bp.route("/about")
def about():
    return render_template("about.html", active="about")


@bp.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        feedback = request.form.get("message")

        return jsonify(success=handle_feedback(name, email, feedback))
    return render_template("feedback.html", active="feedback")
