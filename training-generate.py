#!/usr/bin/python

import random
import string
import itertools
'''
CREATE TABLE person (
	id varchar(60) primary key,
	name varchar(60) not null
)

CREATE TABLE friend (
	id1 varchar(60) not null,
	id2 varchar(60) not null,
	PRIMARY KEY (id1,id2),
	FOREIGN KEY (id1) references person(id),
	FOREIGN KEY (id2) references person(id)
)
'''

class friend:
	def __init__(self,id1,id2):
		self.id1 = id1
		self.id2 = id2

def random_char(y):
	return ''.join(random.choice(string.ascii_letters) for x in range (y)) 


user = [] 
for i in range(30):
	user.append(random_char(8))

#print user

friend_list = []
for each_pair in itertools.permutations(user,2):
	#print each_pair
	if random.randint(0,100) > 25:
		friend_list.append(friend(each_pair[0],each_pair[1]))

#print len(friend_list)

insert_person = """
INSERT INTO PERSON VALUES ('{}', '{}');
"""

insert_friend = """
INSERT INTO FRIEND VALUES ('{}', '{}');
"""

for u in user:
	print insert_person.format(u,u)

for friend in friend_list:
	print insert_friend.format(friend.id1,friend.id2)



