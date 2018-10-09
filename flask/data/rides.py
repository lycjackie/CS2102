from dbconfig import connect
import datetime as dt
import psycopg2, psycopg2.extras, psycopg2.sql

'''
create table ride
(
	start_time timestamp not null,
	status varchar(10) not null constraint ride_status_type check (((status) = 'in progress') OR ((status) = 'completed')),
	current_pax integer not null,
	destination varchar(256) not null,
	origin varchar(256) not null,
	reg_no varchar(8) not null constraint ride_reg_no_fk references car,
	constraint ride_pk primary key (start_time, reg_no)
);
cur.execute(
     INSERT INTO some_table (an_int, a_date, another_date, a_string)
      VALUES (%(int)s, %(date)s, %(date)s, %(str)s);,
     {'int': 10, 'str': "O'Reilly", 'date': datetime.date(2005, 11, 18)})

'''

def addRide(ride_details):
    sql = """
     INSERT INTO ride (start_time,status,current_pax,destination,origin,reg_no)
     VALUES (%s,%s,%s,%s,%s,%s) RETURNING reg_no;
          """
    db = connect()
    res = None;
    try:
        cur = db.cursor()
        print ride_details
        cur.execute(sql,(ride_details['RideStartTime'],ride_details['Status'],
                         ride_details['Current_pax'],ride_details['Destination'],
                         ride_details['Origin'],ride_details['reg_no']))

        res = cur.fetchone()[0] # successful insert will return the RideId

        db.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print "Got Error:"
        print error
    finally:
        if db is not None:
            db.close()
    return res # return the RideId.


def retrieveAllRide():
    sql = """
    SELECT u.first_name, r.origin,r.destination,r.status,r.reg_no,r.start_time
    FROM ride r, "user" u, car c
    WHERE r.reg_no = c.reg_no
    and c.email = u.email
    and r.status = 'in progress'
    ORDER BY r.start_time ASC
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

def retrieveRide(ride_detail):
    sql = """
        SELECT u.first_name, r.origin,r.destination,r.status
        from ride r, "user" u, car c
        WHERE r.reg_no = c.reg_no
        and c.email = u.email
        and r.start_time = %s
        and r.reg_no = %s
     """
    db = connect()
    res = None
    try:
        cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) # nameTuple for easier access i.e using .Columns
        cur.execute(sql, (ride_detail['RideStartTime'],ride_detail['reg_no']))
        res = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print error
    finally:
        if db is not None:
            db.close()
    return res

def updateRide(rideId, newOrigin, newDestination):

    sql = """ UPDATE \"Rides\"
    SET \"Origin\" = %s, \"Destination\" = %s
    WHERE \"RideId\" = %s
     """
    db = connect()
    res = None
    try:
        cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) # nameTuple for easier access i.e using .Columns
        cur.execute(sql, (newOrigin, newDestination, rideId,))
        db.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print error
    finally:
        if db is not None:
            db.close()
    return

def searchRides(origin, destination):

    sql = """ SELECT u.\"Name\",u.\"NRIC\",r.\"Origin\",r.\"Destination\",r.\"Status\",r.\"RideId\"
    FROM \"ride\" r,\"user\" u
    WHERE r.\"Driver\" = u.\"NRIC\" AND LOWER(r.\"Origin\") LIKE LOWER(%s) AND LOWER(r.\"Destination\") LIKE LOWER(%s)
    ORDER BY r.\"RideDateTime\" ASC
     """
    db = connect()
    res = None
    try:
        cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) # nameTuple for easier access i.e using .Columns
        cur.execute(sql,('%' + origin + '%', '%' + destination + '%'),)
        res = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print error
    finally:
        if db is not None:
            db.close()
    return res

if __name__ == '__main__':
    '''
            cur.execute(sql,(ride_details['RideStartTime'],ride_details['Status'],
                             ride_details['current_pax'],ride_details['destination'],
                             ride_details['origin'],ride_details['reg_no']))
                             '''
    test_user = {
        'reg_no':'SGX1337X',
        'RideStartTime': dt.datetime.combine(dt.date(2018,9,19),dt.time(14,00)),
        'Current_pax': 0,
        'Origin': 'NUS',
        'Destination': 'Verde Grove',
        'Status': 'completed'
    }
    #addUser(test_user)
    #print addRide(test_user)
    res = retrieveAllRide()
    #print retrieveRide(test_user)
    for ride in res:
        print "Driver {} is {} to go from {} to {}".format(ride.reg_no,ride.status,ride.origin,ride.destination) # use NamedTuple
