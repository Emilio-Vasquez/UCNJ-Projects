"""
Contains routes/path for application
"""

from flask import Blueprint, render_template, request, url_for, redirect
from .login import handle_login
from .register import handle_registration
import pickle
import pandas as pd
import os
import sys
import base64
from io import BytesIO
from flask import Flask
from matplotlib.figure import Figure


bp = Blueprint("main", __name__)

#Loading CSV file into file
current_folder = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_folder, 'Model_Training (3).csv')
try:
    df = pd.read_csv(csv_path)
    print(f"Successfully loaded CSV from: {csv_path}")
except FileNotFoundError:
    print(f"ERROR: Could not find the CSV file at: {csv_path}")
    df = pd.DataFrame()

#Loading KNN Model into file
current_folder = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_folder)
file_path = os.path.join(current_folder, 'house_price_model.pkl')
try:
    with open(file_path, 'rb') as file:
        loaded_data = pickle.load(file)

    my_knn_model = loaded_data[0]
    my_scaler = loaded_data[1]
    model_columns = loaded_data[2]
    print(f"Successfully loaded model from: {file_path}")
except FileNotFoundError:
    print(f"ERROR: Could not find file at: {file_path}")
except ModuleNotFoundError as e:
    print(f"Pickle Error: {e}")

# Redirect to login page when accessing root URL
@bp.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for('main.login'))

#Home page that takes input
@bp.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            print("trying to predict...")
            beds = int(request.form['beds'])
            full_baths = int(request.form['full_baths'])
            half_baths = int(request.form['half_baths'])
            garage = int(request.form['garage'])
            year = int(request.form['year'])
            acres = float(request.form['acres'])
            town_id = request.form['town']  # Town_id is numbers

            #KNN put to use
            input_df = pd.DataFrame({
                'Beds': [beds],
                'GarageCap': [garage],
                'YearBuilt': [year],
                'Acres': [acres],
                'FullBaths': [full_baths],
                'HalfBaths': [half_baths],
                'Town': [town_id]
            })

            input_df = pd.get_dummies(input_df, columns=['Town']) #Make Town KNN friendly
            input_df = input_df.reindex(columns=model_columns, fill_value=0) #Reorders column to be KNN friendly
            input_scaled = my_scaler.transform(input_df) #Scale features to be in proportion KNN friendly
            pred_price = my_knn_model.prediction(input_scaled) #Predict
            pred = pred_price[0]
            pred = round(pred)
            prediction_text = f"Estimated Price: ${pred:,.2f}"

            #Map townsID to town
            town_mapping = {
                '2901': 'Berkeley Heights',
                '2902': 'Clark',
                '2903': 'Cranford',
                '2904': 'Elizabeth',
                '2905': 'Fanwood',
                '2906': 'Garwood',
                '2907': 'Hillside',
                '2908': 'Kenilworth',
                '2909': 'Linden',
                '2910': 'Mountainside',
                '2911': 'New Providence',
                '2912': 'Plainfield',
                '2913': 'Rahway',
                '2914': 'Roselle',
                '2915': 'Roselle Park',
                '2916': 'Scotch Plains',
                '2917': 'Springfield',
                '2918': 'Summit',
                '2919': 'Union',
                '2920': 'Westfield',
                '2921': 'Winfield'
            }

            #Find town's pricing, and get save median
            town_prices = df[df['Town'] == int(town_id)]['SalesPrice']
            town_price = town_prices.mean()
            town_price = round(town_price)

            #Town ID to Town Name
            town_name = town_mapping[town_id]

            #Plot 1: Price comparison user house vs loca/regional, bar graph
            fig = Figure(figsize=(10, 8))
            (ax1,ax2) = fig.subplots(2,1)
            ax1_towns = ["Estimated Home", f"{town_name} Med", "Union County (NJ) Med", "New Jersey Med", "United States Med"]
            ax1_prices = [pred,town_price,596825, 543000, 368300]
            ax1.bar(ax1_towns, ax1_prices)
            ax1.set_ylabel("Median Sales Price")
            ax1.set_title('Comparison of Housing: Local & Regional Medians')
            ax1.grid()

            #Plot 2: Summary of town's pricing, boxplot
            ax2.boxplot(town_prices, vert = False, widths = 0.6)
            ax2.scatter(pred,[1], color='red', s=1000, marker='*', label='House Estimate')
            ax2.set_title(f"Price Distribution and Model Prediction (Red Star) for {town_name}")
            ax2.set_xlabel("In millions")
            ax2.set_yticks([])

            #Save plots #1 and #2 as png for html
            fig.tight_layout(pad=3.0)
            buf = BytesIO()
            fig.savefig(buf, format='png')
            data = base64.b64encode(buf.getbuffer()).decode('ascii')

            #Plot 3: Two tables to showcase user's house vs town median
            #Select houses from specific town
            town_data = df[df['Town'] == int(town_id)]

            #get median features of town's houses
            avg_Beds = round(town_data['Beds'].median())
            avg_FullBaths = round(town_data['FullBaths'].median())
            avg_HalfBaths = round(town_data['HalfBaths'].median())
            avg_GarageCap = round(town_data['GarageCap'].median())
            avg_Acres = round(town_data['Acres'].median(),2)
            avg_YearBuilt = round(town_data['YearBuilt'].median())

            #Dictionarys inside of list to make comparisons easier
            comparison_data = [
                {"feature": "Beds", "user": beds, "town": avg_Beds},
                {"feature": "Full Baths", "user": full_baths, "town": avg_FullBaths},
                {"feature": "Half Baths", "user": half_baths, "town": avg_HalfBaths},
                {"feature": "Garage Capacity", "user": garage, "town": avg_GarageCap},
                {"feature": "Year Built", "user": year, "town": avg_YearBuilt},
                {"feature": "Acres (lot size)", "user": acres, "town": avg_Acres},
                {"feature": "Sales Price", "user": pred, "town": town_price}
            ]

            #Add new key:value pair to each dictionary that holds percentage diff
            for row in comparison_data:
                if row['user'] == 0:
                    row['diff'] = "N/A"  # Cannot divide by zero
                elif row['town'] == 0:
                    row['diff'] = "N/A" #Cannot divide by zero
                elif row['feature'] == 'Year Built': #Percentage diff in years not reasonable
                    row['diff'] = "N/A"
                else:
                    # Formula: (User - Town) / Town to calculate percentage diff
                    pct = ((row['user'] - row['town']) / row['town']) * 100
                    row['diff'] = f"{pct:+.1f}%"  # Formats as "+5.0%" or "-5.0%"

            #  Passing 'prediction_text' to the HTML file to display in web
            return render_template('output.html', prediction_text=prediction_text,
                                   data = data, comparison_table=comparison_data, town = town_name)

        except ValueError:
            return "Error: Please enter valid numbers."

    return render_template("index.html")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        result = handle_login()
        if result:  
            return result
    
    return render_template("login.html")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        result = handle_registration()
        if result:  
            return result
    
    return render_template("register.html")

@bp.route("/about")
def about():
    return render_template("about.html")

@bp.route("/feedback") 
def feedback():
    return render_template("feedback.html")
