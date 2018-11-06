import psycopg2
from dbconfig import connect
import hashlib

'''
create table "user"
(
	email varchar(256) not null constraint user_pk primary key,
	contact numeric(8),
	first_name varchar(50) not null,
	last_name varchar(50) not null,
	is_admin boolean default false not null
);
'''
def addUser(user):
    #sql = "INSERT INTO \"user\" VALUES (%s,%s,%s,%s,false,%s) RETURNING \"email\";"
    sql = "SELECT REGISTER(%s,%s,%s,%s,%s)"
    s = None
    db = connect()
    try:
        cur = db.cursor()
        #password = hash_it(user['password'])
        cur.execute(sql, (user['email'],user['contact'],user['firstName'],user['lastName'],user['password']))

        s = cur.fetchone()[0]
        ## Insert the role
        if s:
			print "Successfully inserted"
        #     role_sql = "INSERT INTO \"UserRole\" VALUES (%s,%s) RETURNING \"User_NRIC\";"
        #     cur.execute(role_sql, (user['nric'],user['role']))

        # finish
        db.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if db is not None:
            db.close()

    return s


def updateUser(email, first_name, last_name):
    sql = "UPDATE \"user\" SET first_name = %s, last_name = %s WHERE email = %s;"
    s = None
    db = connect()
    try:
        cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) # nameTuple for easier access i.e using .Columns

        cur.execute(sql, (first_name, last_name, email))
        # finish
        db.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if db is not None:
            db.close()

    return

def adminUpdateUser(email, contact, first_name, last_name, password):
	sql = ""
	if password != "":
		sql = "UPDATE \"user\" SET first_name = %s, last_name = %s, contact = %s, password = %s WHERE email = %s;"
	else:
		sql = "UPDATE \"user\" SET first_name = %s, last_name = %s, contact = %s WHERE email = %s;"
	s = None
	db = connect()
	try:
		cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) # nameTuple for easier access i.e using .Columns
		if password != "":
			cur.execute(sql, (first_name, last_name, contact, hash_it(password), email))
		else:
			cur.execute(sql, (first_name, last_name, contact, email))
		# finish
		db.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if db is not None:
			db.close()

	return

def adminDeleteUser(email):
	sql = "DELETE FROM \"user\" WHERE email = %s;"
	s = None
	db = connect()
	try:
		cur = db.cursor()
		cur.execute(sql, (email,))
		db.commit()
		db.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if db is not None:
			db.close()
	return

def retrieveUser(user):
    #sql = "SELECT * FROM \"user\" Where \"email\" = %s AND \"password\" = %s;"
    sql = "select * from login(%s,%s)"
    res = []
    db = connect()
    try:
        cur = db.cursor()
        #password = hash_it(user['password'])
        no_rows = cur.execute(sql,(user['email'],user['password'])) # need 1 comma behind if only using 1 parameter.

        while True: # loop cursor and retrieve results
			row = cur.fetchone() # should only return 1 result
			if row == None:
				break
			res.append(row)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if db is not None:
            db.close()

    return res

def retrieveAllUsers():
	sql = "SELECT * FROM \"user\";"
	res = []
	db = connect()
	try:
		cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
		no_rows = cur.execute(sql)
		res = cur.fetchall()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if db is not None:
			db.close()
	return res

def hash_it(password):
    m = hashlib.sha256()
    m.update(password)
    return m.hexdigest()

if __name__ == '__main__':
    test_user = {
        'name':'jackie',
        'nric':'123456',
        'contact': 99112233,
        'role': 3
    }
    #addUser(test_user)
    print retrieveUser(test_user)
