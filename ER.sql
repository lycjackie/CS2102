create table if not exists "Car"
(
  "Model" varchar(64) not null
    constraint car_pk
    primary key,
  "Maker" varchar(64) not null,
  "Seats" numeric(64) not null
);

create table if not exists "Users"
(
  "Name"    varchar(64) not null,
  "NRIC"    varchar(64) not null
    constraint users_pk
    primary key,
  "Contact" numeric     not null
);

create table if not exists "UserCar"
(
  "VehicleNo" varchar(12) not null
    constraint usercar_pk
    primary key,
  "Color"     varchar(64) not null,
  "Model"     varchar(64) not null
    constraint "UserCar_fk0"
    references "Car",
  "NRIC"      varchar(64) not null
    constraint "UserCar_fk1"
    references "Users"
);

create table if not exists "Rides"
(
  "RideId"       serial      not null
    constraint rides_pk
    primary key,
  "Driver"       varchar(64) not null
    constraint "Rides_fk0"
    references "Users",
  "RideDateTime" date        not null,
  "RideEndTime"  date        not null,
  "Origin"       varchar(64) not null,
  "Destination"  varchar(64) not null,
  "Status"       varchar(64) not null
);

create table if not exists "RideBids"
(
  "UserBid"    varchar(64) not null
    constraint "RideBids_fk0"
    references "Users",
  "RideId"     integer     not null
    constraint "RideBids_fk1"
    references "Rides",
  "BidPrice"   numeric     not null,
  "Passengers" numeric     not null
);

create table if not exists "Roles"
(
  "RoleId"   serial      not null
    constraint "Roles_pkey"
    primary key,
  "RoleName" varchar(64) not null
    constraint "Roles_RoleName_key"
    unique
);

create table if not exists "UserRole"
(
  "User_NRIC" varchar(64) not null
    constraint "UserRole_fk0"
    references "Users"
    on delete cascade,
  "RoleId"    integer     not null
    constraint "UserRole_fk1"
    references "Roles"
    on delete cascade
);

