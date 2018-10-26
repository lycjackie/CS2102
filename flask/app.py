#!/usr/bin/python
from flask import Flask, render_template, redirect, request, session

import psycopg2
import datetime as dt
import importlib
import random
import urlparse
import simplejson as json
import decimal as Decimal

app = Flask(__name__, template_folder='templates')
app.secret_key = "super secret key"
ride = importlib.import_module("data.rides")
user = importlib.import_module("data.users")
car = importlib.import_module("data.cars")
model = importlib.import_module("data.models")
ride_bid = importlib.import_module("data.bid")


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
        return redirect('/login?invalid=true')

    origin = ""
    destination = ""
    if request.args.get('origin') is not None:
		origin = request.args.get('origin')
    if request.args.get('destination') is not None:
		destination = request.args.get('destination')
    list = ride.searchRides(origin, destination)
    print list

    return render_template('index.html', email=session.get('email'), rides=list, origin=origin, destination=destination)


@app.route('/login')
def renderLogin():
    return render_template('login.html', invalid=request.args.get('invalid'), credentialError=request.args.get('credentialError'))


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    u = user.retrieveUser({'email': email,'password': hash(password)})
    if len(u) > 0:
        session['logged_in'] = u
        session['email'] = email
        return redirect('/')
    else:
        return redirect('/login?invalid=true&credentialError=true')


@app.route('/signup')
def renderSignup():
    return render_template('signup.html', invalid=request.args.get('invalid'))


@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    firstName = request.form['firstname']
    lastName = request.form['lastname']
    contact = request.form['contact']
    password = request.form['password']
    u = user.addUser({
        'email': email,
        'firstName': firstName,
        'lastName': lastName,
        'contact': contact,
        'password': hash(password)
    })
    if u:
        return redirect('/login')
    else:
        return redirect('/signup?invalid=true')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/login')


@app.route('/updateUser')
def renderUpdateUser():
    if session.get('logged_in') is None:
        return redirect('/login')
    else:
        print session.get('logged_in')
        try:
            return render_template('updateUser.html', first_name=session.get('logged_in')[0][2], last_name=session.get('logged_in')[0][3])
        except ValueError:
            return redirect('/')


@app.route('/updateUser', methods=['POST'])
def updateUser():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = session.get('email')
    user.updateUser(email, first_name, last_name)
    u = user.retrieveUser({'email': email})
    if len(u) > 0:
        session['logged_in'] = u
        session['email'] = email
    if session.get('logged_in') is None:
		return redirect('/login')
    else:
        return redirect('/')

@app.route('/addRide')
def renderAddRide():
    if session.get('logged_in') is None:
        return redirect('/login')
    else:
        try:
			users = user.retrieveUser(session.get('email'))
			cars = car.retrieveCarsByEmail(session.get('email'))
			return render_template('addRide.html', users=users, cars=cars)
        except ValueError:
            return redirect('/')


@app.route("/addRide", methods=['POST'])
def addRide():
	origin = request.form['origin']
	destination = request.form['destination']
	rideDateTime = request.form['rideDateTime']
	car = request.form['car']
	pax = '0'
	status = request.form['status']

	ride_details = {'RideStartTime': rideDateTime, 'Status': status, 'Current_pax': pax,
				 'Origin': origin, 'Destination': destination, 'reg_no': car}
	ride.addRide(ride_details)

	if session.get('logged_in') is None:
		return redirect('/login')
	else:
		origin = ""
		destination = ""
		list = ride.searchRides(origin, destination)
        #return render_template('index.html', email=session.get('email'), rides=list, origin=origin, destination=destination)
        return redirect('/')

@app.route('/updateRide')
def renderUpdateRide():
	reg_no = request.args.get('regno')
	start_time = request.args.get('starttime')
	if reg_no is None:
		return redirect('/')
	else:
		try:
			ride_details = {'start_time': start_time, 'reg_no': reg_no}
			rides = ride.retrieveRide(ride_details)
			return render_template('updateRide.html', rides=rides)
		except ValueError:
			return redirect('/')


@app.route("/updateRide", methods=['POST'])
def updateRide():
	origin = request.form['origin']
	destination = request.form['destination']
	status = request.form['status']
	reg_no = request.args.get('regno')
	start_time = request.args.get('starttime')
	ride.updateRide(status, origin, destination, reg_no, start_time)
	if reg_no is None:
		return redirect('/')
	else:
		origin = ""
		destination = ""
		list = ride.searchRides(origin, destination)
		return render_template('index.html', email=session.get('email'), rides=list, origin=origin, destination=destination)


