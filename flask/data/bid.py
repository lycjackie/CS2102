from dbconfig import connect
import datetime as dt
import psycopg2, psycopg2.extras, psycopg2.sql
'''
create table ride_bid
(
	email varchar(256) not null constraint ride_bid_email_fk references "user",
	start_time timestamp not null,
	reg_no varchar(8) not null,
	no_pax integer not null constraint min_pax check (no_pax > 0),
	bid_price double precision,
	status varchar(13) not null constraint bid_status_type check (((status) = 'pending') OR ((status) = 'successful') OR ((status) = 'unsuccessful')),
	constraint ride_bid_pk primary key (email, start_time, reg_no),
	constraint ride_bid_start_time_fk foreign key (start_time, reg_no) references ride
);
'''
def add_bid(bid_detail):
    sql = """
    INSERT INTO ride_bid (email,start_time,reg_no,no_pax,bid_price) VALUES (%s,%s,%s,%s,%s)
    """
    db = connect()
    res = None
    try:
	cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) # nameTuple for easier access i.e using .Columns
	cur.execute(sql,(bid_detail['email'],bid_detail['start_time'],bid_detail['reg_no'],bid_detail['no_pax'],bid_detail['bid_price']))
	res = cur.rowcount
	print 'row count ' + str(res)
	db.commit()
	cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print "Got Error:",res
        print error
        return str(error)
    finally:
        if db is not None:
            db.close()
    return res

# Get bid for the owner to approve or list all bid
def get_bid(email):
	sql= """
	SELECT rb.reg_no,c.email as owner, rb.email as bidder, r.origin,r.destination,rb.start_time,rb.status, rb.bid_price as bid_amt, (rb.bid_price * rb.no_pax) as bid_price, rb.no_pax
	FROM ride_bid rb
	inner join ride r ON rb.reg_no = r.reg_no and rb.start_time = r.start_time
	INNER JOIN car c on r.reg_no = c.reg_no
	where c.email LIKE %s
	and rb.status = 'pending'
	"""
	db = connect()
	res = None
	email = '%' + email +'%'
	try:
		cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) # nameTuple for easier access i.e using .Columns
		cur.execute(sql,(email,))
		res = cur.fetchall()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
	    print error
	finally:
	    if db is not None:
	        db.close()
	return res
def getSingleBid(email,reg_no,start_time):
	sql="""
	SELECT rb.email as bidder , rb.reg_no, u.first_name as bidder_name , r.destination, r.origin, rb.start_time, rb.status, rb.bid_price as bid_amt, (rb.bid_price * rb.no_pax) as bid_price, rb.no_pax, (m.capacity - r.current_pax) as pax_left
	FROM ride_bid as rb
	INNER JOIN \"user\" u on u.email = rb.email
	INNER JOIN ride r on rb.reg_no = r.reg_no and rb.start_time = r.start_time
	INNER JOIN car c on c.reg_no = r.reg_no
	INNER JOIN \"model\" m on m.model = c.model AND c.make = m.make
	AND rb.email = %s
	AND rb.reg_no = %s
	and rb.start_time = %s
	"""
	db = connect()
	res = None
	try:
		cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) # nameTuple for easier access i.e using .Columns
		cur.execute(sql,(email,reg_no,start_time))
		res = cur.fetchone()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
	    print error
	finally:
	    if db is not None:
	        db.close()
	return res
def approve_bid(email,reg_no,start_time,status,owner_email):
	sql = """
	UPDATE ride_bid rb set status = %s
	WHERE rb.reg_no = %s AND rb.start_time = %s
	AND rb.email = %s
	AND rb.reg_no in (
		SELECT c.reg_no
		FROM car c
		WHERE c.email = %s
	)
	RETURNING rb.status
	"""
	db = connect()
	res = None
	print email
	print reg_no
	print start_time
	print status
	print owner_email
	try:
		cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) # nameTuple for easier access i.e using .Columns
		cur.execute(sql, (status,reg_no,start_time,email,owner_email,) )
		res = cur.fetchone()
		db.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print "Got Error:"
		print error
	finally:
		if db is not None:
			db.close()
	return res

def get_AllBidForSingleRide(reg_no,start_time):
	sql = """
	SELECT rb.reg_no,c.email as owner, rb.email as bidder,u.first_name as bidder_name, r.origin,r.destination,rb.start_time,rb.status, rb.bid_price as bid_amt, (rb.bid_price * rb.no_pax) as bid_price, rb.no_pax
	FROM ride_bid rb
	inner join ride r ON rb.reg_no = r.reg_no and rb.start_time = r.start_time
	INNER JOIN car c on r.reg_no = c.reg_no
	INNER JOIN \"user\" u on rb.email = u.email
	where rb.reg_no = %s
	and rb.start_time = %s
	and (rb.status = 'pending' OR rb.status = 'successful')
	ORDER BY  rb.status DESC ,rb.bid_price DESC
	"""
	db = connect()
	res = None
	try:
		cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) # nameTuple for easier access i.e using .Columns
		cur.execute(sql,(reg_no,start_time))
		res = cur.fetchall()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
	    print error
	finally:
	    if db is not None:
	        db.close()
	return res

def update_bid(email,reg_no,start_time,bid_price,total_pax):
	sql = """
	UPDATE ride_bid rb
	SET bid_price = %s , no_pax = %s
	WHERE rb.email = %s
	AND	rb.start_time = %s
	AND rb.reg_no = %s
	"""
	db = connect()
	res = None
	try:
		cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) # nameTuple for easier access i.e using .Columns
		cur.execute(sql, (bid_price,total_pax,email,start_time,reg_no))
		res = cur.rowcount
		db.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print "Got Error:"
		print error
	finally:
		if db is not None:
			db.close()
	return res

def success_bid(email,reg_no,start_time):
	sql = """
	SELECT *
	FROM ride_bid rb
	WHERE email = %s
	AND reg_no = %s
	AND start_time = %s
	AND status in ('successful','pending')
	"""
	db = connect()
	res = None
	try:
		cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) # nameTuple for easier access i.e using .Columns
		cur.execute(sql,(email,reg_no,start_time))
		res = cur.fetchall()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
	    print error
	finally:
	    if db is not None:
	        db.close()
	return res

if __name__ == '__main__':
	test_user = {
	    'reg_no':'SGX1337X',
	    'start_time': dt.datetime.combine(dt.date(2018,9,19),dt.time(14,00)),
	    'no_pax': 1,
	    'bid_price': 13.37,
		'email':'owerv@tamu.edu'
	}
	#print add_bid(test_user)
	#print get_bid('wpicklessi@geocities.com')
	#print get_AllBidForSingleRide('SGX1337X',dt.datetime.combine(dt.date(2018,9,19),dt.time(14,00)))
	#a =  getSingleBid('a@a.com','SGX1337X',dt.datetime.combine(dt.date(2018,9,19),dt.time(14,00)))


	#print approve_bid('a@a.com','SGX1337X',dt.datetime.strptime('2018-09-19 14:00:00','%Y-%m-%d %H:%M:%S'),'unsuccessful','wpicklessi@geocities.com')
