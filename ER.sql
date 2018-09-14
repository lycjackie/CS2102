CREATE TABLE "Users" (
	"Name" varchar(64) NOT NULL,
	"NRIC" serial(64) NOT NULL,
	"Contact" numeric(64) NOT NULL,
	CONSTRAINT Users_pk PRIMARY KEY ("NRIC")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Roles" (
	"RoleId" serial NOT NULL,
	"RoleName" varchar(64) NOT NULL UNIQUE,
	CONSTRAINT Roles_pk PRIMARY KEY ("RoleId")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Car" (
	"Model" varchar(64) NOT NULL,
	"Maker" varchar(64) NOT NULL,
	"Seats" numeric(64) NOT NULL,
	CONSTRAINT Car_pk PRIMARY KEY ("Model")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "UserCar" (
	"VehicleNo" varchar(12) NOT NULL,
	"Color" varchar(64) NOT NULL,
	"Model" varchar(64) NOT NULL,
	"NRIC" varchar(64) NOT NULL,
	CONSTRAINT UserCar_pk PRIMARY KEY ("VehicleNo")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "UserRole" (
	"User_NRIC" varchar(64) NOT NULL,
	"RoleId" int(64) NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Rides" (
	"RideId" serial NOT NULL,
	"Driver" varchar(64) NOT NULL,
	"RideDateTime" DATE NOT NULL,
	"RideEndTime" DATE NOT NULL,
	"Origin" varchar(64) NOT NULL,
	"Destination" varchar(64) NOT NULL,
	"Status" varchar(64) NOT NULL,
	CONSTRAINT Rides_pk PRIMARY KEY ("RideId")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "RideBids" (
	"UserBid" varchar(64) NOT NULL,
	"RideId" int NOT NULL,
	"BidPrice" numeric NOT NULL,
	"Passengers" numeric NOT NULL
) WITH (
  OIDS=FALSE
);






ALTER TABLE "UserCar" ADD CONSTRAINT "UserCar_fk0" FOREIGN KEY ("Model") REFERENCES "Car"("Model");
ALTER TABLE "UserCar" ADD CONSTRAINT "UserCar_fk1" FOREIGN KEY ("NRIC") REFERENCES "Users"("NRIC");

ALTER TABLE "UserRole" ADD CONSTRAINT "UserRole_fk0" FOREIGN KEY ("User_NRIC") REFERENCES "Users"("NRIC");
ALTER TABLE "UserRole" ADD CONSTRAINT "UserRole_fk1" FOREIGN KEY ("RoleId") REFERENCES "Roles"("RoleId");

ALTER TABLE "Rides" ADD CONSTRAINT "Rides_fk0" FOREIGN KEY ("Driver") REFERENCES "Users"("NRIC");

ALTER TABLE "RideBids" ADD CONSTRAINT "RideBids_fk0" FOREIGN KEY ("UserBid") REFERENCES "Users"("NRIC");
ALTER TABLE "RideBids" ADD CONSTRAINT "RideBids_fk1" FOREIGN KEY ("RideId") REFERENCES "Rides"("RideId");