@app.route("/searchRides", methods=['POST'])
def searchRides():
    origin = request.form['origin']
    destination = request.form['destination']

    return redirect('/')


@app.route('/listCar')
def renderListCar():
    'Check if logged in'
    if session.get('logged_in') is None:
        return redirect('/login')
    else:
        cars = car.retrieveCarsByEmail(session.get('email'))
        return render_template('listCar.html', cars=cars)


@app.route('/addCar')
def renderAddCar():
    'Check if logged in'
    if session.get('logged_in') is None:
        return redirect('/login')
    else:
        models = model.retrieveAllModels()
        return render_template('addCar.html', models=models)


@app.route("/addCar", methods=['POST'])
def addCar():
    'Check if logged in'
    if session.get('logged_in') is None:
        return redirect('/login')
    else:
        reg_no = request.form['reg_no']
        make_model = request.form['make_model'].split('/')
        colour = request.form['colour']

        new_car = {'reg_no': reg_no,
            'make': make_model[0], 'model': make_model[1], 'colour': colour, 'email': session.get('email')}
        car.addCar(new_car)
        return redirect('/listCar')


@app.route('/updateCar')
def renderUpdateCar():
    'Check if logged in'
    reg_no = request.args.get('reg_no')
    if reg_no is None or car.carBelongsTo(reg_no, session.get('email')) is None:
        return redirect('/listCar')
    if session.get('logged_in') is None:
        return redirect('/login')
    else:
        update_car = car.retrieveCarByRegNo(reg_no)
        models = model.retrieveAllModelsForUpdate(reg_no)
        if update_car is None:
            return redirect('/listCar')
        else:
            return render_template('updateCar.html', car=update_car, models=models)


@app.route("/updateCar", methods=['POST'])
def updateCar():
    'Check if logged in'
    reg_no = request.args.get('reg_no')
    if reg_no is None or car.carBelongsTo(reg_no, session.get('email')) is None:
        return redirect('/')
    if session.get('logged_in') is None:
        return redirect('/login')
    else:
        colour = request.form['colour']
        make_model = request.form['make_model'].split('/')
        res = car.updateCarByRegNo(
            reg_no, make_model[0], make_model[1], colour)
        return redirect('/listCar')


'''
@app.route("/addBid")
def renderAddBid():
    if session.get('logged_in') is None:
        return redirect('/login')
    else:
        # if session.get('reg_no') is None and session.get('start_time') is None:
        #    return redirect('/') # by right should go back to list ride
        # else:
        # ride_detail = {
        #   'reg_no' : session.get('reg_no'),
        #   'start_time : dt.datetime.strptime(session.get('start_time'),'%Y-%m-%d %H:%M:%S')
        # }
        ride_detail = {
            'reg_no': 'SGX1337X',
	        'start_time': dt.datetime.combine(dt.date(2018, 9, 19), dt.time(14, 00))
        }

        rides = ride.retrieveRide(ride_detail)
        return render_template('addBid.html', ride=rides)

'''
'''
    retrieveRide(ride_detail)
	test_user = {
	    'reg_no':'SGX1337X',
	    'start_time': dt.datetime.combine(dt.date(2018,9,19),dt.time(14,00)),
	    'no_pax': 1,
	    'bid_price': 13.37,
		'email':'owerv@tamu.edu'
	}



@app.route("/addBid", methods=['POST'])
def addBid():
	if session.get('email') is None or session.get('logged_in') is None:
		return redirect('/login')
	else:
		price = request.form['price']
		# ride_detail = request.form['ride_detail'].split('/')
		no_pax = request.form['no_pax']
		start_time = dt.datetime.strptime(
		request.form['start_time'], '%Y-%m-%d %H:%M:%S')
		print start_time
		reg_no = request.form['reg_no']
		ride_details = {
		'reg_no': reg_no,
		'start_time': start_time,
		'no_pax': no_pax,
		'bid_price': price,
		'email': session.get('email')
		}
		try:
			print ride_details
			res = ride_bid.add_bid(ride_details)
			if res == 0:
				print 'test'
				rides = ride_bid.getSingleBid(session.get('email'),reg_no,start_time)
				return redirect('/bid',reg_no=reg_no,start_time=start_time)
			else:
				return redirect('/login')
		except Exception as error:
			print error
'''

@app.route('/listBid')
def renderListBid():
    if session.get('logged_in') is None or session.get('email') is None:
        return redirect('/login')
    else:
        rides = rides = ride_bid.get_bid(session.get('email'))
        print rides
        return render_template('listBid.html', rides=rides)


