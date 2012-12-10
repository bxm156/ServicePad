INSERT INTO `service_servicerecord` (`id`, `user_id`, `team_id`, `event_id`, `start`, `end`, `hours`, `rating`, `review`, `attended`)
VALUES
	(1, 1, 1, 6, '2012-12-10 03:00:00', '2012-12-10 06:00:00', 3.00, 5, 'He built an entire house while the rest of us ate lunch.', 1),
	(2, 3, 1, 6, '2012-12-10 03:00:00', '2012-12-10 06:00:00', 3.00, 1, 'Owen just ate lunch. Very disappointing...', 1),
	(3, 2, 3, 1, '2012-12-10 09:00:00', '2012-12-10 11:00:00', 2.00, 3, 'He ate most of the food.', 1),
	(4, 9, NULL, 1, '2012-12-10 09:00:00', '2012-12-10 12:00:00', 3.00, 5, 'Good Helper, didn\'t complain when the eggplant went 8bit.', 1);


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
