# CS2102 Project Report

>Members
>
>1. Ang Wei Ming
>2. Benjamin Chin Choon Kiat, A0168698B
>3. Lee Yu Choy, A0177151H
>4. Yeo Cheng Hong

## General Architecture



## SQL DDL

```sql
create table if not exists "user" -- `"` used because PostgreSQL use 'user' as a keyword
(
	email varchar(256) not null
		constraint user_pkey
			primary key,
	contact numeric(8),
	first_name varchar(50) not null,
	last_name varchar(50) not null,
	is_admin boolean default false not null,
	password varchar(512) not null
)
;

create table if not exists model
(
	model varchar(256) not null,
	make varchar(256) not null,
	capacity integer not null
		constraint capacity_min
			check (capacity > 0),
	constraint model_pk
		primary key (model, make)
)
;


create table if not exists car
(
	reg_no varchar(8) not null
		constraint car_pkey
			primary key,
	colour varchar(50),
	email varchar(256) not null
		constraint car_email_fkey
			references "user",
	make varchar(50) not null,
	model varchar(50) not null,
	constraint car_make_fkey
		foreign key (make, model) references model (make, model)
)
;


create table if not exists ride
(
	start_time timestamp not null,
	status varchar(11) not null
		constraint ride_status_type
			check (((status)::text = 'in progress'::text) OR ((status)::text = 'completed'::text)),
	current_pax integer not null,
	destination varchar(256) not null,
	origin varchar(256) not null,
	reg_no varchar(8) not null
		constraint ride_reg_no_fkey
			references car,
	constraint ride_pkey
		primary key (start_time, reg_no)
)
;


create table if not exists ride_bid
(
	email varchar(256) not null
		constraint ride_bid_email_fkey
			references "user",
	start_time timestamp not null,
	reg_no varchar(8) not null,
	no_pax integer not null
		constraint min_pax
			check (no_pax > 0),
	bid_price double precision check (bid_price > 0 ),
	status varchar(13) default 'pending'::character varying not null
		constraint bid_status_type
			check (((status)::text = 'pending'::text) OR ((status)::text = 'successful'::text) OR ((status)::text = 'unsuccessful'::text)),
	constraint ride_bid_pkey
		primary key (email, start_time, reg_no),
	constraint ride_bid_start_time_fkey
		foreign key (start_time, reg_no) references ride
)
;


create table if not exists audit_log
(
	start_time timestamp not null,
	end_time timestamp not null,
	status varchar(11) not null
		constraint ride_status_type
			check ((status)::text = 'completed'::text),
	current_pax integer not null,
	destination varchar(256) not null,
	origin varchar(256) not null,
	reg_no varchar(8) not null
		constraint ride_reg_no_fk
			references car,
	constraint ride_pk
		primary key (start_time, reg_no)
)
;


```

### Triggers and function

```sql

create or replace function on_approval_update_pax() returns trigger
	language plpgsql
as $$
BEGIN
 IF NEW.status = 'successful' and OLD.STATUS <> 'successful'
 THEN
	UPDATE ride
		SET current_pax = current_pax + NEW.no_pax
	 WHERE reg_no = NEW.reg_no
	 AND start_time = NEW.start_time;
  UPDATE ride_bid rb
    SET status = 'unsuccessful'
  FROM ride r, car c, model m
  WHERE r.reg_no = rb.reg_no
  AND r.start_time = rb.start_time
  AND r.reg_no = c.reg_no
  AND c.make = m.make
  AND c.model = m.model
  AND rb.reg_no = NEW.reg_no
  AND rb.start_time = NEW.start_time
  AND rb.status = 'pending'
  AND rb.no_pax > (m.capacity - r.current_pax);
 END IF;

 RETURN NULL;
END
$$
;


create trigger approval_update
	after update
	on ride_bid
	for each row
	execute procedure on_approval_update_pax()
;







create or replace function audit() returns trigger
	language plpgsql
as $$
BEGIN
  IF NEW.status = 'completed' THEN
  INSERT INTO audit_log(start_time,end_time,status,current_pax,destination,origin,reg_no)
  VALUES (OLD.start_time,now(),NEW.status,OLD.current_pax,OLD.destination,OLD.origin,OLD.reg_no);
  END IF;

  RETURN NEW;
END;
$$
;

create trigger to_audit
	before update
	on ride
	for each row
	execute procedure audit()
;
```



```sql
create or replace function capacity_checker()
  returns trigger
language plpgsql
as $$
BEGIN
  IF (SELECT (r.current_pax + NEW.no_pax <= m.capacity)
      FROM ride r
             inner join car c on r.reg_no = c.reg_no
             INNER JOIN model m on c.make = m.make and c.model = m.model
                                     AND r.reg_no = NEW.reg_no
                                     AND r.start_time = NEW.start_time)
  THEN
  --
  -- Do nothing
  ELSE
    RAISE EXCEPTION 'Exceeded maximum capacity, please reduce your number of passenger';
  END IF;
  IF (SELECT (1)
      FROM ride r
             INNER JOIN car c on r.reg_no = c.reg_no
      where r.reg_no = NEW.reg_no
        AND r.start_time = NEW.start_time
        AND c.email = NEW.email)
  THEN RAISE EXCEPTION 'Cannot Bid for Own Ride';
  ELSE
    RETURN NEW;
  END IF;
