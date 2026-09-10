import os
import random
import sqlite3

from dotenv import load_dotenv
from flask import Flask, render_template, request, session

VALID_CUISINES = ("mexican", "italian", "american", "asian", "bakery", "pizza")
DATABASE = "dinnerfinder.db"
HOMEPAGE = "index.html"
RECOMMENDATION = "recommendation.html"

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["FLASK_SECRET_KEY"]


def get_restaurant_recommendation(selected_cuisine: str) -> list:
    con = sqlite3.connect(DATABASE)
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
