INSERT INTO `events_event` (`id`, `name`, `short_description`, `long_description`, `address`, `city`, `state`, `postalzip`, `public`, `category_id`, `start_time`, `end_time`, `list_date`, `owner_id`)
VALUES
	(1, 'Cleveland Food Bank', 'The Cleveland Foodbank works to ensure that everyone in our communities has the nutritious food they need every day.', '<p>Volunteers are crucial to the operation of the Foodbank. Without volunteers, it would not be possible to collect, sort and repack all the food that comes through our warehouse every day. But that\'s not all. Foodbank volunteers also help with administrative tasks, special events, and serve on committees. </p>\n\n<p>In 2011, Over 10,000 volunteers contributed more than 55,000 hours of service to the Foodbank. Their hard work and effort saved us from hiring 26 full time staff & over a million dollars in salaries & benefits, an expense we could not otherwise afford.</p>\n<br />\n<p>Volunteers make our work possible. We hope you\'ll consider joining us. <br/><br/>\nTypes of Volunteer Work Available:<br/><br/>\n\nProduce: We need volunteers to inspect and sort produce donations.<br/><br/>\n\nSpecial Events: We need volunteers to collect leftover perishable food, distribute Cleveland Foodbank literature, or receive donated canned food.<br/><br/>\n\nCleveland Community Kitchen: We need volunteers to help prepare hot meals that are distributed at local hot meal sites.<br/><br/>\n\nSort/Repack Opportunities: We need volunteers to help sort and repack nonperishable food that is later distributed to local food pantries, soup kitchens, and shelters.<br/><br/>\n\nAdministrative Tasks: We need volunteers to help around the office, stuff envelopes and other special projects.<br/><br/>\n\n</p>', '15500 South Waterloo Road', 'Cleveland', 'OH', '44110', 1, 3, '2013-12-10 09:00:00', '2013-12-10 17:00:00', '2013-12-08 15:47:00', 1);


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

CREATE PROCEDURE recommend_events_nested(IN a_user_id INT, IN threshold INT)
BEGIN

SELECT event_id as recommended_event_id FROM (
	(SELECT event1 AS event_id FROM (SELECT tempP.event1 FROM (
SELECT r1.event AS event1, r2.event AS event2
FROM (SELECT user_id AS user, event_id AS event
FROM service_serviceenrollment WHERE event_id IN (
	SELECT event_id FROM service_serviceenrollment GROUP BY event_id HAVING COUNT(*) >= threshold
)) AS r1, (SELECT user_id AS user, event_id AS event
FROM service_serviceenrollment WHERE event_id IN (
	SELECT event_id FROM service_serviceenrollment GROUP BY event_id HAVING COUNT(*) >= threshold
)) AS r2
WHERE r1.user = r2.user
AND r1.event < r2.event
GROUP BY r1.event, r2.event
HAVING COUNT(*) >= threshold) AS tempP
JOIN service_serviceenrollment ON (service_serviceenrollment.event_id = tempP.event1 OR service_serviceenrollment.event_id = tempP.event2 )
WHERE service_serviceenrollment.user_id = a_user_id) AS list1 WHERE
	event1 NOT IN (
		SELECT event_id FROM service_serviceenrollment WHERE user_id = a_user_id
	))
	union
	(SELECT event2 AS event_id FROM (SELECT tempP.event2 FROM (
SELECT r1.event AS event1, r2.event AS event2
FROM (SELECT user_id AS user, event_id AS event
FROM service_serviceenrollment WHERE event_id IN (
	SELECT event_id FROM service_serviceenrollment GROUP BY event_id HAVING COUNT(*) >= threshold
)) AS r1, (SELECT user_id AS user, event_id AS event
FROM service_serviceenrollment WHERE event_id IN (
	SELECT event_id FROM service_serviceenrollment GROUP BY event_id HAVING COUNT(*) >= threshold
)) AS r2
WHERE r1.user = r2.user
AND r1.event < r2.event
GROUP BY r1.event, r2.event
HAVING COUNT(*) >= threshold) AS tempP
JOIN service_serviceenrollment ON (service_serviceenrollment.event_id = tempP.event1 OR service_serviceenrollment.event_id = tempP.event2 )
WHERE service_serviceenrollment.user_id = a_user_id) AS list2 WHERE
	event2 NOT IN (
		SELECT event_id FROM service_serviceenrollment WHERE user_id = a_user_id
	))
) AS final;--

END;
