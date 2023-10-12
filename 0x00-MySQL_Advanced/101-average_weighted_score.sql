-- Task: Create a stored procedure to compute and store the average weighted score for all students

DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    -- Declare a variable to store the average weighted score
    DECLARE avg_weighted_score FLOAT;

    -- Calculate the average weighted score for all users
    SELECT SUM(score * weight) / SUM(weight) INTO avg_weighted_score
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id;

    -- Update the average_score for all users
    UPDATE users
    SET average_score = avg_weighted_score;
END;
//
DELIMITER ;
