#!/usr/bin/python
from flask import Flask, render_template
import psycopg2
import datetime as dt
import importlib
import random

app = Flask(__name__, template_folder='templates')
ride = importlib.import_module("data.rides")

origin = ["Toa Payoh", "NUS", "Woodlands", "Somewhere", "Orchard", "Sentosa"]
destination = ["Punggol", "Buona Vista", "Paya Lebar", "Over There", "Ghim Moh", "Yew Tee"]
currentDT = dt.datetime.now()

test_driver = {
	    'Driver':'123456',
        'RideDateTime': dt.date(currentDT.year,currentDT.month,currentDT.day),
        'RideEndTime': dt.time(currentDT.hour,currentDT.minute),
        'Origin': str(origin[random.randint(0,5)]),
        'Destination': str(destination[random.randint(0,5)]),
        'Status': 'NOT_YET_GONE'
    }

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
    ride.addRide(test_driver);	
    list = ride.retrieveAllRide();
    return render_template('index.html', users = list);

if __name__ == '__main__':
    app.run(debug=True)
