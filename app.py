import random
import sqlite3

from flask import Flask, render_template, request

VALID_CUISINES = ("mexican", "italian", "american", "asian", "bakery", "pizza")
DATABASE = "dinnerfinder.db"
HOMEPAGE = "index.html"
RECOMMENDATION = "recommendation.html"
app = Flask(__name__)


def get_restaurant_recommendation(selected_cuisine: str) -> str:
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    res = cur.execute(
        "SELECT name FROM restaurants WHERE cuisine=?",
        (selected_cuisine,),
    )
    restaurant_list = res.fetchall()
    con.close()
    print(f"Size of restaurant list: {len(restaurant_list)}")
    restaurant_tuple = random.choice(restaurant_list)
    return restaurant_tuple[0]


@app.route("/")
def hello_world():
    return render_template(HOMEPAGE)


@app.route("/recommend", methods=["POST"])
def recommend():
    selected_cuisine = request.form["cuisine"].lower()
    if selected_cuisine not in VALID_CUISINES:
        print(f"Invalid Cuisine: {selected_cuisine}")
        return render_template(HOMEPAGE)
    restaurant_name = get_restaurant_recommendation(selected_cuisine)
    return render_template(
        RECOMMENDATION, restaurant=restaurant_name, cuisine=selected_cuisine
    )


@app.route("/recommendation", methods=["POST"])
def recommendation():
    resp = request.form["recommendation"].lower()
    selected_cuisine = request.form["cuisine"].lower()
    if resp == "yes":
        return render_template(HOMEPAGE)
    elif resp == "no":
        restaurant_name = get_restaurant_recommendation(selected_cuisine)
        return render_template(
            RECOMMENDATION, restaurant=restaurant_name, cuisine=selected_cuisine
        )
    else:
        return render_template(HOMEPAGE)
