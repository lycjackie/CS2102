#!/usr/bin/python
from flask import Flask, render_template, redirect, request, session

import psycopg2
import datetime as dt
import importlib
import random
import urlparse

app = Flask(__name__, template_folder='templates')
app.secret_key = "super secret key"
ride = importlib.import_module("data.rides")
user = importlib.import_module("data.users")

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
    origin = ""
    destination = ""
    if request.args.get('origin') is not None:
		origin = request.args.get('origin')
    if request.args.get('destination') is not None:
		destination = request.args.get('destination')
    list = ride.searchRides(origin, destination)
    print list

    return render_template('index.html', rides = list, origin = origin, destination = destination);

@app.route('/updateRide')
def renderUpdateRide():
    rideId = request.args.get('rideid')
    if rideId is None:
        return redirect('/')
    else:
        try:
            rideId = int(rideId)
            user = ride.retrieveRide(rideId)
            return render_template('updateRide.html', user=user);
        except ValueError:
            return redirect('/')


@app.route("/updateRide", methods=['POST'])
def updateRide():
    newOrigin = request.form['newOrigin']
    newDestination = request.form['newDestination']
    rideId = request.args.get('rideid')
    ride.updateRide(rideId, newOrigin, newDestination)
    if rideId is None:
        return redirect('/')
    else:
        user = ride.retrieveRide(rideId)
        return redirect('/')


@app.route('/addRide')
def renderAddRide():
    nric = request.args.get('nric')
    if nric is None:
        return redirect('/')
    else:
        try:
            nric = int(nric)
            #users = user.retrieveUser(nric)
            return render_template('addRide.html', user={'nric':'123456', 'Name':'jackie'});
        except ValueError:
            return redirect('/')


@app.route("/addRide", methods=['POST'])
def addRide():
	origin = request.form['origin']
	destination = request.form['destination']
	rideDateTime = request.form['rideDateTime']
	rideEndTime = request.form['rideEndTime']
	status = request.form['status']
	nric = request.args.get('nric')

	new_ride = { 'Driver': nric, 'RideDateTime':dt.date(2018,9,19), 'RideEndTime':dt.time(14,00),
				 'Origin': origin, 'Destination' : destination, 'Status' : status}
	ride.addRide(new_ride)

	if nric is None:
		return redirect('/addRide')
	else:
		user = ride.retrieveAllRide();
        return redirect('/')

@app.route("/searchRides", methods=['POST'])
def searchRides():
    origin = request.form['origin']
    destination = request.form['destination']

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
