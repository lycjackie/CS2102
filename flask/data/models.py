from dbconfig import connect
import datetime as dt
import psycopg2, psycopg2.extras, psycopg2.sql

'''

'''

# def addRide(ride_details):
#     sql = """
#         INSERT INTO \"Rides\" (\"Driver\", \"RideDateTime\", \"RideEndTime\", \"Origin\", \"Destination\",\"Status\")
#         VALUES (%s,%s,%s,%s,%s,%s) RETURNING \"RideId\";
#           """
#     db = connect()
#     res = None;
#     try:
#         cur = db.cursor()
#         cur.execute(sql,(ride_details['Driver'],ride_details['RideDateTime'],
#                          ride_details['RideEndTime'],ride_details['Origin'],
#                          ride_details['Destination'],ride_details['Status']))
#
#         res = cur.fetchone()[0] # successful insert will return the RideId
#
#         db.commit()
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print error
#     finally:
#         if db is not None:
#             db.close()
#     return res # return the RideId.
#
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

def retrieveAllModels():
    sql = """ SELECT m.\"make\",m.\"model\",m.\"capacity\"
    FROM \"model\" m
    ORDER BY m.make, m.model
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

def retrieveAllModelsForUpdate(reg_no):
    sql = """ SELECT m.\"make\",m.\"model\",m.\"capacity\"
    FROM \"model\" m LEFT OUTER JOIN
    (SELECT c.\"make\",c.\"model\", c.\"reg_no\" FROM \"car\" c WHERE c.\"reg_no\" = %s) m1
    ON m1.\"make\" = m.\"make\" AND m1.\"model\" = m.\"model\"
    ORDER BY m1.\"reg_no\", m.\"make\", m.\"model\"
    """

    db = connect()
    res = None
    try:
        cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) # nameTuple for easier access i.e using .Columns
        cur.execute(sql, [reg_no])
        res = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print error
    finally:
        if db is not None:
            db.close()
    return res

def adminAddModel(model, make, capacity):
    sql = "INSERT INTO \"model\" VALUES (%s, %s, %s);"
    db = connect()
    res = None
    try:
        cur = db.cursor()
        cur.execute(sql, (model, make, capacity))
        db.commit()
        db.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if db is not None:
            db.close()
    return

def adminUpdateModel(model, make, capacity):
    sql = "UPDATE \"model\" SET capacity = %s WHERE model = %s AND make = %s;"
    db = connect()
    res = None
    try:
        cur = db.cursor()
        cur.execute(sql, (capacity, model, make))
        db.commit()
        db.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if db is not None:
            db.close()
    return

def adminDeleteModel(model, make):
    sql = "DELETE FROM \"model\" WHERE model = %s AND make = %s;"
    db = connect()
    res = None
    try:
        cur = db.cursor()
        cur.execute(sql, (model, make))
        db.commit()
        db.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if db is not None:
            db.close()
    return

# def updateRide(rideId, newOrigin, newDestination):
#
#     sql = """ UPDATE \"Rides\"
#     SET \"Origin\" = %s, \"Destination\" = %s
#     WHERE \"RideId\" = %s
#      """
#     db = connect()
#     res = None
#     try:
#         cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) # nameTuple for easier access i.e using .Columns
#         cur.execute(sql, (newOrigin, newDestination, rideId,))
#         db.commit()
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print error
#     finally:
#         if db is not None:
#             db.close()
#     return
#
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
