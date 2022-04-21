import os
import hashlib

import sqlite3
from flask import Flask, render_template, session, request,redirect,url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

import helper


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_db():
    #create database connection to blog.db
    db_conn = sqlite3.connect("blog.db", detect_types=sqlite3.PARSE_DECLTYPES)
    #create row dictionary for select results
    db_conn.row_factory = sqlite3.Row

    return db_conn, db_conn.cursor()

@app.route("/")
def index():
    _, db_cursor = get_db()
    recent_posts = db_cursor.execute("SELECT * FROM post ORDER BY time_created DESC LIMIT 3").fetchall()
    # only show the post before the first newline
    recent_posts = helper.convert_markdown_posts(recent_posts, summarize=True)

    return render_template("index.html", posts=recent_posts)

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/blog")
def blog():
    return render_template("blog.html")

# list all recipes in Recipes category
@app.route("/recipes")
def recipes():
    _, db_cursor = get_db()
    categories = db_cursor.execute("SELECT name FROM category WHERE name <> 'Recipes'").fetchall()
    posts = db_cursor.execute("SELECT * FROM post p JOIN post_category pc ON pc.url_slug = p.url_slug WHERE pc.category_name = 'Recipes'")
    posts = helper.convert_markdown_posts(posts)

    return render_template("recipes.html", category=None, posts=posts, categories=categories)

# view a specific category
@app.route("/recipes/<category>")
def view_category(category):
    _, db_cursor = get_db()
    categories = db_cursor.execute("SELECT name FROM category WHERE name <> 'Recipes'").fetchall()
    posts = db_cursor.execute("SELECT * FROM post p JOIN post_category pc ON pc.url_slug = p.url_slug WHERE pc.category_name = ?", [category])
    posts = helper.convert_markdown_posts(posts)
    return render_template("recipes.html", category=category, posts=posts, categories=categories)


# view single post route
@app.route("/posts/<slug>")
def view_post(slug):
    _, db_cursor = get_db()
    post = db_cursor.execute("SELECT * FROM post WHERE url_slug = ?", [slug]).fetchone()
    post = helper.convert_markdown_posts([post])
    return render_template("post.html", post=post[0])


# login user and password
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # covert user input password into hash password using hashlib
        # save the user input username by using request.form
        password_hash = hashlib.sha256(request.form["password"].encode()).hexdigest()
        username = request.form["username"]
        # check if input user and password match in database
        _, db_cursor = get_db()
        user = db_cursor.execute("SELECT username FROM user WHERE username = ? AND password_hash = ?", [username, password_hash]).fetchone()
        if user:
            # using session to store user's login stat
            session["user"] = username
            # after logged in redirect to index page
            return redirect(url_for("create_post"))
        else:
            return "Incorrect user or password"
    else:
        return render_template("login.html")

# creating post
@app.route("/create-post", methods=["GET", "POST"])
def create_post():
    # check if user is logged in to post
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form["title"]
        url_slug = helper.convert_title_to_url(title)
        author = session["user"]
        categories = request.form.getlist("categories")
        body = request.form["post_body"]
        # put created post into database
        db_conn, db_cursor = get_db()
        db_cursor.execute("INSERT INTO post (title, url_slug, author, body) VALUES (?, ?, ?, ?)", [title, url_slug, author, body])
        # associate mulpti categories with post
        values = [(c, url_slug) for c in categories]
        db_cursor.executemany("INSERT INTO post_category (category_name, url_slug) VALUES (?,?)", values)
        db_conn.commit()
        return redirect(url_for("view_post", slug=url_slug))
    else:
        _, db_cursor = get_db()
        categories = db_cursor.execute("SELECT name FROM category").fetchall()
        return render_template("create_post.html", categories=categories)