@app.route('/approve')
def renderApprovePage():
    try:
        reg_no = request.args.get('regno')
        start_time = dt.datetime.strptime(
            request.args.get('starttime'), '%Y-%m-%d %H:%M:%S')
        if reg_no is None:
            return redirect('/')
        else:
            try:
                bids = ride_bid.get_AllBidForSingleRide(reg_no, start_time)
                print bids
                return render_template('listBid.html', bids=bids)
            except ValueError:
                return redirect('/')
    except Exception:
        return redirect('/')


@app.route('/approveBid')
def renderApproveBid():
    reg_no = request.args.get('regno')
    start_time = dt.datetime.strptime(
        request.args.get('starttime'), '%Y-%m-%d %H:%M:%S')
    email = request.args.get('email')
    if reg_no is None:
        return redirect('/')
    else:
        try:
            bid = ride_bid.getSingleBid(email, reg_no, start_time)
            return render_template('approveBid.html', bid=bid)
        except ValueError:
            return redirect('/')


@app.route('/approveBid', methods=['POST'])
def approve_bid():
    if session.get('email') is None:
        return redirect('/login')
    else:
        try:
            bidder_email = request.form['bidder_email']
            reg_no = request.form['reg_no']
            start_time = dt.datetime.strptime(
                request.form['start_time'], '%Y-%m-%d %H:%M:%S')
            owner_email = session.get('email')
            status = request.form['status']
            bid = ride_bid.approve_bid(bidder_email.encode('utf8'), reg_no.encode(
                'utf8'), start_time, status.encode('utf8'), owner_email.encode('utf8'))
            # bid = ride_bid.approve_bid('a@a.com','SGX1337X',dt.datetime.strptime('2018-09-19 14:00:00','%Y-%m-%d %H:%M:%S'),'unsuccessful','wpicklessi@geocities.com')
            print bid
            if bid is not None:
                return redirect('/')
            else:
                bid = ride_bid.getSingleBid(bidder_email, reg_no, start_time)
                return redirect('/login')
        except ValueError:
            print "ERROR"
            return redirect('/')


@app.route('/bid')
def renderBidPage():
	reg_no = request.args.get('regno')
	start_time = request.args.get('starttime')
	if reg_no is None:
		return redirect('/')
	else:
		try:

			ride_details = {'start_time': start_time, 'reg_no': reg_no}
			email = session.get('email')
			checker = ride_bid.success_bid(email,reg_no,start_time)
			print checker
			if checker:
			    return render_template('addBid.html',invalid='1')
			rides = ride.retrieveRide(ride_details)
			return render_template('addBid.html', ride=rides)
		except ValueError:
			return redirect('/')


@app.route('/bid', methods=['POST'])
def add_user_bid():
    if session.get('email') is None:
        return redirect('/login')
    else:
        try:
            reg_no = request.form['reg_no']
            start_time = dt.datetime.strptime(
                request.form['start_time'], '%Y-%m-%d %H:%M:%S')
            no_pax = request.form['no_pax']
            price = request.form['price']
            ride_detail = {
                'reg_no': reg_no,
                'start_time': start_time,
                'no_pax': no_pax,
                'bid_price': price,
                'email': session.get('email')
            }
            res = ride_bid.add_bid(ride_detail)
            if res is None:
				print 'test'
				rides = ride.retrieveRide(ride_detail)
				return render_template('addBid.html',ride=rides,fail='1')
            else:
                return redirect('/')
        except Exception as e:
            print e
            return redirect('/')


@app.route('/updateBid')
def RenderUpdatePage():
    reg_no = request.args.get('regno')
    start_time = request.args.get('starttime')
    email = session.get('email')
    if reg_no is None:
		return redirect('/')
    else:
        try:
            rides = ride_bid.getSingleBid(email,reg_no,start_time)
            update = '1'
            print rides
            return render_template('addBid.html', ride=rides,update=update)
        except ValueError:
            return redirect('/')

@app.route('/updateBid',methods=['POST'])
def Update_Bid():
    if session.get('email') is None:
        return redirect('/login')
    else:
        try:
            reg_no = request.form['reg_no']
            start_time = dt.datetime.strptime(request.form['start_time'], '%Y-%m-%d %H:%M:%S')
            price = request.form['price']
            no_pax = request.form['no_pax']
            email = session.get('email')
            res = ride_bid.update_bid(email,reg_no,start_time,price,no_pax)
            if res != -1:
                return redirect('/')
            else:
                return redirect('/login')
        except ValueError:
            return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
