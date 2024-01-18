-- creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users
SET average_score = (
    SELECT AVG(weighted_score)
    FROM (
        SELECT SUM(c.score * p.weight) / SUM(p.weight) AS weighted_score
        FROM projects AS p
        JOIN corrections AS c ON p.id = c.project_id
        WHERE c.user_id = users.id
        GROUP BY c.user_id
    ) AS user_scores
);
END;
//
DELIMITER ;
