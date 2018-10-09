from dbconfig import connect
import datetime as dt
import psycopg2, psycopg2.extras, psycopg2.sql

'''

'''

def addCar(car_details):
    sql = """
        INSERT INTO \"car\" (\"reg_no\", \"make\", \"model\", \"colour\", \"email\")
        VALUES (%s,%s,%s,%s,%s) RETURNING \"reg_no\";
          """
    db = connect()
    res = None;
    try:
        cur = db.cursor()
        cur.execute(sql,(car_details['reg_no'],car_details['make'],
                         car_details['model'],car_details['colour'],car_details['email']))

        res = cur.fetchone()[0] # successful insert will return the RideId

        db.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print error
    finally:
        if db is not None:
            db.close()
    return res # return the RideId.

#
# def retrieveAllRide():
#
#     sql = """ SELECT u.\"Name\",u.\"NRIC\",r.\"Origin\",r.\"Destination\",r.\"Status\",r.\"RideId\"
#     FROM \"Rides\" r,\"Users\" u
#     WHERE r.\"Driver\" = u.\"NRIC\"
#     ORDER BY r.\"RideDateTime\" ASC
#      """
#     db = connect()
#     res = None
#     try:
#         cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) # nameTuple for easier access i.e using .Columns
#         cur.execute(sql)
#         res = cur.fetchall()
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print error
#     finally:
#         if db is not None:
#             db.close()
#     return res

def retrieveCarsByEmail(email):
    sql = """ SELECT c.\"reg_no\",c.\"colour\",c.\"make\",c.\"model\",m.\"capacity\"
    FROM \"car\" c,\"model\" m
    WHERE c.\"make\" = m.\"make\" 
    AND c.\"model\" = m.\"model\"
    AND c.\"email\" = %s
    """

    db = connect()
    res = None
    try:
        cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) # nameTuple for easier access i.e using .Columns
        cur.execute(sql, (email,))
        res = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print error
    finally:
        if db is not None:
            db.close()
    return res

def retrieveCarByRegNo(reg_no):
    sql = """ SELECT c.\"reg_no\",c.\"colour\",c.\"make\",c.\"model\",m.\"capacity\"
    FROM \"car\" c,\"model\" m
    WHERE c.\"make\" = m.\"make\" 
    AND c.\"model\" = m.\"model\"
    AND c.\"reg_no\" = %s
    """

    db = connect()
    res = None
    try:
        cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) # nameTuple for easier access i.e using .Columns
        cur.execute(sql, (reg_no,))
        res = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print error
    finally:
        if db is not None:
            db.close()
    return res

def updateCarByRegNo(reg_no, make, model, colour):

    sql = """ UPDATE \"car\"
    SET \"make\" = %s, \"model\" = %s, \"colour\" = %s
    WHERE \"reg_no\" = %s AND NOT EXISTS (
        SELECT * FROM \"ride\" r WHERE r.\"status\" = 'in progress'
        AND r.\"reg_no\" = %s
    ) RETURNING \"reg_no\"
     """
    db = connect()
    res = None
    try:
        cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) # nameTuple for easier access i.e using .Columns
        cur.execute(sql, (make, model, colour, reg_no, reg_no))
        db.commit()
        res = cur.fetchone()[0]  # successful insert will return the RideId
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print error
    finally:
        if db is not None:
            db.close()
    return res

def carBelongsTo(reg_no, email):
    sql = """ SELECT c.\"reg_no\",c.\"email\"
        FROM \"car\" c
        WHERE c.\"reg_no\" = %s
        AND c.\"email\" = %s
        """

    db = connect()
    res = None
    try:
        cur = db.cursor(
            cursor_factory=psycopg2.extras.NamedTupleCursor)  # nameTuple for easier access i.e using .Columns
        cur.execute(sql, (reg_no, email))
        res = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print error
    finally:
        if db is not None:
            db.close()
    return res


# def searchRides(origin, destination):
#
#     sql = """ SELECT u.\"Name\",u.\"NRIC\",r.\"Origin\",r.\"Destination\",r.\"Status\",r.\"RideId\"
#     FROM \"ride\" r,\"user\" u
#     WHERE r.\"Driver\" = u.\"NRIC\" AND LOWER(r.\"Origin\") LIKE LOWER(%s) AND LOWER(r.\"Destination\") LIKE LOWER(%s)
#     ORDER BY r.\"RideDateTime\" ASC
#      """
#     db = connect()
#     res = None
#     try:
#         cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) # nameTuple for easier access i.e using .Columns
#         cur.execute(sql,('%' + origin + '%', '%' + destination + '%'),)
#         res = cur.fetchall()
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print error
#     finally:
#         if db is not None:
#             db.close()
#     return res

if __name__ == '__main__':
    # updateCarByRegNo('STD6250U', 'BMW', '3 Series', 'Grey')
    test_user = {
        'Driver':'123456',
        'RideDateTime': dt.date(2018,9,19),
        'RideEndTime': dt.time(14,00),
        'Origin': 'NUS',
        'Destination': 'Verde Grove',
        'Status': 'GONELOL'
    }
    # #addUser(test_user)
    # #print addRide(test_user)
    # res = retrieveAllRide()
    # for ride in res:
    #     print "Driver {} is {} to go from {} to {}".format(ride.Name,ride.Status,ride.Origin,ride.Destination) # use NamedTuple
