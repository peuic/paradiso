from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
  return 'What up!?'
  
@app.route('/greet')
def say_hello():
  return "Hello me, it's me again!"