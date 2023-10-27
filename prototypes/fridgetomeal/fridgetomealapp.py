from flask import Flask, render_template, request, redirect, url_for, session, flash
from bs4 import BeautifulSoup #Scraper if we choose to use it
import requests
import json

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Load user credentials from the database
def load_users():
    try:
        with open("database/users.json", "r") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}
    return users

# Save user credentials to the database
def save_users(users):
    with open("database/users.json", "w") as file:
        json.dump(users, file)

# Check if a user is logged in
def is_logged_in():
    return "user" in session

# Fetch recipes based on user input ingredients (web scraping)
def get_recipes(ingredients):
    # Web scraping logic here (replace with your own)
    # You can use libraries like Beautiful Soup or Scrapy
    # to scrape recipe websites.

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    if is_logged_in():
        ingredients = request.form.get("ingredients")
        recipes = get_recipes(ingredients)
        return render_template("index.html", recipes=recipes)
    else:
        flash("You need to be logged in to search for recipes.")
        return redirect(url_for("index"))

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    users = load_users()

    if username in users and users[username] == password:
        session["user"] = username
        flash("Logged in successfully!")
    else:
        flash("Invalid credentials.")

    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully!")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
