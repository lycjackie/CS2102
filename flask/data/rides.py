from dbconfig import connect
import datetime as dt
import psycopg2, psycopg2.extras

'''
create table if not exists "Rides"
(
  "RideId"       serial      not null
    constraint rides_pk
    primary key,
  "Driver"       varchar(64) not null
    constraint "Rides_fk0"
    references "Users",
  "RideDateTime" date        not null,
  "RideEndTime"  date        not null,
  "Origin"       varchar(64) not null,
  "Destination"  varchar(64) not null,
  "Status"       varchar(64) not null
);
cur.execute(
     INSERT INTO some_table (an_int, a_date, another_date, a_string)
      VALUES (%(int)s, %(date)s, %(date)s, %(str)s);,
     {'int': 10, 'str': "O'Reilly", 'date': datetime.date(2005, 11, 18)})
'''

def addRide(ride_details):
    sql = """
        INSERT INTO \"Rides\" (\"Driver\", \"RideDateTime\", \"RideEndTime\", \"Origin\", \"Destination\",\"Status\")
        VALUES (%s,%s,%s,%s,%s,%s) RETURNING \"RideId\";
          """
    db = connect()
    res = None;
    try:
        cur = db.cursor()
        cur.execute(sql,(ride_details['Driver'],ride_details['RideDateTime'],
                         ride_details['RideEndTime'],ride_details['Origin'],
                         ride_details['Destination'],ride_details['Status']))

        res = cur.fetchone()[0] # successful insert will return the RideId

        db.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print error
    finally:
        if db is not None:
            db.close()
    return res # return the RideId.


def retrieveAllRide():

    sql = """ SELECT u.\"Name\",r.\"Origin\",r.\"Destination\",r.\"Status\"
    FROM \"Rides\" r,\"Users\" u
    WHERE r.\"Driver\" = u.\"NRIC\"
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

if __name__ == '__main__':
    test_user = {
        'Driver':'123456',
        'RideDateTime': dt.date(2018,9,19),
        'RideEndTime': dt.time(14,00),
        'Origin': 'NUS',
        'Destination': 'Verde Grove',
        'Status': 'GONELOL'
    }
    #addUser(test_user)
    #print addRide(test_user)
    res = retrieveAllRide()
    for ride in res:
        print "Driver {} is {} to go from {} to {}".format(ride.Name,ride.Status,ride.Origin,ride.Destination) # use NamedTuple
