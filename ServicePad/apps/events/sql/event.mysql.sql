INSERT INTO `events_event` (`id`, `name`, `short_description`, `long_description`, `address`, `city`, `state`, `postalzip`, `public`, `category_id`, `start_time`, `end_time`, `list_date`, `owner_id`)
VALUES
	(1, 'Cleveland Food Bank', 'The Cleveland Foodbank works to ensure that everyone in our communities has the nutritious food they need every day.', '<p>Volunteers are crucial to the operation of the Foodbank. Without volunteers, it would not be possible to collect, sort and repack all the food that comes through our warehouse every day. But that\'s not all. Foodbank volunteers also help with administrative tasks, special events, and serve on committees. </p>\r\n\r\n<p>In 2011, Over 10,000 volunteers contributed more than 55,000 hours of service to the Foodbank. Their hard work and effort saved us from hiring 26 full time staff & over a million dollars in salaries & benefits, an expense we could not otherwise afford.</p>\r\n<br />\r\n<p>Volunteers make our work possible. We hope you\'ll consider joining us. <br/><br/>\r\nTypes of Volunteer Work Available:<br/><br/>\r\n\r\nProduce: We need volunteers to inspect and sort produce donations.<br/><br/>\r\n\r\nSpecial Events: We need volunteers to collect leftover perishable food, distribute Cleveland Foodbank literature, or receive donated canned food.<br/><br/>\r\n\r\nCleveland Community Kitchen: We need volunteers to help prepare hot meals that are distributed at local hot meal sites.<br/><br/>\r\n\r\nSort/Repack Opportunities: We need volunteers to help sort and repack nonperishable food that is later distributed to local food pantries, soup kitchens, and shelters.<br/><br/>\r\n\r\nAdministrative Tasks: We need volunteers to help around the office, stuff envelopes and other special projects.<br/><br/>\r\n\r\n</p>', '15500 South Waterloo Road', 'Cleveland', 'OH', '44110', 1, 3, '2012-12-10 09:00:00', '2012-12-10 17:00:00', '2012-12-08 15:47:00', 5),
	(2, 'Database Tutoring', 'Teach the young about databases', 'Shaker Elementary is looking for someone knowledgable in database design to teach our 1st grade class. The commitment will be one hour every week. All applicants must be good with kids.', '2625 Shaker Rd', 'Cleveland', 'OH', '44118', 1, 7, '2012-02-09 10:00:00', '2012-02-13 13:00:00', '2012-12-08 13:51:04', 6),
	(3, 'Dog Shelter', 'Walk dogs!', 'The Cuyahoga County Animal Shelter needs your help. We have dozens of dogs that need exercise but not enough people to walk them. Donate a few hours of your time and help our dogs get outside and enjoy themselves.', '9500 Sweet Valley Dr.', 'Cleveland', 'OH', '44125', 1, 1, '2012-01-15 10:00:00', '2012-01-15 12:00:00', '2012-12-09 13:58:11', 7),
	(4, 'Wade Lagoon Cleanup', 'Make Cleveland beautiful', 'Come out and help pickup trash to help keep the Wade Lagoon a beautiful part of Cleveland.', 'Martin Luther King Jr Dr & Euclid Ave', 'Cleveland', 'OH', '44106', 1, 6, '2012-12-01 14:00:00', '2012-12-25 16:30:00', '2012-11-20 14:03:44', 5),
	(5, 'Thanksgiving with the Homeless', 'Help those less fortunate on Thanksgiving', 'We need volunteers to help us cook and serve Thanksgiving dinner at the Salvation Army.', '4139 East 93rd Street', 'Cleveland', 'OH', '44105', 1, 3, '2012-11-22 11:00:00', '2012-11-22 13:00:00', '2012-12-09 14:50:13', 6),
	(6, 'Habitat for Humanity', 'Build houses!', 'We need able and helping hands to build homes for those without. No prior building experience needed. We\'ll teach you everything you need to know.', '4000 Euclid Ave', 'Cleveland', 'OH', '44107', 1, 9, '2012-01-01 09:00:00', '2013-01-01 20:00:00', '2012-01-01 01:52:36', 7),
	(7, 'Broadview Game Night', 'Play games with our residents', 'It\'s time for Broadview Multi-Care Center\'s Game Night! Come play games with our residents. Fun will be had by all.', '5520 Broadview Rd', 'Parma', 'OH', '44134', 1, 5, '2012-12-10 17:00:00', '2012-12-10 22:00:00', '2012-12-09 16:04:10', 5),
	(9, 'Feed Cuthulu', 'Cuthulu has hunger', 'Come mortals and bow before the elder god', 'insanity', 'R\'lyeh', 'OR', '99999', 1, 9, '2020-12-20 12:00:00', '2020-12-20 16:00:00', '2012-12-09 19:04:50', 6);

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
