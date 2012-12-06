CREATE TRIGGER validate_event_start_end
BEFORE INSERT ON events_event
FOR EACH ROW
BEGIN
	IF NEW.start_time >= NEW.end_time THEN
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = "Invalid Interval", MYSQL_ERRNO = 1001; --
	END IF; --
END;

CREATE PROCEDURE recommend_events(IN a_user_id INT, IN threshold INT)
BEGIN
CREATE TABLE related (
	user int(11) NOT NULL,
	event int(11) NOT NULL
);--

INSERT INTO related (user, event)
SELECT user_id, event_id
FROM service_serviceenrollment WHERE event_id IN (
	SELECT event_id FROM service_serviceenrollment GROUP BY event_id HAVING COUNT(*) >= threshold
);--

CREATE TABLE user_event_list (
	event1 int(11) NOT NULL,
	event2 int(11) NOT NULL
);--

INSERT INTO user_event_list (event1, event2)
SELECT tempP.event1, tempP.event2 FROM (
SELECT r1.event AS event1, r2.event AS event2
FROM related r1, related r2
WHERE r1.user = r2.user
AND r1.event < r2.event
GROUP BY r1.event, r2.event
HAVING COUNT(*) >= threshold) AS tempP
JOIN service_serviceenrollment ON (service_serviceenrollment.event_id = tempP.event1 OR service_serviceenrollment.event_id = tempP.event2 )
WHERE service_serviceenrollment.user_id = a_user_id;--


SELECT event_id as recommended_event_id FROM (
	(SELECT event1 AS event_id FROM user_event_list WHERE
	event1 NOT IN (
		SELECT event_id FROM service_serviceenrollment WHERE user_id = a_user_id
	))
	union
	(SELECT event2 AS event_id FROM user_event_list WHERE
	event2 NOT IN (
		SELECT event_id FROM service_serviceenrollment WHERE user_id = a_user_id
	))
) AS final;--

DROP TABLE related;--
DROP TABLE user_event_list;--

END;