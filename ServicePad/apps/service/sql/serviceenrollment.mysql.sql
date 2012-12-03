CREATE TRIGGER validate_enrollment_hours
BEFORE INSERT ON service_serviceenrollment
FOR EACH ROW
BEGIN 
	DECLARE event_start datetime;
	DECLARE event_end datetime;
	SELECT start_time, end_time INTO event_start, event_end FROM events_event WHERE id = NEW.event_id;
	IF NEW.start < event_start OR NEW.end > event_end THEN
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Invalid Start/End Time', MYSQL_ERRNO = 1001;
	END IF;
END;