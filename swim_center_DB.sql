CREATE DATABASE swim_center_db;
use swim_center_db;




CREATE TABLE Users (
	user_id INT PRIMARY KEY AUTO_INCREMENT,
    password VARCHAR(255) NOT NULL,
	username VARCHAR(100) NOT NULL,
	role VARCHAR(50) NOT NULL
 );
 
INSERT INTO Users (password, username, role)
VALUES
    ('$2b$12$s0yeYt193oY9mjXCP/3Kkur18lqHj5qJ5R6fkUJ9Z6lMlNkCtILDW', 'admin1', 'admin'),
    ('$2b$12$3iC2ApFUp8kjl7juKyQB3.oQ9DuPznfjrKlYYhaHykSJLzvC.0sWC', 'admin2', 'admin'),
    ('password3', 'admin3', 'admin'),
    ('$2b$12$IiwCxCD2.BPxqdH5KUbmZeNtYHEt/67Gf66TBSvhr1hNkLn2KKgPa', 'instructor1', 'instructor'),
    ('$2b$12$gsZn1joOSTwlqZEZ9GxEWuGSUlx1k4j.KLLlqaLQrqDY1z65.oLuy', 'instructor2', 'instructor'),
    ('password6', 'instructor3', 'instructor'),
    ('password7', 'instructor4', 'instructor'),
    ('password8', 'instructor5', 'instructor'),
    ('password9', 'instructor6', 'instructor'),
    ('password10', 'instructor7', 'instructor'),
    ('password11', 'instructor8', 'instructor'),
    ('password12', 'instructor9', 'instructor'),
    ('password13', 'instructor10', 'instructor'),
    ('$2b$12$jb3irSodNbgS.LXXFGw48.CdcT.d.i2Pvti5aB4iYkBZulYz6kOh6', 'member1', 'member'),
    ('$2b$12$IHzJPqlq/bAGI0hq1RcoMOlc8dt1adiRSpr3H1KeHFGxs25IQRRW6', 'member2', 'member'),
    ('password16', 'member3', 'member'),
    ('password17', 'member4', 'member'),
    ('password18', 'member5', 'member'),
    ('password19', 'member6', 'member'),
    ('password20', 'member7', 'member'),
    ('password21', 'member8', 'member'),
    ('password22', 'member9', 'member'),
    ('password23', 'member10', 'member'),
    ('password24', 'member11', 'member'),
    ('password25', 'member12', 'member'),
    ('password26', 'member13', 'member'),
    ('password27', 'member14', 'member'),
    ('password28', 'member15', 'member'),
    ('password29', 'member16', 'member'),
    ('password30', 'member17', 'member'),
    ('password31', 'member18', 'member'),
    ('password32', 'member19', 'member'),
    ('password33', 'member20', 'member');

 CREATE TABLE Admins (
     admin_id INT PRIMARY KEY AUTO_INCREMENT,
     title VARCHAR(10),
     first_name VARCHAR(100),
     last_name VARCHAR(100),
     position VARCHAR(100),
     phone VARCHAR(20),
     email VARCHAR(255),
     user_id INT,
     FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

INSERT INTO Admins (title, first_name, last_name, position, phone, email, user_id)
VALUES
    ('Mr', 'John', 'Doe', 'Manager', '1234567890', 'john@example.com', 1),
    ('Ms', 'Jane', 'Smith', 'Supervisor', '9876543210', 'jane@example.com', 2),
    ('Dr', 'David', 'Johnson', 'Coordinator', '4567890123', 'david@example.com', 3);



 CREATE TABLE Instructors (
    instructor_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(10),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    position VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(255),
    instructor_profile TEXT,
    user_id INT,
    image_url VARCHAR(255), 
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

INSERT INTO Instructors (title, first_name, last_name, position, phone, email, instructor_profile, user_id, image_url)
VALUES
    ('Mr', 'Michael', 'Williams', 'Senior Instructor', '1111111111', 'michael@example.com', 'Experienced swim instructor', 4, 'static/images/instructors/michael.jpg'),
    ('Ms', 'Jessica', 'Brown', 'Swim Coach', '2222222222', 'jessica@example.com', 'Passionate about teaching swimming', 5, 'static/images/instructors/jessica.jpg'),
    ('Dr', 'Christopher', 'Jones', 'Aquatics Specialist', '3333333333', 'chris@example.com', 'Expert in water safety', 6, 'static/images/instructors/christopher.jpg'),
    ('Mr', 'Daniel', 'Martinez', 'Instructor', '4444444444', 'daniel@example.com', 'Former competitive swimmer', 7, 'static/images/instructors/daniel.jpg'),
    ('Ms', 'Emily', 'Davis', 'Instructor', '5555555555', 'emily@example.com', 'Teaching all skill levels', 8, 'static/images/instructors/emily.jpg'),
    ('Mr', 'John', 'Smith', 'Senior Instructor', '6666666666', 'john@example.com', 'Swim expert with 10+ years of experience', 9, 'static/images/instructors/john.jpg'),
    ('Ms', 'Sarah', 'Johnson', 'Swim Coach', '7777777777', 'sarah@example.com', 'Specializes in teaching children', 10, 'static/images/instructors/sarah.jpg'),
    ('Dr', 'David', 'Wilson', 'Aquatics Specialist', '8888888888', 'david@example.com', 'Certified lifeguard and water safety expert', 11, 'static/images/instructors/david.jpg'),
    ('Mr', 'Olivia', 'Garcia', 'Instructor', '9999999999', 'olivia@example.com', 'Passionate about improving swimming techniques', 12, 'static/images/instructors/olivia.jpg'),
    ('Ms', 'James', 'Brown', 'Instructor', '1010101010', 'james@example.com', 'Enthusiastic swim instructor', 13, 'static/images/instructors/james.jpg');

CREATE TABLE Members (
     member_id INT PRIMARY KEY AUTO_INCREMENT,
     title VARCHAR(10),
     first_name VARCHAR(100),
     last_name VARCHAR(100),
     position VARCHAR(100),
     phone VARCHAR(20),
     email VARCHAR(255),
     address VARCHAR(255),
     birthdate DATE,
     health_info TEXT,
     user_id INT,
     booked_courses TEXT,
     status INT,
     FOREIGN KEY (user_id) REFERENCES Users(user_id)
 );

INSERT INTO Members (title, first_name, last_name, position, phone, email, address, birthdate, health_info, user_id, booked_courses, status)
VALUES
    ('Mr', 'John', 'Smith', 'Student', '1111111111', 'john@example.com', '123 Main St, City', '1990-05-15', 'No known health issues', 14, '1,10,5,9', 1),
    ('Ms', 'Emily', 'Johnson', 'Teacher', '2222222222', 'emily@example.com', '456 Elm St, Town', '1985-08-22', 'Asthma, mild allergies', 15, '', 1),
    ('Dr', 'Michael', 'Williams', 'Doctor', '3333333333', 'michael@example.com', '789 Oak St, Village', '1978-03-10', 'High blood pressure', 16, '', 1),
    ('Mrs', 'Sarah', 'Davis', 'Engineer', '4444444444', 'sarah@example.com', '101 Pine St, Suburb', '1995-11-28', 'No known health issues', 17, '2', 1),
    ('Mr', 'David', 'Martinez', 'Manager', '5555555555', 'david@example.com', '234 Maple St, County', '1982-06-09', 'Lactose intolerance', 18, '', 1),
    ('Ms', 'Jessica', 'Wilson', 'Designer', '6666666666', 'jessica@example.com', '567 Birch St, State', '1998-02-17', 'No known health issues', 19, '2', 1),
    ('Mr', 'James', 'Brown', 'Accountant', '7777777777', 'james@example.com', '890 Cedar St, Province', '1993-09-05', 'Mild back pain', 20, '', 1),
    ('Ms', 'Olivia', 'Miller', 'Writer', '8888888888', 'olivia@example.com', '1234 Oak St, Territory', '1991-07-12', 'Allergic to shellfish', 21, '2', 1),
    ('Mr', 'William', 'Jones', 'Musician', '9999999999', 'william@example.com', '5678 Elm St, Region', '1989-04-30', 'No known health issues', 22, '', 1),
    ('Mrs', 'Sophia', 'Wilson', 'Lawyer', '1010101010', 'sophia@example.com', '4567 Maple St, District', '1987-01-20', 'Gluten sensitivity', 23, '2', 1),
    ('Mr', 'Mason', 'Wilson', 'Lawyer', '5555555555', 'mason@example.com', '789 Elm St, County', '1980-09-28', 'None', 24, '2,9', 1),
    ('Ms', 'Harper', 'Martinez', 'Teacher', '6666666666', 'harper@example.com', '456 Oak St, Town', '1972-01-15', 'Allergic to pollen', 25, '1,7', 1),
    ('Mr', 'Ethan', 'Taylor', 'Doctor', '7777777777', 'ethan@example.com', '567 Birch St, Village', '1993-06-22', 'None', 26, '4,5', 1),
    ('Mrs', 'Sofia', 'Hernandez', 'Nurse', '8888888888', 'sofia@example.com', '345 Pine St, City', '1982-07-08', 'None', 27, '6,10', 1),
    ('Mr', 'Liam', 'Gonzalez', 'Engineer', '9999999999', 'liam@example.com', '123 Cedar St, Suburb', '1994-02-14', 'No known health issues', 28, '2,8', 1),
    ('Miss', 'Aria', 'Lopez', 'Student', '1111111111', 'aria@example.com', '456 Elm St, Town', '2001-12-09', 'No known health issues', 29, '3,9', 1),
    ('Mr', 'Noah', 'Clark', 'Artist', '2222222222', 'noah@example.com', '789 Maple St, Village', '1978-10-17', 'Allergic to cats', 30, '1,4,7', 1),
    ('Ms', 'Emma', 'White', 'Designer', '3333333333', 'emma@example.com', '567 Oak St, County', '1996-04-03', 'No known health issues', 31, '2,5,8', 1),
    ('Mr', 'Liam', 'Smith', 'Teacher', '4444444444', 'liam@example.com', '234 Pine St, Suburb', '1997-08-08', 'No known health issues', 32, '6,10', 1),
    ('Miss', 'Ava', 'Johnson', 'Student', '5555555555', 'ava@example.com', '345 Birch St, City', '2002-03-20', 'No known health issues', 33, '1,3,9', 1);

CREATE TABLE Payment (
     payment_id INT PRIMARY KEY AUTO_INCREMENT,
     member_id INT NOT NULL,
     payment_type VARCHAR(20) NOT NULL,
     FOREIGN KEY (member_id) REFERENCES Members(member_id)
 );

INSERT INTO Payment (payment_id, member_id, payment_type)
VALUES 
(1, 1, "subscription"),
(2, 2, "subscription"),
(3, 3, "subscription"),
(4, 4, "subscription"),
(5, 5, "subscription"),
(6, 6, "subscription"),
(7, 7, "subscription"),
(8, 8, "subscription"),
(9, 9, "subscription"),
(10, 10, "subscription"),
(11, 1, "tuition"),
(12, 3, "tuition"),
(13, 5, "tuition"),
(14, 6, "tuition"),
(15, 9, "tuition"),
(16, 2, "tuition")
;

CREATE TABLE Subscriptions (
	subscription_id INT PRIMARY KEY AUTO_INCREMENT,
	member_id INT NOT NULL,
	subscription_type VARCHAR(50) NOT NULL,
	start_date DATE,
	end_date DATE,
	payment_amount DECIMAL(10, 2),
	payment_date DATE,
    subscription_status VARCHAR(20) NOT NULL,
    payment_id INT,
    FOREIGN KEY (member_id) REFERENCES Members(member_id),
    FOREIGN KEY (payment_id) REFERENCES Payment(payment_id)
);


INSERT INTO Subscriptions (member_id, subscription_type, start_date, end_date, payment_amount, payment_date, subscription_status, payment_id)
VALUES
    (1, 'Monthly', '2023-08-01', '2023-09-01', 70.00, '2023-08-01', 'active',1),
    (2, 'Monthly', '2023-08-01', '2023-09-01', 70.00, '2023-08-01', 'inactive', 2),
    (3, 'Monthly', '2023-08-01', '2023-09-01', 70.00, '2023-08-01', 'inactive', 3),
    (4, 'Monthly', '2023-08-01', '2023-09-01', 70.00, '2023-08-01', 'active', 4),
    (5, 'Monthly', '2023-08-01', '2023-09-01', 70.00, '2023-08-01', 'inactive', 5),
    (6, 'Monthly', '2023-08-01', '2023-09-01', 70.00, '2023-08-01', 'active', 6),
    (7, 'Monthly', '2023-08-01', '2023-09-01', 70.00, '2023-08-01', 'inactive',7),
    (8, 'Monthly', '2023-08-01', '2023-09-01', 70.00, '2023-08-01', 'active', 8),
    (9, 'Monthly', '2023-08-01', '2023-09-01', 70.00, '2023-08-01', 'inactive', 9),
    (10, 'Monthly', '2023-08-01', '2023-09-01', 70.00, '2023-08-01', 'active',10);


CREATE TABLE Pools (
    pool_id INT PRIMARY KEY,
    pool_name VARCHAR(255) NOT NULL,
    useage TEXT
);

INSERT INTO Pools (pool_id, pool_name, useage)
VALUES
	(1, 'Hydrotherapy', 'aqua aerobics class, individual lesson'),
    (2, 'Training', 'aqua aerobics class, individual lesson'),
    (3, 'Olympic', 'member swimming laps'),
    (4, 'Family', 'family, individual lesson');


  CREATE TABLE Courses (
     course_id INT PRIMARY KEY AUTO_INCREMENT,
     course_name VARCHAR(100) NOT NULL,
     course_type VARCHAR(50) NOT NULL,
     instructor_id INT NOT NULL,
     day_of_the_week VARCHAR(50) NOT NULL,
     start_time TIME NOT NULL,
     end_time TIME NOT NULL,
     max_capacity INT NOT NULL,
     booked_count INT,
     pool_id INT,
     FOREIGN KEY (instructor_id) REFERENCES Instructors(instructor_id),
     FOREIGN KEY (pool_id) REFERENCES Pools(pool_id)
 );


INSERT INTO Courses (course_name, course_type, instructor_id, day_of_the_week, start_time, end_time, max_capacity, booked_count, pool_id)
VALUES
    ('Aqua Fit', 'Aqua Aerobics', 1, 'Monday', '09:00:00', '10:00:00', 30, 0, 1),
    ('Water Zumba', 'Aqua Aerobics', 2, 'Wednesday', '10:00:00', '11:00:00', 4, 4, 1),
    ('Deep Water Workout', 'Aqua Aerobics', 3, 'Friday', '15:00:00', '16:00:00', 30, 0, 2),
    ('Cardio Splash', 'Aqua Aerobics', 4, 'Tuesday', '14:00:00', '15:00:00', 30, 0, 2),
    ('Aqua Strength', 'Aqua Aerobics', 5, 'Thursday', '11:00:00', '12:00:00', 30, 0, 1),
    ('Hydro Cycling', 'Aqua Cycling', 1, 'Monday', '18:00:00', '19:00:00', 30, 0, 2),
    ('Aqua Yoga', 'Aqua Yoga', 2, 'Saturday', '10:00:00', '11:00:00', 5, 0, 1),
    ('Swim-Sculpt', 'Aqua Fitness', 3, 'Sunday', '16:00:00', '17:00:00', 30, 0, 2),
    ('Aquatic Bootcamp', 'Aqua Fitness', 4, 'Thursday', '17:00:00', '18:00:00', 30, 0, 2),
    ('Poolside Pilates', 'Aqua Pilates', 5, 'Tuesday', '09:00:00', '10:00:00', 30, 0, 1);



 CREATE TABLE IndividualLessons (
     lesson_id INT PRIMARY KEY AUTO_INCREMENT,
     member_id INT,
     instructor_id INT NOT NULL,
     lesson_duration INT NOT NULL,
     date DATE NOT NULL,
     lesson_time TIME NOT NULL,
     lesson_fee DECIMAL(10, 2) NOT NULL,
     lesson_status VARCHAR(20) NOT NULL,
     pool_id INT,
     payment_id INT,
     payment_date DATE,
     FOREIGN KEY (pool_id) REFERENCES Pools(pool_id),
     FOREIGN KEY (member_id) REFERENCES Members(member_id),
     FOREIGN KEY (instructor_id) REFERENCES Instructors(instructor_id),
     FOREIGN KEY (payment_id) REFERENCES Payment(payment_id)
 );


INSERT INTO IndividualLessons (member_id, instructor_id, lesson_duration, date, lesson_time, lesson_fee, lesson_status, pool_id, payment_id, payment_date)
VALUES
    (1, 1, 30, curdate(), '11:00', 44.00, 'booked', 2, 11, '2023-08-01'),
    (Null, 2, 60, curdate(), '14:00', 80.00, 'available', 1, Null, Null),

    (Null, 3, 60, ADDDATE(curdate(), INTERVAL 1 DAY), '09:00', 80.00, 'available', 2, Null, Null),
    (Null, 3, 30, ADDDATE(curdate(), INTERVAL 1 DAY), '10:00', 44.00, 'available', 2, Null, Null),

    (3, 4, 60, ADDDATE(curdate(), INTERVAL 2 DAY), '10:00', 80.00, 'booked', 2, 12, '2023-08-01'),
    (5, 3, 30, ADDDATE(curdate(), INTERVAL 2 DAY), '16:00', 44.00, 'booked', 1, 13, '2023-08-01'),

    (Null, 5, 60, ADDDATE(curdate(), INTERVAL 3 DAY), '15:00', 80.00, 'available', 1, Null, Null),
    (6, 5, 60, ADDDATE(curdate(), INTERVAL 3 DAY), '16:00', 80.00, 'booked', 1, 14, '2023-08-01'),

    (9, 1, 60, ADDDATE(curdate(), INTERVAL 4 DAY), '09:00', 80.00, 'booked', 2, 15, '2023-08-01'),
    (Null, 1, 30, ADDDATE(curdate(), INTERVAL 4 DAY), '10:00', 44.00, 'available', 3, Null, Null),

    (2, 2, 60, ADDDATE(curdate(), INTERVAL 5 DAY), '13:00', 80.00, 'booked',1, 16, '2023-08-01'),
    (Null, 2, 30, ADDDATE(curdate(), INTERVAL 5 DAY), '14:00', 44.00, 'available', 3, Null, Null),
    
    (Null, 3, 60, ADDDATE(curdate(), INTERVAL 6 DAY), '09:00', 80.00, 'available', 2, Null, Null),
    (Null, 3, 30, ADDDATE(curdate(), INTERVAL 6 DAY), '10:00', 44.00, 'available', 2, Null, Null),
    
    (Null, 3, 60, ADDDATE(curdate(), INTERVAL 7 DAY), '09:00', 80.00, 'available', 2, Null, Null),
    (Null, 5, 30, ADDDATE(curdate(), INTERVAL 7 DAY), '10:00', 44.00, 'available', 2, Null, Null),

    (Null, 2, 60, ADDDATE(curdate(), INTERVAL 8 DAY), '14:00', 80.00, 'available', 1, Null, Null),
    (Null, 5, 30, ADDDATE(curdate(), INTERVAL 8 DAY), '10:00', 44.00, 'available', 2, Null, Null),

    (Null, 1, 60, ADDDATE(curdate(), INTERVAL 9 DAY), '09:00', 80.00, 'available', 2, Null, Null),
    (Null, 3, 30, ADDDATE(curdate(), INTERVAL 9 DAY), '10:00', 44.00, 'available', 2, Null, Null),
    
    (Null, 2, 60, ADDDATE(curdate(), INTERVAL 10 DAY), '09:00', 80.00, 'available', 2, Null, Null),
    (Null, 5, 30, ADDDATE(curdate(), INTERVAL 10 DAY), '10:00', 44.00, 'available', 2, Null, Null),

    (Null, 2, 60, ADDDATE(curdate(), INTERVAL 11 DAY), '14:00', 80.00, 'available', 1, Null, Null),
    (Null, 1, 30, ADDDATE(curdate(), INTERVAL 11 DAY), '10:00', 44.00, 'available', 2, Null, Null),

    (Null, 1, 60, ADDDATE(curdate(), INTERVAL 12 DAY), '09:00', 80.00, 'available', 2, Null, Null),
    (Null, 3, 30, ADDDATE(curdate(), INTERVAL 12 DAY), '10:00', 44.00, 'available', 2, Null, Null),
    
    (Null, 2, 60, ADDDATE(curdate(), INTERVAL 13 DAY), '09:00', 80.00, 'available', 2, Null, Null),
    (Null, 5, 30, ADDDATE(curdate(), INTERVAL 13 DAY), '10:00', 44.00, 'available', 2, Null, Null)

    ;


CREATE TABLE Activities (
    activity_id INT PRIMARY KEY AUTO_INCREMENT,
    activity_type VARCHAR(30) NOT NULL
 );

 INSERT INTO Activities (activity_id, activity_type) VALUES
    (1, 'pool use'),
    (2, 'aqua aerobics'),
    (3, 'swimming lesson');

CREATE TABLE Attendance (
    attendance_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT NOT NULL,
    activity_id INT NOT NULL,
    course_id INT,
    attendance_date DATE,
    FOREIGN KEY (member_id) REFERENCES Members(member_id), 
    FOREIGN KEY (activity_id) REFERENCES Activities(activity_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
 );

INSERT INTO Attendance (member_id, activity_id, attendance_date, course_id) VALUES
    (1, 1, '2023-09-13', NULL),
    (1, 2, '2023-09-10', 7),
    (1, 3, '2023-09-06', NULL),
    (1, 1, '2023-09-01', NULL),
    (1, 1, '2023-08-30', NULL),
    (1, 1, '2023-08-26', NULL),
    (1, 1, '2023-08-24', NULL),
    (1, 2, '2023-08-20', 7),
    (1, 3, '2023-08-15', NULL),
    (1, 1, '2023-08-13', NULL),
    (1, 2, '2023-08-06', 10),
    (1, 1, '2023-08-01', NULL),
    (1, 1, '2023-07-30', NULL),
    (1, 1, '2023-07-26', NULL),
    (1, 1, '2023-07-24', NULL),
    (1, 1, '2023-07-20', NULL),
    (1, 1, '2023-07-15', NULL),
    (1, 2, '2023-07-13', 7),
    (1, 3, '2023-07-06', NULL),
    (1, 2, '2023-07-01', 8),
    (1, 2, '2023-06-30', 5),
    (1, 2, '2023-06-26', 6),
    (1, 1, '2023-06-24', NULL),
    (1, 1, '2023-06-20', NULL),
    (1, 1, '2023-06-15', NULL),
    (1, 3, '2023-06-13', NULL),

    (2, 1, '2023-09-13', NULL),
    (2, 2, '2023-09-06', 8),
    (2, 1, '2023-09-01', NULL),
    (2, 1, '2023-08-30', NULL),
    (2, 1, '2023-08-26', NULL),
    (2, 2, '2023-08-24', 7),
    (2, 2, '2023-08-20', 8),
    (2, 3, '2023-08-15', NULL),
    (2, 1, '2023-08-13', NULL),
    (2, 2, '2023-08-06', 7),
    (2, 1, '2023-08-01', NULL),
    (2, 1, '2023-07-30', NULL),
    (2, 1, '2023-07-26', NULL),
    (2, 1, '2023-07-24', NULL),
    (2, 1, '2023-07-20', NULL),
    (2, 2, '2023-07-15', 7),
    (2, 2, '2023-07-13', 8),
    (2, 3, '2023-07-06', NULL),
    (2, 2, '2023-07-01', 3),
    (2, 2, '2023-06-30', 7),
    (2, 2, '2023-06-26', 6),
    (2, 1, '2023-06-24', NULL),
    (2, 3, '2023-06-20', NULL),
    (2, 1, '2023-06-06', NULL),
    (2, 3, '2023-06-01', NULL),

    (3, 1, '2023-09-13', NULL),
    (3, 2, '2023-09-10', 6),
    (3, 1, '2023-08-30', NULL),
    (3, 1, '2023-08-24', NULL),
    (3, 2, '2023-08-20', 3),
    (3, 3, '2023-08-15', NULL),
    (3, 1, '2023-08-13', NULL),
    (3, 2, '2023-08-06', 3),
    (3, 1, '2023-08-01', NULL),
    (3, 1, '2023-07-30', NULL),
    (3, 1, '2023-07-26', NULL),
    (3, 1, '2023-07-24', NULL),
    (3, 1, '2023-07-20', NULL),
    (3, 1, '2023-07-15', NULL),
    (3, 2, '2023-07-13', 3),
    (3, 3, '2023-07-06', NULL),
    (3, 2, '2023-07-01', 6),
    (3, 2, '2023-06-30', 3),
    (3, 2, '2023-06-26', 3),
    (3, 1, '2023-06-24', NULL),
    (3, 1, '2023-06-20', NULL),
    (3, 1, '2023-06-15', NULL),
    (3, 3, '2023-06-13', NULL),
    (3, 1, '2023-06-06', NULL),

    (4, 1, '2023-09-13', NULL),
    (4, 2, '2023-09-10', 7),
    (4, 1, '2023-09-06', NULL),
    (4, 1, '2023-09-01', NULL),
    (4, 1, '2023-08-30', NULL),
    (4, 1, '2023-08-26', NULL),
    (4, 1, '2023-08-24', NULL),
    (4, 2, '2023-08-20', 7),
    (4, 3, '2023-08-15', NULL),
    (4, 1, '2023-08-13', NULL),
    (4, 1, '2023-07-30', NULL),
    (4, 1, '2023-07-26', NULL),
    (4, 1, '2023-07-24', NULL),
    (4, 1, '2023-07-20', NULL),
    (4, 1, '2023-07-15', NULL),
    (4, 2, '2023-07-13', 8),
    (4, 3, '2023-07-06', NULL),
    (4, 2, '2023-07-01', 8),
    (4, 2, '2023-06-30', 1),
    (4, 2, '2023-06-26', 8),
    (4, 1, '2023-06-24', NULL),
    (4, 1, '2023-06-20', NULL),

    (5, 1, '2023-09-13', NULL),
    (5, 2, '2023-09-10', 3),
    (5, 1, '2023-09-06', NULL),
    (5, 1, '2023-09-01', NULL),
    (5, 1, '2023-08-30', NULL),
    (5, 1, '2023-08-26', NULL),
    (5, 1, '2023-08-24', NULL),
    (5, 2, '2023-08-20', 3),
    (5, 3, '2023-08-15', NULL),
    (5, 1, '2023-08-13', NULL),
    (5, 2, '2023-08-06', 8),
    (5, 1, '2023-08-01', NULL),
    (5, 1, '2023-07-30', NULL),
    (5, 1, '2023-07-26', NULL),
    (5, 1, '2023-07-24', NULL),
    (5, 1, '2023-07-20', NULL),
    (5, 1, '2023-07-15', NULL),
    (5, 2, '2023-07-13', 8),
    (5, 3, '2023-07-06', NULL),
    (5, 2, '2023-07-01', 3),
    (5, 2, '2023-06-30', 8),
    (5, 2, '2023-06-26', 3),
    (5, 1, '2023-06-24', NULL),
    (5, 1, '2023-06-20', NULL),
    (5, 1, '2023-06-15', NULL),
    (5, 3, '2023-06-13', NULL),
    (5, 1, '2023-06-06', NULL),

    (6, 1, '2023-09-13', NULL),
    (6, 2, '2023-09-10', 9),
    (6, 1, '2023-09-06', NULL),
    (6, 1, '2023-09-01', NULL),
    (6, 1, '2023-08-30', NULL),
    (6, 1, '2023-08-26', NULL),
    (6, 1, '2023-08-24', NULL),
    (6, 2, '2023-08-20', 9),
    (6, 2, '2023-08-15', 7),
    (6, 1, '2023-08-13', NULL),
    (6, 2, '2023-08-06', 7),
    (6, 1, '2023-08-01', NULL),
    (6, 2, '2023-07-30', 7),
    (6, 1, '2023-07-26', NULL),
    (6, 1, '2023-07-24', NULL),
    (6, 1, '2023-07-20', NULL),
    (6, 1, '2023-07-15', NULL),
    (6, 2, '2023-07-13', 9),
    (6, 1, '2023-07-06', NULL),
    (6, 2, '2023-07-01', 9),
    (6, 2, '2023-06-30', 9),
    (6, 2, '2023-06-26', 7),
    (6, 1, '2023-06-24', NULL),
    (6, 1, '2023-06-20', NULL),
    (6, 1, '2023-06-15', NULL),
    (6, 1, '2023-06-13', NULL),
    (6, 1, '2023-06-06', NULL),
    (6, 1, '2023-06-01', NULL),

    (7, 1, '2023-09-06', NULL),
    (7, 1, '2023-09-01', NULL),
    (7, 1, '2023-08-30', NULL),
    (7, 1, '2023-08-26', NULL),
    (7, 1, '2023-08-24', NULL),
    (7, 2, '2023-08-20', 8),
    (7, 3, '2023-08-15', NULL),
    (7, 1, '2023-08-13', NULL),
    (7, 2, '2023-08-06', 8),
    (7, 1, '2023-08-01', NULL),
    (7, 1, '2023-07-30', NULL),
    (7, 1, '2023-07-26', NULL),
    (7, 1, '2023-07-24', NULL),
    (7, 1, '2023-07-20', NULL),
    (7, 1, '2023-07-15', NULL),
    (7, 2, '2023-07-13', 6),
    (7, 3, '2023-07-06', NULL),
    (7, 2, '2023-07-01', 8),
    (7, 2, '2023-06-30', 8),
    (7, 2, '2023-06-26', 6),
    (7, 1, '2023-06-24', NULL),
    (7, 1, '2023-06-20', NULL),
    (7, 1, '2023-06-15', NULL),
    (7, 3, '2023-06-13', NULL),
    (7, 1, '2023-06-06', NULL),
    (7, 3, '2023-06-01', NULL),

    (8, 1, '2023-09-13', NULL),
    (8, 2, '2023-09-10', 3),
    (8, 1, '2023-09-06', NULL),
    (8, 1, '2023-09-01', NULL),
    (8, 1, '2023-08-30', NULL),
    (8, 1, '2023-08-26', NULL),
    (8, 1, '2023-08-24', NULL),
    (8, 2, '2023-08-20', 3),
    (8, 3, '2023-08-15', NULL),
    (8, 1, '2023-08-13', NULL),
    (8, 2, '2023-08-06', 9),
    (8, 1, '2023-08-01', NULL),
    (8, 1, '2023-07-30', NULL),
    (8, 1, '2023-07-26', NULL),
    (8, 1, '2023-07-24', NULL),
    (8, 1, '2023-07-20', NULL),
    (8, 1, '2023-07-15', NULL),
    (8, 2, '2023-07-13', 3),
    (8, 3, '2023-07-06', NULL),
    (8, 2, '2023-07-01', 9),
    (8, 2, '2023-06-30', 3),
    (8, 2, '2023-06-26', 3),
    (8, 1, '2023-06-24', NULL),
    (8, 1, '2023-06-20', NULL),
    (8, 1, '2023-06-15', NULL),
    (8, 3, '2023-06-13', NULL),
    (8, 1, '2023-06-06', NULL),
    (8, 3, '2023-06-01', NULL),

    (9, 1, '2023-09-13', NULL),
    (9, 2, '2023-09-10', 4),
    (9, 1, '2023-09-06', NULL),
    (9, 2, '2023-09-01', 5),
    (9, 1, '2023-08-30', NULL),
    (9, 1, '2023-08-26', NULL),
    (9, 2, '2023-08-24', 1),
    (9, 2, '2023-08-20', 10),
    (9, 3, '2023-08-15', NULL),
    (9, 1, '2023-08-13', NULL),
    (9, 2, '2023-08-06', 2),
    (9, 1, '2023-08-01', NULL),
    (9, 1, '2023-07-30', NULL),
    (9, 2, '2023-07-26', 5),
    (9, 1, '2023-07-24', NULL),
    (9, 1, '2023-07-20', NULL),
    (9, 2, '2023-07-15', 1),
    (9, 3, '2023-07-06', NULL),
    (9, 2, '2023-07-01', 4),
    (9, 2, '2023-06-30', 2),
    (9, 2, '2023-06-26', 10),
    (9, 1, '2023-06-24', NULL),
    (9, 1, '2023-06-20', NULL),
    (9, 1, '2023-06-06', NULL),
    (9, 3, '2023-06-01', NULL),

    (10, 1, '2023-09-13', NULL),
    (10, 1, '2023-09-06', NULL),
    (10, 1, '2023-09-01', NULL),
    (10, 1, '2023-08-30', NULL),
    (10, 1, '2023-08-26', NULL),
    (10, 1, '2023-08-24', NULL),
    (10, 2, '2023-08-20', 1),
    (10, 3, '2023-08-15', NULL),
    (10, 1, '2023-08-13', NULL),
    (10, 2, '2023-08-06', 5),
    (10, 1, '2023-08-01', NULL),
    (10, 1, '2023-07-30', NULL),
    (10, 1, '2023-07-26', NULL),
    (10, 1, '2023-07-24', NULL),
    (10, 1, '2023-07-20', NULL),
    (10, 1, '2023-07-15', NULL),
    (10, 2, '2023-07-13', 4),
    (10, 3, '2023-07-06', NULL),
    (10, 2, '2023-07-01', 10),
    (10, 2, '2023-06-30', 5),
    (10, 2, '2023-06-26', 1),
    (10, 1, '2023-06-24', NULL),
    (10, 1, '2023-06-20', NULL),
    (10, 1, '2023-06-15', NULL),
    (10, 3, '2023-06-13', NULL),
    (10, 1, '2023-06-06', NULL),
    (10, 3, '2023-06-01', NULL);

CREATE TABLE NewsUpdates (
    update_id INT PRIMARY KEY AUTO_INCREMENT,
    subject VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
