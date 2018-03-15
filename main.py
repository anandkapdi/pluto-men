# This Python file uses the following encoding: utf-8
from flask import Flask
from flask import render_template


app = Flask(__name__)
app.config.from_object('config')
app.debug = True


@app.route('/')
def index():
    return 'Hello World'


@app.route('/add_employees/', methods=['GET', 'POST', 'DELETE'])
def add_employees():
    return render_template('add_employees.html')
