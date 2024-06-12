-- Task: Create a stored procedure `ComputeAverageScoreForUser` that 
-- computes and stores the average score for a student
-- This script is part of the Back-end SQL MySQL curriculum

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
	DECLARE avg_score FLOAT;

	-- compute the average score
	SELECT AVG(score) INTO avg_score FROM corrections WHERE user_id = user_id;

	-- store the average score in the `users` table
	UPDATE users SET average_score = avg_score WHERE id = user_id;

	-- Compute the average and store it into the `users` table directly
	-- UPDATE users
	-- SET average_score = (SELECT AVG(score) FROM corrections WHERE user_id = user_id)
	-- WHERE id = user_id;
END $$

DELIMITER ;
