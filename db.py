import sqlite3
from datetime import datetime

import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def create_restaurant(name, cuisine, user_id):
    db = get_db()
    db.execute(
        "INSERT INTO restaurants (name, cuisine, user_id) VALUES (?, ?, ?)",
        (name, cuisine, user_id)
    )
    db.commit()

def get_restaurant_recommendation(selected_cuisine: str, user_id: int) -> list:
    db = get_db()
    res = db.execute(
        "SELECT name FROM restaurants WHERE cuisine=? AND user_id=?",
        (selected_cuisine,user_id)
    )
    restaurants = res.fetchall()
    restaurant_list = []
    for restaurant in restaurants:
        restaurant_list.append(restaurant[0])
    return restaurant_list

def get_restaurant_table(user_id: int):
    db = get_db()
    query_data = db.execute(
        "SELECT id, name, cuisine FROM restaurants WHERE user_id=?",
        (user_id,)
    )

    return query_data.fetchall()

def update_restaurant_name(old_name, new_name, user_id):
    db = get_db()
    db.execute(
        "UPDATE restaurants SET name=? WHERE name=? AND user_id=?",
        (new_name, old_name, user_id)
    )
    db.commit()

def update_restaurant_cuisine(name, new_cuisine, user_id):
    db = get_db()
    db.execute(
        "UPDATE restaurants SET cuisine=? WHERE name=? AND user_id=?",
        (new_cuisine, name, user_id)
    )
    db.commit()

def delete_restaurant(name, user_id, restaurant_id):
    db = get_db()
    db.execute(
        "DELETE FROM restaurants WHERE name=? AND user_id=? AND id=?",
        (name, user_id, restaurant_id)
    )
    db.commit()

def create_user(username, email, password_hash):
    db = get_db()
    db.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        (username, email, password_hash)
    )
    db.commit()

def get_user_id(username, password_hash):
    db = get_db()
    result = db.execute(
        "SELECT id FROM users WHERE username=? AND password_hash=?",
        (username, password_hash)
    )
    user = result.fetchone()
    return user["id"]

def update_user_name(id, username):
    db = get_db()
    db.execute(
        "UPDATE users SET username=? WHERE id=?",
        (username, id)
    )
    db.commit()

def update_user_email(id, email):
    db = get_db()
    db.execute(
        "UPDATE users SET email=? WHERE id=?",
        (email, id)
    )
    db.commit()

def update_user_password_hash(id, password_hash):
    db = get_db()
    db.execute(
        "UPDATE users SET password_hash=? WHERE id=?",
        (password_hash, id)
    )
    db.commit()

def delete_user(id):
    db = get_db()
    db.execute(
        "DELETE FROM users WHERE id=?",
        (id,)
    )
    db.commit()