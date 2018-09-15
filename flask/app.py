#!/usr/bin/python
from flask import Flask, render_template
import psycopg2
import importlib

app = Flask(__name__, template_folder='templates')
ride = importlib.import_module("data.rides")

@app.route('/')
def main():
    '''
    test_user = {
        'name':'jackie',
        'nric':'123456',
        'contact': 99112233,
        'role': 3
    }
    '''
    list = ride.retrieveAllRide();
    return render_template('index.html', users = list);

if __name__ == '__main__':
    app.run(debug=True)