END
$$;

create trigger cap_check
	before insert
	on ride_bid
	for each row
	execute procedure capacity_checker()
;
```





### Sample Code SQL

#### Complex SQL

> Ride Capacity Update and checks

For every `successful`  ride bid that is approved by the `driver` , there will be a trigger to update the current capacity of the ride.

##### Trigger as shown below

```sql
create trigger approval_update
	after update
	on ride_bid
	for each row
	execute procedure on_approval_update_pax()
;
```

##### on_approval_update_pax function

```sql
create or replace function on_approval_update_pax() returns trigger
	language plpgsql
as $$
BEGIN
 IF NEW.status = 'successful' and OLD.STATUS <> 'successful'
 THEN
	UPDATE ride
		SET current_pax = current_pax + NEW.no_pax
	 WHERE reg_no = NEW.reg_no
	 AND start_time = NEW.start_time;
	 -- The following part update all current biddings which have their number of passenger above the current available seats
	 -- for example total pax is 4, current pax is 2
	 -- all bidding which is >2 will be automatically changed to unsuccessful
  UPDATE ride_bid rb
    SET status = 'unsuccessful'
  FROM ride r, car c, model m
  WHERE r.reg_no = rb.reg_no
  AND r.start_time = rb.start_time
  AND r.reg_no = c.reg_no
  AND c.make = m.make
  AND c.model = m.model
  AND rb.reg_no = NEW.reg_no
  AND rb.start_time = NEW.start_time
  AND rb.status = 'pending'
  AND rb.no_pax > (m.capacity - r.current_pax);
 END IF;
 -- return NULL as trigger is called after update
 RETURN NULL;
END
$$
;
```

The `current_pax` attribute allow us to check for available seats easily. 

Which is being shown below

##### Query to retrieve Ride information

```sql
SELECT u.first_name, r.origin,r.destination,r.status,r.start_time,r.reg_no, (m.capacity - r.current_pax) as pax_left
FROM ride r, "user" u, car c,model m
WHERE r.reg_no = c.reg_no
AND c.model = m.model
AND c.make = m.make
AND c.email = u.email
AND r.start_time = %s
AND r.reg_no = %s
```



### Search Ride

> If origin and destination is `NULL`, return all rides

```sql
SELECT u.first_name,u.email,r.origin,r.destination,r.status,r.reg_no, r.start_time, r.current_pax, (m.capacity - r.current_pax) as pax_left,
EXISTS (SELECT c1.email FROM car c1 WHERE c1.reg_no = c.reg_no AND c1.email = %s) as is_driver,
EXISTS (SELECT rb.email FROM ride_bid rb WHERE rb.reg_no = c.reg_no AND rb.email = %s AND rb.status = 'successful' AND rb.start_time = r.start_time) as has_success_bid,
EXISTS (SELECT rb.email FROM ride_bid rb WHERE rb.reg_no = c.reg_no AND rb.email = %s AND rb.status = 'unsuccessful' AND rb.start_time = r.start_time) as has_unsuccessful_bid,
EXISTS (SELECT rb.email FROM ride_bid rb WHERE rb.reg_no = c.reg_no AND rb.email = %s AND rb.status = 'pending' AND rb.start_time = r.start_time) as has_pending_bid
FROM ride r, "user" u, car c,model m
WHERE r.reg_no = c.reg_no
and c.email = u.email
and LOWER(r.origin) LIKE LOWER(%s) and LOWER(r.destination) like LOWER(%s)
and r.status = 'in progress'
and c.make = m.make
and c.model = m.model
ORDER BY r.start_time ASC
     
```



## Rejection of Bid 



> When the car ride available capacity is below what the user is bidding for, the system will reject the transaction via `trigger`

### Trigger

```sql
create or replace function capacity_checker() returns trigger
	language plpgsql
as $$
BEGIN
    IF ( SELECT (r.current_pax + NEW.no_pax <= m.capacity)
    FROM ride r
    inner join car c on r.reg_no = c.reg_no
    INNER JOIN model m on c.make = m.make and c.model =m.model
    AND r.reg_no = NEW.reg_no
    AND r.start_time = NEW.start_time)
      THEN
      RETURN NEW;
  ELSE
  RAISE EXCEPTION 'Exceeded maximum capacity, please reduce your number of passenger';
     END IF;
END
$$
;

create trigger cap_check
	before insert
	on ride_bid
	for each row
	execute procedure capacity_checker()
;	
```

### Simple Insert Query

```sql
INSERT INTO ride_bid (email,start_time,reg_no,no_pax,bid_price) VALUES (%s,%s,%s,%s,%s)
```



## Ride History

### Trigger

```sql
create or replace function audit() returns trigger
	language plpgsql
as $$
BEGIN
  IF NEW.status = 'completed' THEN
  INSERT INTO audit_log(start_time,end_time,status,current_pax,destination,origin,reg_no)
  VALUES (OLD.start_time,now(),NEW.status,OLD.current_pax,OLD.destination,OLD.origin,OLD.reg_no);
  END IF;

  RETURN NEW;
END;
$$
;

create trigger to_audit
	before update
	on ride
	for each row
	execute procedure audit()
;
```

### Simple Update Query

```sql
UPDATE ride
    SET origin = %s, destination = %s, status = %s
    WHERE reg_no = %s AND start_time = %s
```



## Screen shots

