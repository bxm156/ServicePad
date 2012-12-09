INSERT INTO `auth_user` (`id`, `username`, `first_name`, `last_name`, `email`, `password`, `is_staff`, `is_active`, `is_superuser`, `last_login`, `date_joined`)
VALUES
	(1, 'bxm156', 'Bryan', 'Marty', 'bryan.marty@case.edu', '!', 0, 1, 0, '2012-12-08 15:32:45', '2012-12-07 18:22:16');
INSERT INTO `auth_user` (`id`, `username`, `first_name`, `last_name`, `email`, `password`, `is_staff`, `is_active`, `is_superuser`, `last_login`, `date_joined`)
VALUES
	(2, 'kwr17', 'Kevin', 'Rossoll', 'kevin.rossoll@case.edu', '!', 0, 1, 0, '2012-12-08 21:34:01', '2012-12-08 21:33:59');
INSERT INTO `account_userprofile` (`account_type`, `gender`, `ethnicity`, `major`, `graduating_class`, `address`, `city`, `state`, `postalzip`, `authentication`, `user_id`, `organization_name`, `organization_address`, `organization_city`, `organization_state`, `organization_postalzip`, `organization_phone`)
VALUES
	(0, 'm', 'w', 'Computer Engineering', '12', '4917 Pine Ridge Dr.', 'Wootser', 'OH', '44691', 1, 1, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `account_userprofile` (`account_type`, `gender`, `ethnicity`, `major`, `graduating_class`, `address`, `city`, `state`, `postalzip`, `authentication`, `user_id`, `organization_name`, `organization_address`, `organization_city`, `organization_state`, `organization_postalzip`, `organization_phone`)
VALUES
	(0, 'm', 'w', 'English', '13', 'Carlton Rd.', 'Cleveland Heights', 'Oh', '44106', 1, 2, NULL, NULL, NULL, NULL, NULL, NULL);
CREATE PROCEDURE delete_user(IN user_id INT)
BEGIN
	UPDATE auth_user SET is_active='0' WHERE id = user_id; --
END;

CREATE TRIGGER prevent_user_deletion
BEFORE DELETE ON auth_user
FOR EACH ROW
BEGIN
	CALL delete_user(OLD.id); --
	SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = "DELETE operation not allowed. Use the stored procedue: delete_user(user_id)"; --
END;

CREATE TRIGGER validate_profile
BEFORE INSERT ON account_userprofile
FOR EACH ROW
BEGIN
IF NEW.account_type = 0 THEN
	IF NEW.gender IS NULL OR NEW.ethnicity IS NULL THEN
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = "Please supply both gender and ethnicity", MYSQL_ERRNO = 1001; --
	END IF; --
END IF; --
IF NEW.account_type = 1 THEN
	IF NEW.organization_name IS NULL OR NEW.organization_address IS NULL OR NEW.organization_city IS NULL
	OR NEW.organization_state IS NULL or NEW.organization_postalzip IS NULL OR NEW.organization_phone IS NULL
	THEN
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = "Please supply all organization information", MYSQL_ERRNO = 1001; --
	END IF; --
END IF; --
END;
