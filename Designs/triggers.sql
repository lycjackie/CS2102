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
 END IF;

 RETURN NULL;
END
$BODY$ LANGUAGE plpgsql;


	CREATE TRIGGER approval_update
  AFTER UPDATE
  ON ride_bid
  FOR EACH ROW
  EXECUTE PROCEDURE on_approval_update_pax();


CREATE OR REPLACE FUNCTION capacity_checker()
  RETURNS trigger AS
$func$
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
  RETURN NULL;
     END IF;
END
$func$  LANGUAGE plpgsql;



	CREATE TRIGGER cap_check
  BEFORE INSERT
  ON ride_bid
  FOR EACH ROW
  EXECUTE PROCEDURE capacity_checker();
