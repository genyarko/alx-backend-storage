-- Task: Create a stored procedure to compute and store the average weighted score for a student

DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE weighted_avg FLOAT;
    
    -- Calculate the weighted average score for the user
    SELECT SUM(score * weight) / SUM(weight) INTO weighted_avg
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE user_id = user_id;
    
    -- Update the user's average score
    UPDATE users
    SET average_score = weighted_avg
    WHERE id = user_id;
END;
//
DELIMITER ;
