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