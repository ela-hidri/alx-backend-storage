-- creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE avg_score FLOAT;

    SET avg_score = (SELECT SUM(c.score * p.weight) / SUM(p.weight) 
    FROM projects as p, corrections  as c
    WHERE c.user_id = user_id 
    AND p.id = c.project_id);
    UPDATE users SET average_score = avg_score WHERE id=user_id;
END;
//
DELIMITER ;
