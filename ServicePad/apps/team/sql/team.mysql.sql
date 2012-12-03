CREATE TRIGGER enroll_admin_into_team
AFTER INSERT ON team_team
FOR EACH ROW
BEGIN 
INSERT INTO team_teammembership (member_id,team_id,join_date,invite) VALUES (NEW.admin_id,NEW.id,NEW.JOIN_DATE,0); --
END; --