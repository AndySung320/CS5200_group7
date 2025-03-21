SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Instructor;
DROP TABLE IF EXISTS Admin;
DROP TABLE IF EXISTS Topic;
DROP TABLE IF EXISTS SQLProblem;
DROP TABLE IF EXISTS Attempt;
DROP TABLE IF EXISTS Message;
DROP TABLE IF EXISTS Notification;
DROP TABLE IF EXISTS Comment;
DROP TABLE IF EXISTS LearningAnalytics;
DROP TABLE IF EXISTS Badge;
DROP TABLE IF EXISTS StudentBadge;
DROP TABLE IF EXISTS Hint;
DROP TABLE IF EXISTS UserIndex;


DROP PROCEDURE IF EXISTS AssignBadges;

DROP FUNCTION IF EXISTS CalculateTopicProgress;

DROP TRIGGER IF EXISTS after_user_insert;
DROP TRIGGER IF EXISTS after_message_insert;

DROP VIEW IF EXISTS StudentPerformanceView;
DROP VIEW IF EXISTS ProblemDifficultyStats;

SET FOREIGN_KEY_CHECKS = 1;

