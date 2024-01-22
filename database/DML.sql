
-- Query for add a new character functionality with colon : character being used to 
-- denote the variables that will have data from the backend programming language

-- -------- Students
-- References data pertaining to the Students entity
-- SELECT join on dorms and majors
SELECT student.studentID, student.firstName, student.lastName, student.GPA, dorm.name, major.name, student.classification, student.enrollmentStatus  FROM Students student JOIN Dorms dorm ON student.dormID = dorm.dormID JOIN Majors major ON student.majorID = major.majorID;

SELECT * FROM Students;

-- SEARCH
SELECT * FROM Students WHERE firstName = :firstName AND lastName = :lastName;

-- INSERT
-- Inserts student info into Students table
INSERT INTO Students (firstName, lastName, GPA, classification, enrollmentStatus, dormID, majorID) VALUES (:firstName, :lastName, :GPA, :classification, :enrollmentStatus,
                                                                                                           (SELECT dormID FROM Dorms WHERE name = :dormName), (SELECT majorID FROM Majors WHERE name = :majorName));
-- UPDATE
-- Updates student info in the Students table
UPDATE Students SET firstName = :firstName, lastName = :lastName, GPA = :GPA, classification = :classification, enrollmentStatus = :enrollmentStatus, dormID = (SELECT dormID FROM Dorms WHERE name = :dormName), majorID = (SELECT majorID FROM Majors WHERE name = :majorName) WHERE studentID = :studentID;

-- DELETE
-- Deletes student info in Students table
DELETE FROM Students WHERE studentID = :studentID;


-- -------- Courses
-- References data pertaining to the Courses entity

-- - SELECT
SELECT * FROM Courses;

-- SEARCH
SELECT * FROM Courses WHERE courseName = :courseName;

-- INSERT
-- Inserts course info into Courses table
INSERT INTO Courses (courseName, maxEnrollment) VALUES (:courseName, :maxEnrollment);

-- UPDATE
-- Updates course info into Courses table
UPDATE Courses SET courseName = :courseName, maxEnrollment = :maxEnrollment WHERE courseID = :courseID;

-- DELETE
-- Deletes course info into Courses table
DELETE FROM Courses WHERE courseID = :courseID;



-- -------- Dorms
-- References data pertaining to the Dorms entity
-- Variables sourced from the backend are denoted with a colon prefix (:)
SELECT * FROM Dorms;

-- Search
SELECT * FROM Dorms WHERE name = :name;

-- Insert
-- Inserts dorms info into Dorms table
INSERT INTO Dorms (name, address, maxOccupancy)
VALUES (:name, :address, :maxOccupancy);


-- Update
-- Updates a dorm in the Dorms table
-- Variables sourced from the backend are denoted with a colon prefix (:)
UPDATE Dorms
SET name = :name,
    address = :address,
    maxOccupancy = :maxOccupancy
WHERE dormID = :dormID;

-- Delete
-- Inserts dorm info in Dorms table
DELETE FROM Dorms WHERE dormID = :dormID;

-- ------------------
-- Majors
-- References data pertaining to the Majors entity

-- Create
SELECT * FROM Majors;

-- Search
SELECT * FROM Majors WHERE name = :name;

-- Insert
-- Inserts major info into Majors table
INSERT INTO Majors (name)
VALUES (:name);

-- Update
-- Updates major info in Majors table
UPDATE Majors
SET name = :name
WHERE majorID = :majorID;

-- Delete
-- Deletes major info in Majors table
DELETE FROM Majors WHERE majorID = :majorID;


-- ---------- 
-- Students Courses Intersection Table
-- References data pertaining to the StudentCourses entity

-- SELECT with join on Students and Courses
SELECT studentCourse.studentCourseID, CONCAT(student.firstName, ' ', student.lastName) as StudentName, course.courseName FROM StudentCourses studentCourse JOIN Students student ON studentCourse.studentID = student.studentID JOIN Courses course ON studentCourse.courseID = course.courseID;

-- SEARCH
SELECT * FROM StudentCourses WHERE studentID = :studentID AND courseID = :courseID;


-- INSERT
-- Inserts data into StudentCourses table
INSERT INTO StudentCourses (studentID, courseID) VALUES ((SELECT studentID FROM Students WHERE firstName = :firstName AND lastName = :lastName),
                                                           (SELECT courseID FROM Courses WHERE courseName = :courseName));

-- UPDATE
-- Updates data in StudentCourses table
UPDATE StudentCourses SET studentID = (SELECT studentID FROM Students WHERE firstName = :firstName AND lastName = :lastName),
                            courseID = (SELECT courseID FROM Courses WHERE courseName = :courseName) WHERE studentCourseID = :studentCourseID;

-- DELETE
-- Deletes data from StudentCourses table
DELETE FROM StudentCourses WHERE studentCourseID = :studentCourseID;


-- ---------------
--  Major Courses Intersection Table
-- References data pertaining to the MajorCourses entity

-- SELECT with JOIN on Majors and Courses
SELECT majorCourse.majorCourseID, major.name AS MajorName, course.courseName AS CourseName FROM MajorCourses majorCourse JOIN Majors major ON majorCourse.majorID = major.majorID JOIN Courses course ON majorCourse.courseID = course.courseID;

-- SEARCH
SELECT * FROM MajorCourses WHERE majorID = :majorID AND courseID = :courseID;

-- INSERT
-- Inserts data into MajorCourses table
INSERT INTO MajorCourses (majorID, courseID) VALUES ((SELECT majorID FROM Majors WHERE name = :name),
                                                       (SELECT courseID FROM Courses WHERE courseName = :courseName));

-- UPDATE 
-- Updates data in MajorCourses table
UPDATE 
    MajorCourses
SET
    majorID = (
        SELECT  majorID 
        FROM Majors
        WHERE name = :name),
    courseID = (
        SELECT courseID
        FROM Courses
        WHERE courseName = :courseName
    )
    WHERE majorCourseID = :majorCourseID;

-- DELETE
-- Deletes data in MajorCourses table
DELETE FROM MajorCourses
WHERE majorCourseID = :majorCourseID;
