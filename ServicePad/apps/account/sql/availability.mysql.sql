INSERT INTO `account_availability` (`id`, `user_id`, `start`, `end`)
VALUES
	(6, 2, '08:00:00', '11:00:00'),
	(1, 8, '17:00:00', '21:00:00'),
	(4, 9, '11:30:00', '13:45:00'),
	(5, 9, '17:00:00', '21:00:00'),
	(2, 10, '09:00:00', '13:00:00'),
	(3, 10, '15:00:00', '19:00:00');

CREATE TRIGGER validate_availability_start_end
BEFORE INSERT ON account_availability
FOR EACH ROW
BEGIN
	IF NEW.start >= NEW.end THEN
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = "Invalid Interval", MYSQL_ERRNO = 1001; --
	END IF; --
END; --