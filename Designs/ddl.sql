create table "user"
(
	email varchar(256) not null constraint user_pk primary key,
	contact numeric(8),
	first_name varchar(50) not null,
	last_name varchar(50) not null,
	is_admin boolean default false not null
);

create table model
(
	model varchar(256) not null,
	make varchar(256) not null,
	capacity integer not null constraint capacity_min check (capacity > 0),
	constraint model_pk primary key (model, make)
);

create table car
(
	reg_no varchar(8) not null constraint car_pk primary key,
	colour varchar(50),
	email varchar(256) not null constraint car_email_fk references "user",
	make varchar(50) not null,
	model varchar(50) not null,
	constraint car_model_fk foreign key (make, model) references model (make, model)
);

create table ride
(
	start_time timestamp not null,
	status varchar(11) not null constraint ride_status_type check (((status) = 'in progress') OR ((status) = 'completed')),
	current_pax integer not null,
	destination varchar(256) not null,
	origin varchar(256) not null,
	reg_no varchar(8) not null constraint ride_reg_no_fk references car,
	constraint ride_pk primary key (start_time, reg_no)
);

create table ride_bid
(
	email varchar(256) not null constraint ride_bid_email_fk references "user",
	start_time timestamp not null,
	reg_no varchar(8) not null,
	no_pax integer not null constraint min_pax check (no_pax > 0),
	bid_price double precision,
	status varchar(13) not null constraint bid_status_type check (((status) = 'pending') OR ((status) = 'successful') OR ((status) = 'unsuccessful')) default 'pending',
	constraint ride_bid_pk primary key (email, start_time, reg_no),
	constraint ride_bid_start_time_fk foreign key (start_time, reg_no) references ride
);
