from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for,jsonify, flash, session
import os, sys
from functools import wraps
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(ROOT)

from app.config import DATA_DIR
from app.modules.database.db import get_all_feedback

from app.calcs import LOAD_DATA
from app.decorators.auth_decorator import anonymous_required, login_required
from app.modules.auth.auth import register_user, authenticate_user
from app.modules.database import db
from app.modules.predictor.predictor import predict_sale_price


app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")

ADMIN_USERNAME = "admin"

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("is_admin"):
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return wrapper


@app.route('/')
def hello_world():
	return redirect(url_for('login'))

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
	return render_template('home.html')

@app.route('/lookup', methods=['POST'])
def lookup():
	data = request.get_json()
	zip_code = data.get("zip_code")
	
	result = {
        "zip_code": zip_code,
        "message": f"Received ZIP code: {zip_code}"
		
    }
	print("zipcode: ",zip_code)
	print("result: ",result)
	return jsonify(result)


@app.route('/charts', methods=['GET'])
@login_required
def charts():
    import json
    data_path = Path(__file__).resolve().parent / "eda_chart_data.json"
    try:
        with data_path.open(encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return redirect(url_for('home'))
    return render_template('charts.html', chart_data=data)

@app.route('/login', methods=['GET', 'POST'])
@anonymous_required
def login():
	if request.method == 'POST':
		username = request.form.get('username', '').strip()
		password = request.form.get('password', '')

		if not username or not password:
			flash("Username and password are required")
			return redirect(url_for('login'))

		result = authenticate_user(username, password)
		if result.success:
			session['user_id'] = result.user_id
			session['username'] = username
			session["is_admin"] = (username == ADMIN_USERNAME)
			flash("Logged in successfully")
			return redirect(url_for('home'))

		flash(result.message)
		return redirect(url_for('login'))

	return render_template('login.html')


@app.route('/history', methods=['GET'])
@login_required 
def render_history():
    user_id = session.get("user_id")
    history_data = db.get_all_history(user_id)
    return render_template('history.html', history=history_data)

@app.route("/admin/feedback")
@admin_required
def admin_feedback():
    feedback_list = db.get_all_feedback()   
    return render_template("admin_feedback.html", feedback_list=feedback_list)
	



@app.route('/logout', methods=['POST', 'GET'])
def logout():
	session.clear()
	flash("You have been logged out")
	return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
@anonymous_required
def signup():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		confirm_password = request.form.get('confirm_password')
		if password != confirm_password:
			flash("Passwords do not match")
			return redirect(url_for('signup'))
		else:
			result = register_user(username, password)
			if not result.success:
				flash(result.message)
				return redirect(url_for('signup'))
			else:
				flash("User created successfully")
				return redirect(url_for('login'))
		
	return render_template('signup.html')


@app.route('/feedback_page')
@login_required
def feedback_page():
    return render_template("feedback.html")

@app.route('/feedback', methods=['POST'])
@login_required
def feedback():
    # Support both JSON and normal form submissions
    if request.is_json:
        data = request.get_json()
        content = data.get("content", "").strip()
    else:
        content = request.form.get("content", "").strip()

    user_id = session.get("user_id")

    if not user_id or not content:
        return jsonify({"error": "user_id and content are required"}), 400

    try:
        feedback_id = db.create_feedback(user_id=user_id, content=content)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    flash("Feedback submitted successfully!")
    return redirect(url_for("home"))
	
@app.route('/predictor', methods=['POST'])
@login_required
def predict():
	data = request.get_json()
	data_model = {
		'borough': data.get('borough'),
		'zip_code': int(data.get('zip_code')),
		'prop_type': data.get('prop_type'),
		'gross_sqft': float(data.get('gross_sqft')),
		'year_built': int(data.get('year_built')),
		'land_sqft': float(data.get('land_sqft', 0))
	}
	try:
		response = predict_sale_price(data_model)
		prediction_record = {
			**data_model,
			**response,
			"user_id": session.get("user_id")
		}
		db.register_prediction(prediction_record)
	except ValueError as e:
		print(e)
		return jsonify({"error": str(e)}), 400
	return jsonify(response)
	
if __name__ == "__main__":
    app.run(debug=True)
