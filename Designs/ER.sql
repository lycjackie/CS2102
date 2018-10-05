create database cs2102_project
with owner postgres;

create table if not exists "Car"
(
  "Model" varchar(64) not null,
  "Maker" varchar(64) not null,
  "Seats" numeric(64) not null,
  constraint car_pk
  primary key ("Model")
);

create table if not exists "Users"
(
  "Name"    varchar(64) not null,
  "NRIC"    varchar(64) not null,
  "Contact" numeric     not null,
  constraint users_pk
  primary key ("NRIC")
);

create table if not exists "UserCar"
(
  "VehicleNo" varchar(12) not null,
  "Color"     varchar(64) not null,
  "Model"     varchar(64) not null,
  "NRIC"      varchar(64) not null,
  constraint usercar_pk
  primary key ("VehicleNo"),
  constraint "UserCar_fk0"
  foreign key ("Model") references "Car",
  constraint "UserCar_fk1"
  foreign key ("NRIC") references "Users"
);

create table if not exists "Roles"
(
  "RoleId"   serial      not null,
  "RoleName" varchar(64) not null,
  constraint "Roles_pkey"
  primary key ("RoleId"),
  constraint "Roles_RoleName_key"
  unique ("RoleName")
);

create table if not exists "UserRole"
(
  "User_NRIC" varchar(64) not null,
  "RoleId"    integer     not null,
  constraint "UserRole_fk0"
  foreign key ("User_NRIC") references "Users"
  on delete cascade,
  constraint "UserRole_fk1"
  foreign key ("RoleId") references "Roles"
  on delete cascade
);

create table if not exists "Rides"
(
  "RideId"       serial      not null,
  "Driver"       varchar(64) not null,
  "RideDateTime" date        not null,
  "RideEndTime"  time        not null,
  "Origin"       varchar(64) not null,
  "Destination"  varchar(64) not null,
  "Status"       varchar(64) not null,
  constraint rides_pk
  primary key ("RideId"),
  constraint "Rides_fk0"
  foreign key ("Driver") references "Users"
  on delete cascade
);

create table if not exists "RideBids"
(
  "UserBid"    varchar(64) not null,
  "RideId"     integer     not null,
  "BidPrice"   numeric     not null,
  "Passengers" numeric     not null,
  constraint "RideBids_fk0"
  foreign key ("UserBid") references "Users"
  on delete cascade,
  constraint "RideBids_fk1"
  foreign key ("RideId") references "Rides"
  on delete cascade
);
