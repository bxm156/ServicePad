INSERT INTO `auth_user` (`id`, `username`, `first_name`, `last_name`, `email`, `password`, `is_staff`, `is_active`, `is_superuser`, `last_login`, `date_joined`)
VALUES
	(1, 'bxm156', 'Bryan', 'Marty', 'bryan.marty@case.edu', '!', 0, 1, 0, '2012-12-08 15:32:45', '2012-12-07 18:22:16');
INSERT INTO `auth_user` (`id`, `username`, `first_name`, `last_name`, `email`, `password`, `is_staff`, `is_active`, `is_superuser`, `last_login`, `date_joined`)
VALUES
	(2, 'kwr17', 'Kevin', 'Rossoll', 'kevin.rossoll@case.edu', '!', 0, 1, 0, '2012-12-08 21:34:01', '2012-12-08 21:33:59');
INSERT INTO `auth_user` (`id`, `username`, `first_name`, `last_name`, `email`, `password`, `is_staff`, `is_active`, `is_superuser`, `last_login`, `date_joined`)
VALUES
	(3, 'oab7', 'Owen', 'Bell', 'owen.bell@case.edu', '!', 0, 1, 0, '2012-12-09 13:41:08', '2012-12-09 13:41:06');
INSERT INTO `auth_user` (`id`, `username`, `first_name`, `last_name`, `email`, `password`, `is_staff`, `is_active`, `is_superuser`, `last_login`, `date_joined`)
VALUES
	(4, 'mal135', 'Mikala', 'Little', 'mikala.little@case.edu', '!', 0, 1, 0, '2012-12-09 16:57:25', '2012-12-09 16:57:25');




INSERT INTO `auth_user` (`id`, `username`, `first_name`, `last_name`, `email`, `password`, `is_staff`, `is_active`, `is_superuser`, `last_login`, `date_joined`)
VALUES
	(5, 'org1@mailinator.com', 'Jane', 'Robinson', 'org1@mailinator.com', 'pbkdf2_sha256$10000$wZjsZqJEjK2d$7JXQSK6KA2OJCf8LNV7DMF0SZxCntZYf8hY5SFENO38=', 0, 1, 0, '2012-12-10 03:44:09', '2012-12-10 03:43:42');
INSERT INTO `auth_user` (`id`, `username`, `first_name`, `last_name`, `email`, `password`, `is_staff`, `is_active`, `is_superuser`, `last_login`, `date_joined`)
VALUES
	(6, 'org2@mailinator.com', 'Charlie', 'Checker', 'org2@mailinator.com', 'pbkdf2_sha256$10000$s0DcvKiH2yva$R9Ddr20wZEd2jXnkSdUfy4DE/P0zLzYxkslZe7xMuEQ=', 0, 1, 0, '2012-12-10 03:49:50', '2012-12-10 03:49:27');
INSERT INTO `auth_user` (`id`, `username`, `first_name`, `last_name`, `email`, `password`, `is_staff`, `is_active`, `is_superuser`, `last_login`, `date_joined`)
VALUES
	(7, 'org3@mailinator.com', 'Alice', 'Abramson', 'org3@mailinator.com', 'pbkdf2_sha256$10000$i8atxzpyWGtR$jY8DxGk5BUhMziTpMdl655Ag8fZLUALSyMYZ2OJrpZY=', 0, 1, 0, '2012-12-10 03:58:27', '2012-12-10 03:58:06');



INSERT INTO `auth_user` (`id`, `username`, `first_name`, `last_name`, `email`, `password`, `is_staff`, `is_active`, `is_superuser`, `last_login`, `date_joined`)
VALUES
	(8, 'vol1@mailinator.com', 'Jim', 'Slim', 'vol1@mailinator.com', 'pbkdf2_sha256$10000$fp8wAm9QZexu$mZu0M8Ah/zQ9gW2ypSHFesAjy7t5J7X3Ig24CAQTK20=', 0, 1, 0, '2012-12-10 04:01:55', '2012-12-10 04:01:27');
INSERT INTO `auth_user` (`id`, `username`, `first_name`, `last_name`, `email`, `password`, `is_staff`, `is_active`, `is_superuser`, `last_login`, `date_joined`)
VALUES
	(9, 'vol2@mailinator.com', 'Mary', 'Berry', 'vol2@mailinator.com', 'pbkdf2_sha256$10000$wYVWAX25AZlH$oERSU6ZJGMHfZhbfZPdzzWlJs+w+IaFYm1HFTIb6FqU=', 0, 1, 0, '2012-12-10 04:04:17', '2012-12-10 04:03:53');
INSERT INTO `auth_user` (`id`, `username`, `first_name`, `last_name`, `email`, `password`, `is_staff`, `is_active`, `is_superuser`, `last_login`, `date_joined`)
VALUES
	(10, 'vol3@mailinator.com', 'Charles', 'Blarles', 'vol3@mailinator.com', 'pbkdf2_sha256$10000$xlmRKqbnZclN$x40I8kjsGUhu75xVCWXpfj98Z3aCorrVwAf17P+Xelo=', 0, 1, 0, '2012-12-10 04:07:24', '2012-12-10 04:07:24');



