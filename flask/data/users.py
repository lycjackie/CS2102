import psycopg2
from dbconfig import connect

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
    sql = "INSERT INTO \"user\" VALUES (%s,%s,%s,%s,false) RETURNING \"email\";"
    s = None
    db = connect()
    try:
        cur = db.cursor()

        cur.execute(sql, (user['email'],user['contact'],user['firstName'],user['lastName']))

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



def retrieveUser(user):
    sql = "SELECT * FROM \"user\" Where \"email\" = %s;"
    res = []
    db = connect()
    try:
        cur = db.cursor()
        no_rows = cur.execute(sql,(user['email'],)) # need 1 comma behind if only using 1 parameter.

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


if __name__ == '__main__':
    test_user = {
        'name':'jackie',
        'nric':'123456',
        'contact': 99112233,
        'role': 3
    }
    #addUser(test_user)
    print retrieveUser(test_user)
