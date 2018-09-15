import psycopg2
from dbconfig import connect

'''
	CREATE TABLE "Users" (
	"Name" varchar(64) NOT NULL,
	"NRIC" varchar(64) NOT NULL,
	"Contact" numeric NOT NULL,
	CONSTRAINT Users_pk PRIMARY KEY ("NRIC")
)
'''
def addUser(user):
    sql = "INSERT INTO \"Users\" VALUES (%s,%s,%s) RETURNING \"NRIC\";"
    s = None
    db = connect()
    try:
        cur = db.cursor()

        cur.execute(sql, (user['name'],user['nric'],user['contact']))

        s = cur.fetchone()[0]
        ## Insert the role
        if s:
            print "Successfully inserted"
            role_sql = "INSERT INTO \"UserRole\" VALUES (%s,%s) RETURNING \"User_NRIC\";"
            cur.execute(role_sql, (user['nric'],user['role']))

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
    sql = "SELECT * FROM \"Users\" Where \"NRIC\" = %s;"
    res = []
    db = connect()
    try:
        cur = db.cursor()
        no_rows = cur.execute(sql,(user['nric'],)) # need 1 comma behind if only using 1 parameter.

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
