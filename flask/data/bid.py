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
    INSERT INTO ride_bid (email,start_time,reg_no,no_pax,bid_price) VALUES (%s,%s,%s,%s,%s) RETURNING status
    """
    db = connect()
    res = None
    try:
        cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) # nameTuple for easier access i.e using .Columns
        cur.execute(sql,(bid_detail['email'],bid_detail['start_time'],bid_detail['reg_no'],bid_detail['no_pax'],bid_detail['bid_price']))
        res = cur.fetchone()[0]

        db.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print "Got Error:"
        print error
    finally:
        if db is not None:
            db.close()
    return res

# Get bid for the owner to approve or list all bid
def get_bid(email):
	sql= """
	SELECT rb.reg_no,c.email as owner, rb.email as bidder, r.origin,r.destination,rb.start_time,rb.status, (rb.bid_price * rb.no_pax) as bid_price, rb.no_pax
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

def get_available_bidding():
	sql= """
	SELECT r.reg_no,r.start_time
	FROM ride r
	where r.status = 'in progress'
	"""
	db = connect()
	res = None
	try:
		cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) # nameTuple for easier access i.e using .Columns
		cur.execute(sql)
		res = cur.fetchall()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
	    print error
	finally:
	    if db is not None:
	        db.close()
	return res

def bid_approval(email,reg_no,start_time,status):
	sql = """
	UPDATE ride_bid set status = %s
	WHERE reg_no = %s AND start_time = %s
	AND email = %s
	RETURNING status
	"""
	db = connect()
	res = None
	try:
		cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) # nameTuple for easier access i.e using .Columns
		cur.execute(sql,(status,reg_no,start_time,email))
		res = cur.fetchone()[0]
		db.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print "Got Error:"
		print error
	finally:
		if db is not None:
			db.close()
	return res

def get_single_bid(email,reg_no,start_time):
	sql = """SELECT * from ride_bid where email = %s and reg_no = %s and start_time = %s and status='pending'"""
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

def update_bid(reg_no,start_time,bid_price):
    return 0

if __name__ == '__main__':
	test_user = {
	    'reg_no':'SGX1337X',
	    'start_time': dt.datetime.combine(dt.date(2018,9,19),dt.time(14,00)),
	    'no_pax': 1,
	    'bid_price': 13.37,
		'email':'owerv@tamu.edu'
	}
	#print add_bid(test_user)
	print get_bid('wpicklessi@geocities.com')
	#print get_single_bid('a@a.com','SGX1337X',dt.datetime.combine(dt.date(2018,9,19),dt.time(14,00)))
	
	#print bid_approval('owerv@tamu.edu','SGX1337X',dt.datetime.combine(dt.date(2018,9,19),dt.time(14,00)),'successful')
