import os
import random
import sqlite3
import db

from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect

VALID_CUISINES = ("mexican", "italian", "american", "asian", "bakery", "pizza")
HOMEPAGE = "/index.html"
RECOMMENDATION = "recommendation.html"
USERS = "users.html"
RESTAURANTS = "restaurants.html"

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["FLASK_SECRET_KEY"]
app.config["DATABASE"] = os.path.join(app.root_path, "dinnerfinder.db")
db.init_app(app)

def get_restaurant_recommendation(selected_cuisine: str) -> list:
    con = sqlite3.connect(app.config["DATABASE"])
    cur = con.cursor()
    res = cur.execute(
        "SELECT name FROM restaurants WHERE cuisine=?",
        (selected_cuisine,),
    )
    restaurants = res.fetchall()
    con.close()
    restaurant_list = []
    for restaurant in restaurants:
        restaurant_list.append(restaurant[0])
    return restaurant_list


def pop_random_element_from_list(restaurants: list[str]) -> str:
    random_element = random.randint(0, len(restaurants) - 1)
    return restaurants.pop(random_element)


@app.route("/")
def hello_world():
    return render_template(HOMEPAGE)


@app.route("/recommend", methods=["POST"])
def recommend():
    selected_cuisine = request.form["cuisine"].lower()
    session["cuisine"] = selected_cuisine
    if selected_cuisine not in VALID_CUISINES:
        return render_template(HOMEPAGE)
    restaurants = get_restaurant_recommendation(selected_cuisine)
    restaurant = pop_random_element_from_list(restaurants)
    session["restaurants"] = restaurants
    return render_template(
        RECOMMENDATION, restaurant=restaurant, cuisine=selected_cuisine
    )


@app.route("/recommendation", methods=["POST"])
def recommendation():
    resp = request.form["recommendation"].lower()
    selected_cuisine = session["cuisine"].lower()
    if resp == "yes":
        return render_template(HOMEPAGE)
    elif resp == "no":
        restaurants = session["restaurants"]
        if not restaurants:
            print("Out of restaurants!")
            return render_template(HOMEPAGE)
        restaurant = pop_random_element_from_list(restaurants)
        session["restaurants"] = restaurants
        return render_template(
            RECOMMENDATION, restaurant=restaurant, cuisine=selected_cuisine
        )
    else:
        return render_template(HOMEPAGE)

@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "POST":
        resp = request.form["user_management"]
        if resp == "add_user":
            db.create_user("testuser4", "testuser4@test.com", "1234567")
            return redirect("/")
        if resp == "get_user_id":
            print(db.get_user_id("testuser4", "1234567"))
            return redirect("/")
        if resp == "update_user":
            db.update_user_email(1, "fake@fakerson.com")
            return redirect("/")
        if resp == "delete_user":
            db.delete_user(1)
            return redirect("/")

    if request.method == "GET":
        return render_template(USERS)

@app.route("/restaurants", methods=["GET", "POST"])
def restaurants():
    if request.method == "POST":
        resp = request.form["restaurant_management"]
        if resp == "add_restaurant":
            db.create_restaurant("test", "mexican", 1)
            return redirect("/")
        if resp == "update_restaurant":
            db.update_restaurant_cuisine("test", "american", 1)
            return redirect("/")
        if resp == "delete_restaurant":
            db.delete_restaurant("test", 1, 1)
            return redirect("/")

    if request.method == "GET":
        user_id = 1
        restaurant_table = db.get_restaurant_table(user_id)
        return render_template(RESTAURANTS, restaurant_table=restaurant_table)