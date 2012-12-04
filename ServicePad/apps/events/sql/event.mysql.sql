CREATE TRIGGER validate_event_start_end
BEFORE INSERT ON events_event
FOR EACH ROW
BEGIN
	IF NEW.start_time >= NEW.end_time THEN
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = "Invalid Interval", MYSQL_ERRNO = 1001; --
	END IF; --
END; --