INSERT INTO `account_userprofile` (`account_type`, `gender`, `ethnicity`, `major`, `graduating_class`, `address`, `city`, `state`, `postalzip`, `authentication`, `user_id`, `organization_name`, `organization_address`, `organization_city`, `organization_state`, `organization_postalzip`, `organization_phone`)
VALUES
	(0, 'm', 'w', 'Computer Engineering', '12', '4917 Pine Ridge Dr.', 'Wootser', 'OH', '44691', 1, 1, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `account_userprofile` (`account_type`, `gender`, `ethnicity`, `major`, `graduating_class`, `address`, `city`, `state`, `postalzip`, `authentication`, `user_id`, `organization_name`, `organization_address`, `organization_city`, `organization_state`, `organization_postalzip`, `organization_phone`)
VALUES
	(0, 'm', 'w', 'English', '13', 'Carlton Rd.', 'Cleveland Heights', 'Oh', '44106', 1, 2, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `account_userprofile` (`account_type`, `gender`, `ethnicity`, `major`, `graduating_class`, `address`, `city`, `state`, `postalzip`, `authentication`, `user_id`, `organization_name`, `organization_address`, `organization_city`, `organization_state`, `organization_postalzip`, `organization_phone`)
VALUES
	(0, 'm', 'w', 'English, CS', '13', '11909 Carlton Rd', 'Cleveland', 'OH', '44106', 1, 3, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `account_userprofile` (`account_type`, `gender`, `ethnicity`, `major`, `graduating_class`, `address`, `city`, `state`, `postalzip`, `authentication`, `user_id`, `organization_name`, `organization_address`, `organization_city`, `organization_state`, `organization_postalzip`, `organization_phone`)
VALUES
	(0, 'm', 'w', 'Computer Science', '13', '844 NW 193rd St', 'Shoreline', 'Wa', '98177', 1, 4, NULL, NULL, NULL, NULL, NULL, NULL);



INSERT INTO `account_userprofile` (`account_type`, `gender`, `ethnicity`, `major`, `graduating_class`, `address`, `city`, `state`, `postalzip`, `authentication`, `user_id`, `organization_name`, `organization_address`, `organization_city`, `organization_state`, `organization_postalzip`, `organization_phone`)
VALUES
	(1, 'na', 'w', NULL, NULL, '137 Fun Dr.', 'Cleveland', 'OH', '44106', 1, 5, 'Jane\'s Jungle Gyms for Juveniles', '7423 Play Rd.', 'Cleveland', 'OH', '44106', '2165556326');
INSERT INTO `account_userprofile` (`account_type`, `gender`, `ethnicity`, `major`, `graduating_class`, `address`, `city`, `state`, `postalzip`, `authentication`, `user_id`, `organization_name`, `organization_address`, `organization_city`, `organization_state`, `organization_postalzip`, `organization_phone`)
VALUES
	(1, 'na', 'w', NULL, NULL, '16 Melt Rd.', 'Lakewood', 'OH', '44107', 1, 6, 'Charlie\'s Chocolate Challenges', '3023 Cocoa Dr.', 'Bay Village', 'OH', '44140', '2165559000');
INSERT INTO `account_userprofile` (`account_type`, `gender`, `ethnicity`, `major`, `graduating_class`, `address`, `city`, `state`, `postalzip`, `authentication`, `user_id`, `organization_name`, `organization_address`, `organization_city`, `organization_state`, `organization_postalzip`, `organization_phone`)
VALUES
	(1, 'na', 'w', NULL, NULL, '5436 Dark Dr.', 'Beachwood', 'OH', '44122', 1, 7, 'Alice\'s Alliterative Architecture', '253 Round Rd.', 'Beachwood', 'OH', '44122', '2165559874');


INSERT INTO `account_userprofile` (`account_type`, `gender`, `ethnicity`, `major`, `graduating_class`, `address`, `city`, `state`, `postalzip`, `authentication`, `user_id`, `organization_name`, `organization_address`, `organization_city`, `organization_state`, `organization_postalzip`, `organization_phone`)
VALUES
	(0, 'm', 'oth', 'Nutrition', '15', '11914 Juniper Rd.', 'Cleveland', 'OH', '44106', 1, 8, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `account_userprofile` (`account_type`, `gender`, `ethnicity`, `major`, `graduating_class`, `address`, `city`, `state`, `postalzip`, `authentication`, `user_id`, `organization_name`, `organization_address`, `organization_city`, `organization_state`, `organization_postalzip`, `organization_phone`)
VALUES
	(0, 'f', 'w', 'Classics', '14', '2520 Overlook Rd.', 'Cleveland Heights', 'OH', '44106', 1, 9, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `account_userprofile` (`account_type`, `gender`, `ethnicity`, `major`, `graduating_class`, `address`, `city`, `state`, `postalzip`, `authentication`, `user_id`, `organization_name`, `organization_address`, `organization_city`, `organization_state`, `organization_postalzip`, `organization_phone`)
VALUES
	(0, 'm', 'w', 'Materials Science', '16', '5323 Rarles Rd.', 'Bay Village', 'OH', '44140', 1, 10, NULL, NULL, NULL, NULL, NULL, NULL);




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
