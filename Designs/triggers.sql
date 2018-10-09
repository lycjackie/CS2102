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
