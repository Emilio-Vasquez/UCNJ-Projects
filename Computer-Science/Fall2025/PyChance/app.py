from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "replace_me_with_a_random_secret_key"


# Make sure every user has a wallet balance in session
@app.before_request
def ensure_wallet():
    if "balance" not in session:
        session["balance"] = 0.0


@app.route("/")
def home():
    return render_template("homepage.html")


@app.route("/games")
def games():
    return render_template("games.html")


@app.route("/coinflip")
def coinflip():
    return render_template("coinflip.html")


@app.route("/play_coinflip", methods=["POST"])
def play_coinflip():
    choice = request.form.get("choice")  # "heads" or "tails"
    result = random.choice(["heads", "tails"])
    win = (choice == result)
    return {"result": result, "win": win}


@app.route("/roulette")
def roulette():
    return render_template("roulette.html")


@app.route("/slot")
def slot():
    return render_template("slot.html")


# ---------- NEW PAGES BELOW ----------

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/help")
def help_page():
    return render_template("help.html")


@app.route("/contact")
def contact():
    # you can change this email to your real one
    support_email = "support@pychancecasino.com"
    return render_template("contact.html", support_email=support_email)


@app.route("/wallet", methods=["GET", "POST"])
def wallet():
    balance = session.get("balance", 0.0)
    error = None

    if request.method == "POST":
        amount_str = request.form.get("amount", "0")
        try:
            amount = float(amount_str)
        except ValueError:
            amount = 0

        if amount <= 0:
            error = "Please enter a positive amount."
        else:
            balance += amount
            session["balance"] = balance

        # Re-render the page with updated balance and any error
        return render_template("wallet.html", balance=balance, error=error)

    # GET request
    return render_template("wallet.html", balance=balance, error=error)

@app.route("/cashout", methods=["POST"])
def cashout():
    balance = session.get("balance", 0.0)
    error = None

    amount_str = request.form.get("amount", "0")

    try:
        amount = float(amount_str)
    except ValueError:
        amount = 0

    if amount <= 0:
        error = "Please enter a positive withdrawal amount."
    elif amount > balance:
        error = "You don't have enough funds to cash out."
    else:
        balance -= amount
        session["balance"] = balance

    return render_template("wallet.html", balance=balance, error=error)
# Make balance available in all templates (for navbar, etc.)
@app.context_processor
def inject_balance():
    return {"current_balance": session.get("balance", 0.0)}
