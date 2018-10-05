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

select p.name
from person p, friend f
where p.id = f.id2
and f.id1 = f.id2

select p.name
from person p, friend f1, friend f2
and p.id = f1.id1
and f1.id1 = f2.id2
and f1.id2 = f1.id1
group by p.id. p.name


select p.name, count(*)
from person p, friend f
where p.id = f.id1
group by u.id,u.name
-- having count(*) > 1
