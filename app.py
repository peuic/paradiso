import json
import re
from flask import Flask, request, render_template, request, url_for
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')
  
@app.route('/greet')
def say_hello():
  return "Hello me, it's me again!"

@app.route('/movie', methods=['POST'])
def search():
	movie_name = request.form['movie']
	selected_movie = ""

	with open('movies.json', 'r') as data:
		data = data.read()
		movie_list = json.loads(data)
		for movie in movie_list:
			if re.search(movie_name, movie['Title'], re.IGNORECASE):
				selected_movie = movie

	if not selected_movie:
		return render_template('not_found.html')

	return render_template('movie.html', movie=selected_movie)