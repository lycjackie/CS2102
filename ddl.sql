{\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 create table "user"\
(\
	email varchar(256) not null constraint user_pk primary key,\
	contact numeric(8),\
	first_name varchar(50) not null,\
	last_name varchar(50) not null,\
	is_admin boolean default false not null\
);\
\
create table model\
(\
	model varchar(256) not null,\
	make varchar(256) not null,\
	capacity integer not null constraint capacity_min check (capacity > 0),\
	constraint model_pk primary key (model, make)\
);\
\
create table car\
(\
	reg_no varchar(8) not null constraint car_pk primary key,\
	colour varchar(50),\
	email varchar(256) not null constraint car_email_fk references "user",\
	make varchar(50) not null,\
	model varchar(50) not null,\
	constraint car_model_fk foreign key (make, model) references model (make, model)\
);\
\
create table ride\
(\
	start_time timestamp not null,\
	status varchar(10) not null constraint ride_status_type check (((status)::text = 'in progress'::text) OR ((status)::text = 'completed'::text)),\
	current_pax integer not null,\
	destination varchar(256) not null,\
	origin varchar(256) not null,\
	reg_no varchar(8) not null constraint ride_reg_no_fk references car,\
	constraint ride_pk primary key (start_time, reg_no)\
);\
\
create table ride_bid\
(\
	email varchar(256) not null constraint ride_bid_email_fk references "user",\
	start_time timestamp not null,\
	reg_no varchar(8) not null,\
	no_pax integer not null constraint min_pax check (no_pax > 0),\
	bid_price double precision,\
	status varchar(13) not null constraint bid_status_type check (((status)::text = 'pending'::text) OR ((status)::text = 'successful'::text) OR ((status)::text = 'unsuccessful'::text)),\
	constraint ride_bid_pk primary key (email, start_time, reg_no),\
	constraint ride_bid_start_time_fk foreign key (start_time, reg_no) references ride\
);\
\
}