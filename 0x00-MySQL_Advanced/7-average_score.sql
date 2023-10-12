-- Task: Create a stored procedure to compute and store the average score for a student

DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE avg_score DECIMAL(10, 2);
    
    -- Calculate the average score for the user
    SELECT AVG(score) INTO avg_score
    FROM student_scores
    WHERE student_id = user_id;
    
    -- Check if a record already exists for the user
    IF EXISTS (SELECT 1 FROM user_average_scores WHERE user_id = user_id) THEN
        -- Update the existing record with the new average score
        UPDATE user_average_scores
        SET average_score = avg_score
        WHERE user_id = user_id;
    ELSE
        -- Insert a new record with the average score
        INSERT INTO user_average_scores (user_id, average_score)
        VALUES (user_id, avg_score);
    END IF;
END;
//
DELIMITER ;
