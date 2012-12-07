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
