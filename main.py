# This Python file uses the following encoding: utf-8
from flask import Flask


app = Flask(__name__)
app.config.from_object('config')
app.debug = True


@app.route('/')
def index():
    return 'Hello World'