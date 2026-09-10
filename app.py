import random
import sqlite3

from flask import Flask, redirect, render_template, request, url_for
from markupsafe import escape

VALID_CUISINES = ("mexican", "italian", "american", "asian", "bakery", "pizza")
DATABASE = "dinnerfinder.db"
HOMEPAGE = "index.html"
app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template(HOMEPAGE)


@app.route("/recommend", methods=["POST"])
def recommend():
    selected_cuisine = request.form["cuisine"].lower()
    if selected_cuisine not in VALID_CUISINES:
        print(f"Invalid Cuisine: {selected_cuisine}")
        return render_template(HOMEPAGE)
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    res = cur.execute(
        """
        SELECT name
        FROM restaurants
        WHERE cuisine='italian'
        """
    )
    restaurant_list = res.fetchall()
    print(f"Size of restaurant list: {len(restaurant_list)}")
    restaurant_tuple = random.choice(restaurant_list)
    restaurant_name = restaurant_tuple[0]
    return restaurant_name


# @app.route("/hello")
# @app.route("/hello/<name>")
# def hello(name=None):
#     return render_template('hello.html', person=name)

# @app.route('/user/<username>')
# def show_user_profile(username):
#     # show the user profile for that user
#     return f'User {escape (username)}'

# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     return f'Post {post_id}'

# @app.route('/path/<path:subpath>')
# def show_subpath(subpath):
#     # show the subpath after /path/
#     return f'Subpath {escape(subpath)}'

# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if valid_login(request.form['username'],
#             request.form['password']):
#             return log_the_user_in(request.form['username'])
#         else:
#             error = 'Invalid username/password'
#     return render_template('login.html', error=error)
