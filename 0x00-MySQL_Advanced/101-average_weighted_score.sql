-- Task: Create a stored procedure `ComputeAverageWeightedScoreForUsers` that 
-- computes and stores the average weighted score for all students.
-- This script is part of the Back-end SQL MySQL curriculum.

DELIMITER $$
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	-- hold the user_id of each user 
	DECLARE user_id INT;

	-- cursor for all users 
	DECLARE cur CURSOR FOR SELECT id FROM users;

	-- CONTINUE handler, will be invoked when the cursor runs out of rows
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET @done = TRUE;

	OPEN cur;

	-- start
	read_loop: LOOP 
		-- fetch the next user_id
		FETCH cur INTO user_id;

		IF @done THEN
			LEAVE read_loop;
		END IF;

		-- Compute the average weighted score for the current user and store it
		UPDATE users
		SET average_score = (
			SELECT SUM(c.score * p.weight) / SUM(p.weight)
			FROM corrections c 
			JOIN projects p ON c.project_id = p.id 
			WHERE c.user_id = user_id
		)
		WHERE id = user_id;
	END LOOP;

	CLOSE cur;
END;$$
DELIMITER ;
