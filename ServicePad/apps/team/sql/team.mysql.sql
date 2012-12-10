INSERT INTO `team_team` (`id`, `name`, `join_date`, `admin_id`)
VALUES
	(1, 'PKT', '2012-12-09 16:10:45', 1),
	(2, 'Workaholics', '2012-12-10 04:34:08', 8),
	(3, 'Prime Rhyme', '2012-12-10 04:35:23', 2);

CREATE TRIGGER enroll_admin_into_team
AFTER INSERT ON team_team
FOR EACH ROW
BEGIN 
INSERT INTO team_teammembership (member_id,team_id,join_date,invite) VALUES (NEW.admin_id,NEW.id,NEW.JOIN_DATE,0); --
END;