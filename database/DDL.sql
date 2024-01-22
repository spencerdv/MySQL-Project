-- Karim Mahmoud
-- Spencer Verhagen
-- CS 340
-- Project Step 2 Draft

SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;

-- create the majors table
DROP TABLE IF EXISTS Majors;
CREATE TABLE Majors
(
    majorID INTEGER AUTO_INCREMENT not NULL,
    name    VARCHAR(255)           not NULL,
    PRIMARY KEY (majorID)
);

-- create the dorms table
DROP TABLE IF EXISTS Dorms;
CREATE TABLE Dorms
(
    dormID       INTEGER AUTO_INCREMENT NOT NULL,
    name         VARCHAR(255)           NOT NULL,
    address      VARCHAR(255),
    maxOccupancy INTEGER                not NULL,
    PRIMARY KEY (dormID)
);

-- create the students table
DROP TABLE IF EXISTS Students;
CREATE TABLE Students
(
    studentID        INTEGER AUTO_INCREMENT NOT NULL,
    firstName        VARCHAR(255)           NOT NULL,
    lastName         VARCHAR(255)           NOT NULL,
    GPA              DECIMAL(3, 2),
    dormID           INTEGER,
    majorID          INTEGER                NOT NULL,
    classification   VARCHAR(255)           NOT NULL,
    enrollmentStatus VARCHAR(255)           NOT NULL,
    PRIMARY KEY (studentID),
    FOREIGN KEY (dormID) REFERENCES Dorms (dormID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (majorID) REFERENCES Majors (majorID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- create the courses table
DROP TABLE IF EXISTS Courses;
CREATE TABLE Courses
(
    courseID      INTEGER      NOT NULL AUTO_INCREMENT,
    courseName    VARCHAR(255) NOT NULL,
    maxEnrollment INTEGER      NOT NULL,
    PRIMARY KEY (courseID)
);

-- create the majors_courses table
DROP TABLE IF EXISTS MajorCourses;
CREATE TABLE MajorCourses
(
    majorCourseID INTEGER NOT NULL AUTO_INCREMENT,
    majorID       INTEGER NOT NULL,
    courseID      INTEGER NOT NULL,
    PRIMARY KEY (majorCourseID),
    FOREIGN KEY (majorID) REFERENCES Majors (majorID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (courseID) REFERENCES Courses (courseID) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE (majorID, courseID)
);


-- create the students_courses table
DROP TABLE IF EXISTS StudentCourses;
CREATE TABLE StudentCourses
(
    studentCourseID INTEGER NOT NULL AUTO_INCREMENT,
    studentID       INTEGER NOT NULL,
    courseID        INTEGER NOT NULL,
    PRIMARY KEY (studentCourseID),
    FOREIGN KEY (studentID) REFERENCES Students (studentID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (courseID) REFERENCES Courses (courseID) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE (studentID, courseID)
);


-- insert data into the Dorms table
INSERT INTO Dorms (name, address, maxOccupancy)
VALUES ('Bloss', '2001, SW Western Blvd, Corvallis, OR 97333', 100),
       ('Callahan', '1420 SW Jefferson Way, Corvallis, OR 97331', 120),
       ('Finley', '2100 SW May Ave, Corvallis, OR 97333', 250),
       ('Hawley', '311 SW Sackett Pl, Corvallis, OR 97331', 80),
       ('Wilson', '1351 SW Adams Ave, Corvallis, OR 97331', 90);

-- insert data into the Majors table
INSERT INTO Majors (name)
VALUES ('Human Biology'),
       ('Computer Science'),
       ('History'),
       ('Pre-Law'),
       ('Accounting');

-- insert data into the Courses table
INSERT INTO Courses (courseName, maxEnrollment)
VALUES ('Databases', 100),
       ('Cell Biology', 100),
       ('Literature', 200),
       ('Algebra 101', 50),
       ('Leadership', 30);

-- insert data into the Majors_Courses table
INSERT INTO MajorCourses (majorID, courseID)
VALUES ((SELECT majorID FROM Majors WHERE name = 'History'),
        (SELECT courseID FROM Courses WHERE courseName = 'Literature')),
       ((SELECT majorID FROM Majors WHERE name = 'History'),
        (SELECT courseID FROM Courses WHERE courseName = 'Leadership')),
       ((SELECT majorID FROM Majors WHERE name = 'Human Biology'),
        (SELECT courseID FROM Courses WHERE courseName = 'Cell Biology')),
       ((SELECT majorID FROM Majors WHERE name = 'Human Biology'),
        (SELECT courseID FROM Courses WHERE courseName = 'Literature')),
       ((SELECT majorID FROM Majors WHERE name = 'Computer Science'),
        (SELECT courseID FROM Courses WHERE courseName = 'Databases'));

-- insert data into the Students table
INSERT INTO Students (firstName, lastName, GPA, dormID, majorID, classification, enrollmentStatus)
VALUES ('Spencer', 'Verhagen', 2.2, 1, 2, 'Sophmore', 'Part-time'),
       ('Karim', 'Doe', 4.0, 3, 2, 'Sophmore', 'Full-time'),
       ('Sarah', 'Smith', 3.6, 3, 2, 'Junior', 'Graduated'),
       ('John', 'West', 3.4, 1, 4, 'Senior', 'Full-time'),
       ('Patrick', 'Kelce', 3.0, 1, 2, 'Freshman', 'Full-time');

-- insert data into the Students_Courses table
INSERT INTO StudentCourses (studentID, courseID)
VALUES ((SELECT studentID FROM Students WHERE firstName = 'John' AND lastName = 'West'),
        (SELECT courseID FROM Courses WHERE courseName = 'Literature')),
       ((SELECT studentID FROM Students WHERE firstName = 'Sarah'AND lastName = 'Smith'),
        (SELECT courseID FROM Courses WHERE courseName = 'Algebra 101')),
       ((SELECT studentID
         FROM Students
         WHERE firstName = 'John'
           AND lastName = 'West'), (SELECT courseID
                                    FROM Courses
                                    WHERE courseName = 'Cell Biology')),
       ((SELECT studentID
         FROM Students
         WHERE firstName = 'Karim'
           AND lastName = 'Doe'), (SELECT courseID
                                   FROM Courses
                                   WHERE courseName = 'Algebra 101')),
       ((SELECT studentID
         FROM Students
         WHERE firstName = 'Spencer'
           AND lastName = 'Verhagen'), (SELECT courseID
                                        FROM Courses
                                        WHERE courseName = 'Databases'));


SET FOREIGN_KEY_CHECKS = 1;
COMMIT;

