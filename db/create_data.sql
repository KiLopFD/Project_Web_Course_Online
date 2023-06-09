-- Insert five tuples into the users table
INSERT INTO users (user_id, username, email, password, created_at, updated_at)
VALUES 
    (1, 'john', 'john@example.com', '123', '2022-01-01', NULL),
    (2, 'jane', 'jane@example.com', '123', '2022-01-01', NULL),
    (3, 'bob', 'bob@example.com', '123', '2022-01-01', NULL),
    (4, 'alice', 'alice@example.com', '123', '2022-01-01', NULL),
    (5, 'sam', 'sam@example.com', '123', '2022-01-01', NULL);

-- Insert five tuples into the roles table
INSERT INTO roles (role_id, role_name)
VALUES 
    (0, 'admin'),
    (1, 'user');

-- Insert five tuples into the users_roles table
INSERT INTO users_roles (user_id, role_id)
VALUES 
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 1);

-- Insert five tuples into the payment_status table
INSERT INTO payment_status (payment_status_id, status_name)
VALUES 
    (1, 'pending'),
    (2, 'paid'),
    (3, 'refunded'),
    (4, 'cancelled'),
    (5, 'failed');

-- Insert five tuples into the level_courses table
INSERT INTO level_courses (level_id, level_name)
VALUES 
    (1, 'Beginner'),
    (2, 'Intermediate'),
    (3, 'Advanced'),
    (4, 'Expert'),
    (5, 'Master');

-- Insert five tuples into the courses table
INSERT INTO courses (course_id, title, description, price, instructor, created_at, updated_at, level_id)
VALUES 
    (1, 'Introduction to SQL', 'This course provides an introduction to SQL.', 49.99, 'John Doe', '2022-01-01', NULL, 1),
    (2, 'Advanced SQL', 'This course covers advanced topics in SQL.', 99.99, 'Jane Smith', '2022-01-01', NULL, 3),
    (3, 'Database Design', 'This course covers database design concepts.', 79.99, 'Bob Johnson', '2022-01-01', NULL, 2),
    (4, 'Data Analysis', 'This course covers data analysis techniques.', 149.99, 'Alice Lee', '2022-01-01', NULL, 4),
    (5, 'Business Intelligence', 'This course covers business intelligence concepts.', 199.99, 'Sam Wilson', '2022-01-01', NULL, 5);



-- Insert 5 tuples into categories table
INSERT INTO categories (category_id, category_name)
VALUES (1, 'Programming'),
(2, 'SQL'),
(3, 'Design'),
(4, 'Big Data'),
(5, 'AI');

-- Insert 5 tuples into course_categories table
INSERT INTO course_categories (course_id, category_id)
VALUES (1, 1),
(1, 2),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

-- Budget
INSERT INTO budget (budget_id, user_id, amount, start_date, end_date)
VALUES
(1, 1, 1000.00, '2023-05-01', '3000-01-01 00:00:00.000'),
(2, 2, 2000.00, '2023-05-01', '3000-01-01 00:00:00.000'),
(3, 3, 3000.00, '2023-05-01', '3000-01-01 00:00:00.000'),
(4, 4, 4000.00, '2023-05-01', '3000-01-01 00:00:00.000'),
(5, 5, 5000.00, '2023-05-01', '3000-01-01 00:00:00.000');