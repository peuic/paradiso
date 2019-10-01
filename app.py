import json
import re

import requests
from bson.json_util import dumps
from flask import Flask, redirect, render_template, request, url_for
from pymongo import MongoClient

uri = "mongodb://heroku_g1rjwwrr:1849hspa91t3u2vughfr3ql0kk@ds019668.mlab.com:19668/heroku_g1rjwwrr"
client = MongoClient(
    uri,
    connectTimeoutMS=30000,
    socketTimeoutMS=None,
    socketKeepAlive=True,
    retryWrites=False,
)
db = client.get_default_database()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/added", methods=["POST"])
def add_movie():
    movie_name = request.form["movie"]
    parsed_query = movie_name.replace(" ", "+")
    url = f"http://www.omdbapi.com/?t={parsed_query}&apikey=PlzBanM3"
    response = requests.get(url)
    movie_object = response.json()

    if not movie_object.get("Error"):
        db.Movies.insert_one(movie_object)
        return render_template("added_movie.html", movie=movie_object)
    return render_template("not_found.html")


@app.route("/movie", methods=["POST"])
def search():
    movie_name = request.form["movie"]
    movie_regex = re.compile(f"{movie_name}(.*)", re.IGNORECASE)
    movie_search = db.Movies.find({"Title": movie_regex})
    movie_list = json.loads(dumps(movie_search))
    if not movie_list:
        return redirect(url_for("add_movie_fallback", name=movie_name))
    movie = movie_list[0]

    return render_template("movie.html", movie=movie)


@app.route("/added/<name>", methods=["GET"])
def add_movie_fallback(name):
    parsed_query = name.replace(" ", "+")
    url = f"http://www.omdbapi.com/?t={parsed_query}&apikey=6de38469"
    response = requests.get(url)
    movie_object = response.json()
    if not movie_object.get("Error"):
        db.Movies.insert_one(movie_object)
        return render_template("added_movie.html", movie=movie_object)
    return render_template("not_found.html")


if __name__ == "__main__":
    app.run_server()
