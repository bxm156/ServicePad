CREATE TRIGGER validate_record_hours
BEFORE INSERT ON service_servicerecord
FOR EACH ROW
BEGIN 
	DECLARE event_start datetime; --
	DECLARE event_end datetime; --
	SELECT start_time, end_time INTO event_start, event_end FROM events_event WHERE id = NEW.event_id; --
	IF NEW.start < event_start OR NEW.end > event_end OR NEW.start > NEW.end THEN
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Invalid Start/End Time', MYSQL_ERRNO = 1001; --
	END IF; --
	SET NEW.hours = TIMESTAMPDIFF(SECOND,NEW.start,NEW.end) / 60 /60 ; --
END; 
