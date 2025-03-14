-- Insert data into User table
INSERT INTO User (name, email, password, profile_info, last_login, role, registration_date) VALUES
('Alice Johnson', 'alice@email.com', 'hashed_password_1', 'Passionate about SQL.', '2024-03-10 12:30:00', 'Student', '2024-02-01'),
('Bob Smith', 'bob@email.com', 'hashed_password_2', 'Expert in database management.', '2024-03-11 15:20:00', 'Instructor', '2024-01-15'),
('Charlie Brown', 'charlie@email.com', 'hashed_password_3', 'Backend developer specializing in SQL optimization.', '2024-03-12 09:15:00', 'Instructor', '2023-12-20'),
('David Miller', 'david@email.com', 'hashed_password_4', 'System administrator for SQL platforms.', '2024-03-13 10:45:00', 'Admin', '2023-11-10'),
('Emma Watson', 'emma@email.com', 'hashed_password_5', 'Data analyst focusing on big data.', '2024-03-14 18:00:00', 'Student', '2024-02-05'),
('Frank Thomas', 'frank@email.com', 'hashed_password_6', 'Full-stack developer.', '2024-03-15 21:10:00', 'Student', '2024-02-10'),
('Grace Hopper', 'grace@email.com', 'hashed_password_7', 'Legendary computer scientist.', '2024-03-16 08:25:00', 'Admin', '2023-10-05');

-- Insert data into Student table (Student ID must match User ID)
INSERT INTO Student (student_id) VALUES
(1),
(5),
(6);

-- Insert data into Instructor table (Instructor ID must match User ID)
INSERT INTO Instructor (instructor_id, department) VALUES
(2, 'Computer Science'),
(3, 'Information Technology');

-- Insert data into Admin table (Admin ID must match User ID)
INSERT INTO Admin (admin_id, access_level, department) VALUES
(4, 'SuperAdmin', 'System Administration'),
(7, 'Moderator', 'Platform Support');

-- Insert data into Topic table
INSERT INTO Topic (name, description) VALUES
('SQL Joins', 'Understanding INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL JOIN.'),
('Aggregation Functions', 'Using GROUP BY, SUM, AVG, COUNT, MIN, and MAX.'),
('Indexes & Performance', 'How indexing affects performance in SQL queries.'),
('Stored Procedures', 'Writing and executing stored procedures in SQL.');

-- Insert data into SQLProblem table
INSERT INTO SQLProblem (title, description, difficulty_level, topic_id) VALUES
('Find Active Users', 'Write an SQL query to find users who logged in within the last 7 days.', 'Easy', 1),
('Top Selling Products', 'Get the top 3 best-selling products from the sales table.', 'Medium', 2),
('Optimize Queries', 'Identify and optimize slow SQL queries in logs.', 'Hard', 3),
('Stored Procedure Task', 'Write a stored procedure to insert new employees.', 'Expert', 4);

-- Insert data into Attempt table
INSERT INTO Attempt (student_id, problem_id, submission_date, score, time_taken, status, hints_used) VALUES
(1, 1, '2024-03-10 14:00:00', 85.50, 120, 'Completed', 1),
(5, 2, '2024-03-11 16:30:00', 92.00, 150, 'Completed', 0),
(6, 3, '2024-03-12 10:15:00', 45.75, 200, 'Failed', 2),
(1, 4, '2024-03-13 18:45:00', 80.00, 300, 'Completed', 1);

-- Insert data into Message table
INSERT INTO Message (sender_id, receiver_id, message_content, is_read, timestamp) VALUES
(2, 1, 'Please review the SQL joins lesson.', FALSE, '2024-03-10 14:30:00'),
(3, 5, 'Great job on the database optimization task!', TRUE, '2024-03-12 17:45:00'),
(4, 6, 'Your SQL problem submission has been reviewed.', FALSE, '2024-03-14 09:15:00');

-- Insert data into Notification table
INSERT INTO Notification (receiver_id, content, is_read, timestamp, comment_message) VALUES
(1, 'New SQL challenge available!', FALSE, '2024-03-10 10:00:00', FALSE),
(5, 'Your attempt on the SQL problem has been graded.', TRUE, '2024-03-11 18:45:00', TRUE),
(6, 'Reminder: Complete the database indexing lesson.', FALSE, '2024-03-13 08:00:00', FALSE);

-- Insert data into Comment table
INSERT INTO Comment (problem_id, user_id, content, timestamp) VALUES
(1, 1, 'This problem was really helpful!', '2024-03-10 16:00:00'),
(2, 5, 'I found the GROUP BY concept a bit tricky.', '2024-03-12 20:15:00'),
(3, 6, 'Indexes made my queries much faster!', '2024-03-14 11:30:00');


INSERT INTO LearningAnalytics (student_id, problem_id, error_frequency, time_spent, completion_status) VALUES
(1, 1, 2, 120, 'Completed'),
(5, 2, 0, 150, 'Completed'),
(6, 3, 5, 200, 'Abandoned');  

-- Insert data into Badge table
INSERT INTO Badge (name, criteria, icon) VALUES
('SQL Beginner', 'Complete 3 easy SQL problems.', 'beginner.png'),
('SQL Master', 'Solve all hard SQL problems.', 'master.png'),
('Performance Guru', 'Optimize at least 5 queries.', 'guru.png');

-- Insert data into StudentBadge table
INSERT INTO StudentBadge (student_id, badge_id, earned_date) VALUES
(1, 1, '2024-03-10 17:00:00'),
(5, 2, '2024-03-11 19:00:00'),
(6, 3, '2024-03-12 12:30:00');