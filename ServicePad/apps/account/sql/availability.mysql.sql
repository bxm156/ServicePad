CREATE TRIGGER validate_availability_start_end
BEFORE INSERT ON account_availability
FOR EACH ROW
BEGIN
	IF NEW.start >= NEW.end THEN
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = "Invalid Interval", MYSQL_ERRNO = 1001; --
	END IF; --
END; --