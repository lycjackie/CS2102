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

    'Check if logged in'
    if session.get('logged_in') is None:
        return redirect('/login')

    origin = ""
    destination = ""
    if request.args.get('origin') is not None:
		origin = request.args.get('origin')
    if request.args.get('destination') is not None:
		destination = request.args.get('destination')
    list = ride.searchRides(origin, destination)
    print list

    return render_template('index.html', email = session.get('logged_in')['email'], rides = list, origin = origin, destination = destination);

@app.route('/login')
def renderLogin():
    return render_template('login.html');

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    u = user.retrieveUser({'email': email})
    if u.length > 0:
        session['logged_in'] = {
            'email': u[0]
        }
        return redirect('/')
    else:
        return redirect('/login?invalid=true')

@app.route('/signup')
def renderSignup():
    return render_template('signup.html');

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    firstName = request.form['firstname']
    lastName = request.form['lastname']
    contact = request.form['contact']
    u = user.addUser({
        'email': email,
        'firstName': firstName,
        'lastName': lastName,
        'contact': contact
    })
    if u:
        return redirect('/login')
    else:
        return redirect('/signup?invalid=true')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/login')

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
    nric = request.args.get('email')
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
