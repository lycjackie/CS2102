CREATE OR REPLACE FUNCTION on_approval_update_pax()
  RETURNS trigger AS
$BODY$
BEGIN
  IF NEW.status = 'successful' and OLD.STATUS <> 'successful'
  THEN
    UPDATE ride
    SET current_pax = current_pax + NEW.no_pax
    WHERE reg_no = NEW.reg_no
      AND start_time = NEW.start_time;

    UPDATE ride_bid rb
    SET status = 'unsuccessful'
    FROM ride r,
         car c,
         model m
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
$BODY$
LANGUAGE plpgsql;


CREATE TRIGGER approval_update
  AFTER UPDATE
  ON ride_bid
  FOR EACH ROW
EXECUTE PROCEDURE on_approval_update_pax();


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
  before insert OR update
  on ride_bid
  for each row
execute procedure capacity_checker();


create or replace function audit()
  returns trigger
language plpgsql
as $$
BEGIN
  IF NEW.status = 'completed'
  THEN
    INSERT INTO audit_log (start_time, end_time, status, current_pax, destination, origin, reg_no)
    VALUES (OLD.start_time, now(), NEW.status, OLD.current_pax, OLD.destination, OLD.origin, OLD.reg_no);
  --   DELETE FROM ride WHERE origin=OLD.origin AND reg_no=OLD.reg_no;
  END IF;

  RETURN NEW;
END;
$$;

create trigger to_audit
  before update
  on ride
  for each row
execute procedure audit();

-- Note that 
-- Need to run `create extension pgcrypto;` as super user before the function work

CREATE OR REPLACE FUNCTION register(email varchar(256),contact numeric(8),first_name varchar(50), last_name varchar(50),password varchar(256))
	RETURNS BOOLEAN AS $$
	DECLARE
		success BOOLEAN;
		hashPassword varchar(512);
	BEGIN
		SELECT encode(digest($5, 'sha256'), 'hex') INTO hashPassword;
		INSERT INTO "user" VALUES ($1,$2,$3,$4,false ,hashPassword) Returning 1 into success;
		RETURN success;
	END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION login(email varchar(256),password varchar(256))
	RETURNS setof "user" AS $$
	DECLARE
		hashPassword varchar(512);
	BEGIN
		SELECT encode(digest($2, 'sha256'), 'hex') INTO hashPassword;
		RETURN QUERY SELECT * FROM "user" where "user".email = $1 and "user".password = hashPassword;
	END;
$$ LANGUAGE plpgsql;
