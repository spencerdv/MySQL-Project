"""
Citations:
CS 340 Starter Project - https://github.com/osu-cs340-ecampus/flask-starter-app#accessing-the-database
This project was used as a starting point for this project. The database connection code was used from this project.
It was modified to use the database connector that was created for this project. The query methods were adapted from
this project as well.
"""
import database.db_connector as db
from flask import Flask, render_template, json, request, redirect, jsonify, flash, abort
from flask_mysqldb import MySQL

# Configuration
app = Flask(__name__)

app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_mahmoudk"
app.config["MYSQL_PASSWORD"] = "7813"
app.config["MYSQL_DB"] = "cs340_mahmoudk"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"


db_connection = db.connect_to_database()
mysql = MySQL(app)


studentData = [
    {
        "student_ID": 1,
        "first_Name": "Spencer",
        "last_Name": "Verhagen",
        "GPA": 2.2,
        "Classification": "Sophomore",
        "enrollment_Status": "Part-Time",
        "dormName": "Bloss",
        "majorName": "Computer Science"
    },
    {
        "student_ID": 2,
        "first_Name": "Karim",
        "last_Name": "Doe",
        "GPA": 4.0,
        "Classification": "Sophomore",
        "enrollment_Status": "Full-Time",
        "dormName": "Finley",
        "majorName": "Computer Science",
    },
    {
        "student_ID": 3,
        "first_Name": "Sarah",
        "last_Name": "Smith",
        "GPA": 3.6,
        "Classification": "Junior",
        "enrollment_Status": "Graduated",
        "dormName": "Finley",
        "majorName": "Pre-Law"
    },
    {
        "student_ID": 4,
        "first_Name": "John",
        "last_Name": "West",
        "GPA": 3.4,
        "Classification": "Senior",
        "enrollment_Status": "Full-Time",
        "dormName": "Bloss",
        "majorName": "Computer Science",
    },
    {
        "student_ID": 5,
        "first_Name": "Patrick",
        "last_Name": "Kelce",
        "GPA": 3.0,
        "Classification": "Freshman",
        "enrollment_Status": "Full-time",
        "dormName": "Bloss",
        "majorName": "Computer Science",
    },
]

courseData = [
    {
        "courseID": 1,
        "courseName": "Databases",
        "maxEnrollment": 100
    },
    {
        "courseID": 2,
        "courseName": "Cell Biology",
        "maxEnrollment": 100
    },
    {
        "courseID": 3,
        "courseName": "Literature",
        "maxEnrollment": 200
    },
    {
        "courseID": 4,
        "courseName": "Algebra 101",
        "maxEnrollment": 50
    },
    {
        "courseID": 5,
        "courseName": "Leadership",
        "maxEnrollment": 30
    },
]

majorCourseData = [
    {
        "majorCourseID": 1,
        "majorName": "History",
        "courseName": "Literature"
    },
    {
        "majorCourseID": 2,
        "majorName": "History",
        "courseName": "Leadership"
    },
    {
        "majorCourseID": 3,
        "majorName": "Human Biology",
        "courseName": "Cell Biology"
    },
    {
        "majorCourseID": 4,
        "majorName": "Human Biology",
        "courseName": "Literature"
    },
    {
        "majorCourseID": 5,
        "majorName": "Computer Science",
        "courseName": "Databases"
    },
]

studentCourseData = [
    {
        "studentCourseID": 1,
        "studentName": "John West",
        "courseName": "Literature"
    },
    {
        "studentCourseID": 2,
        "studentName": "Sarah Smith",
        "courseName": "Algebra 101"
    },
    {
        "studentCourseID": 3,
        "studentName": "John West",
        "courseName": "Cell Biology"
    },
    {
        "studentCourseID": 4,
        "studentName": "Karim Doe",
        "courseName": "Algebra 101"
    },
    {
        "studentCourseID": 5,
        "studentName": "Spencer Verhagen",
        "courseName": "Databases"
    },
]

dormList = [
    {
        "dormID": 1,
        "name": "Bloss",
        "address": "2001 SW Western Blvd, Corvallis, OR 97333",
        "maxOccupancy": 100,
    },
    {
        "dormID": 2,
        "name": "Callahan",
        "address": "2001 SW Western Blvd, Corvallis, OR 97333",
        "maxOccupancy": 120,
    },
    {
        "dormID": 3,
        "name": "Finley",
        "address": "2100 SW May Ave, Corvallis, OR 97333",
        "maxOccupancy": 250,
    },
    {
        "dormID": 4,
        "name": "Hawley",
        "address": "311 SW Sackett Pl, Corvallis, OR 97331",
        "maxOccupancy": 80,
    },
    {
        "dormID": 5,
        "name": "Wilson",
        "address": "1351 SW Adams Ave, Corvallis, OR 97331",
        "maxOccupancy": 90,
    },
]

majorList = [
    {
        "majorID": 1,
        "name": "Humon Biology"
    },
    {
        "majorID": 2,
        "name": "Computer Science"
    },
    {
        "majorID": 3,
        "name": "History"
    },
    {
        "majorID": 4,
        "name": "Pre-Law"
    },
    {
        "majorID": 5,
        "name": "Accounting"
    },
]


# Routes
@app.route("/")
def root():
    """ """
    return render_template("main.j2")

@app.route("/Students", methods=["GET", "POST", "PUT"])
def Students():
    
    def get_students():
        db_connection = db.connect_to_database()
        query = "SELECT student.studentID, student.firstName, student.lastName, student.GPA,  student.classification, student.enrollmentStatus, major.name, dorm.name  FROM Students student LEFT JOIN Dorms dorm ON student.dormID = dorm.dormID JOIN Majors major ON student.majorID = major.majorID ORDER BY studentID;"
        cursor =  db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("students.j2", studentList=results)

    # if the request is a GET request, then return the students page
    if request.method == "GET":
        return get_students()

    # if the request is a POST request, then add the student to the database
    elif request.method == "POST":
        data = request.get_json()
        first_name = data["First Name"]
        last_name = data["Last Name"]
        gpa = data["GPA"]
        classification = data["Classification"]
        enrollment_status = data["Enrollment Status"]
        dorm_name = data["Dorm Name"]
        major_name = data["Major Name"]

        # if the dorm_name is null, then remove it from the query
        if dorm_name == "" or dorm_name == "NULL" or dorm_name == "null":
            query = "INSERT INTO Students (firstName, lastName, GPA, classification, enrollmentStatus, majorID) VALUES (%s, %s, %s, %s, %s, (SELECT majorID FROM Majors WHERE name=%s));"
            data = (first_name, last_name, gpa, classification, enrollment_status, major_name)
            db_connection = db.connect_to_database()
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=data)
            return get_students()

        else:
            query = "INSERT INTO Students (firstName, lastName, GPA, classification, enrollmentStatus, dormID, majorID) VALUES (%s, %s, %s, %s, %s,(SELECT dormID FROM Dorms WHERE name = %s), (SELECT majorID FROM Majors WHERE name=%s));"
            data = (first_name, last_name, gpa, classification, enrollment_status, dorm_name, major_name)
            db_connection = db.connect_to_database()
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=data)
            return get_students()

    # if the request is a PUT request, then update the student in the database
    elif request.method == "PUT":
        data = request.get_json()
        student_id = data["Student ID"]
        first_name = data["First Name"]
        last_name = data["Last Name"]
        gpa = data["GPA"]
        classification = data["Classification"]
        enrollment_status = data["Enrollment Status"]
        dorm_name = data["Dorm Name"]
        major_name = data["Major Name"]

        # if the dorm_name is null, then remove it from the query and set the dormID to null
        if dorm_name == "" or dorm_name == "NULL" or dorm_name == "null" or dorm_name == "None" or dorm_name == "none":
            query = "UPDATE Students SET firstName = %s, lastName = %s, GPA = %s, classification = %s, enrollmentStatus = %s, dormID = NULL, majorID = (SELECT majorID FROM Majors WHERE name=%s) WHERE studentID = %s;"
            data = (first_name, last_name, gpa, classification, enrollment_status, major_name, student_id)
            db_connection = db.connect_to_database()
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=data)
        else:
            query = "UPDATE Students SET firstName = %s, lastName = %s, GPA = %s, classification = %s, enrollmentStatus = %s, dormID = (SELECT dormID FROM Dorms WHERE name = %s), majorID = (SELECT majorID FROM Majors WHERE name=%s) WHERE studentID = %s;"
            data = (first_name, last_name, gpa, classification, enrollment_status, dorm_name, major_name, student_id)
            db_connection = db.connect_to_database()
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=data)
        return get_students()

@app.route("/delete/<string:tableName>/<int:id>", methods=["GET"])
def delete(tableName, id):
    """ """
    db_connection = db.connect_to_database()
    print("Deleting student with id: " + str(id))
    pKey = tableName[0].lower() + tableName[1:-1]
    query = f"DELETE FROM {tableName} WHERE {pKey}ID = %s"
    cur = db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
    return redirect(f"/{tableName}")


@app.route("/Courses", methods=["GET", "POST", "PUT"])
def Courses():
    db_connection = db.connect_to_database()
    def get_courses():
        db_connection = db.connect_to_database()
        query = "SELECT * FROM Courses ORDER BY courseID;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("courses.j2", courseList=results)

    # if the request is a GET request, then return the students page
    if request.method == "GET":
        return get_courses()

    # if the request is a POST request, then add the course to the database
    elif request.method == "POST":
        data = request.get_json()
        course_name = data["Course Name"]
        max_enrollment = data["Maximum Enrollment"]

        query = "INSERT INTO Courses (courseName, maxEnrollment) VALUES (%s, %s);"
        data = (course_name, max_enrollment)
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=data)

        return get_courses()

    # if the request is a PUT request, then update the course in the database
    elif request.method == "PUT":
        data = request.get_json()
        course_id = data["Course ID"]
        course_name = data["Course Name"]
        max_enrollment = data["Maximum Enrollment"]

        query = "UPDATE Courses SET courseName = %s, maxEnrollment = %s WHERE courseID = %s;"
        data = (course_name, max_enrollment, course_id)
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=data)

        return get_courses()

@app.route("/Majors", methods=["GET", "POST", "PUT"])
def Majors():
    db_connection = db.connect_to_database()
    def get_majors():
        db_connection = db.connect_to_database()
        query = "SELECT * FROM Majors ORDER BY majorID;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("majors.j2", majorData=results)

    # if the request is a GET request, then return the students page
    if request.method == "GET":
        return get_majors()

    # if the request is a POST request, then add the major to the database
    elif request.method == "POST":
        data = request.get_json()
        major_name = data["Major Name"]

        query = "INSERT INTO Majors (name) VALUES (%s);"
        data = (major_name,)
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=data)

        return get_majors()

    # if the request is a PUT request, then update the major in the database
    elif request.method == "PUT":
        data = request.get_json()
        major_id = data["Major ID"]
        major_name = data["Major Name"]

        query = "UPDATE Majors SET name = %s WHERE majorID = %s;"
        data = (major_name, major_id)
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=data)

        return get_majors()

@app.route("/Dorms", methods=["GET", "POST", "PUT"])
def Dorms():
    def get_dorms():
        db_connection = db.connect_to_database()
        query = "SELECT * FROM Dorms ORDER BY dormID;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("dorms.j2", dormData=results)

    # if the request is a GET request, then return the students page
    if request.method == "GET":
        return get_dorms()

    # if the request is a POST request, then add the dorm to the database
    elif request.method == "POST":
        data = request.get_json()
        print(data)
        dorm_name = data["Name"]
        dorm_address = data["Address"]
        max_occupancy = data["Max Occupancy"]

        query = "INSERT INTO Dorms (name, address, maxOccupancy) VALUES (%s, %s, %s);"
        data = (dorm_name, dorm_address, max_occupancy)
        db_connection = db.connect_to_database()
        try:
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=data)
        except Exception as e:
            print(f"An error occurred while executing the query: {str(e)}")
            abort(400, description=f"{str(e)}")

        return get_dorms()

    # if the request is a PUT request, then update the dorm in the database
    elif request.method == "PUT":
        data = request.get_json()
        print(data)
        dorm_id = data["Dorm ID"]
        dorm_name = data["Name"]
        dorm_address = data["Address"]
        max_occupancy = data["Max Occupancy"]

        query = "UPDATE Dorms SET name = %s, address = %s, maxOccupancy = %s WHERE dormID = %s;"
        data = (dorm_name, dorm_address, max_occupancy, dorm_id)
        db_connection = db.connect_to_database()
        try:
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=data)
        except Exception as e:
            print(f"An error occurred while executing the query: {str(e)}")
            abort(400, description=f"{str(e)}")
        return get_dorms()

@app.route("/MajorCourses", methods=["GET", "POST", "PUT"])
def MajorCourses():
    def get_major_courses():
        db_connection = db.connect_to_database()
        query = "SELECT majorCourse.majorCourseID, major.name AS MajorName, course.courseName AS CourseName FROM MajorCourses majorCourse JOIN Majors major ON majorCourse.majorID = major.majorID JOIN Courses course ON majorCourse.courseID = course.courseID ORDER BY majorCourseID;"
        db_connection = db.connect_to_database()
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        
        return render_template("Major_Courses.j2", majorCourseList=results)
    
    print(request.method)
    # if the request is a GET request, then return the students page
    if request.method == "GET":
        return get_major_courses()

    # if the request is a POST request, then add the major to the database
    elif request.method == "POST":
        data = request.get_json()
        major_name = data["Major Name"]
        course_name = data["Course Name"]

        query = "INSERT INTO MajorCourses (majorID, courseID) VALUES ((SELECT majorID FROM Majors WHERE name = %s), (SELECT courseID FROM Courses WHERE courseName = %s));"
        data = (major_name, course_name)
        db_connection = db.connect_to_database()
        try:
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=data)
        except Exception as e:
            print(f"An error occurred while executing the query: {str(e)}")
            abort(400, description=f"{str(e)}")
        return get_major_courses()

    # if the request is a PUT request, then update the major in the database
    elif request.method == "PUT":
        data = request.get_json()
        major_course_id = data["Major Course ID"]
        major_name = data["Major Name"]
        course_name = data["Course Name"]

        query = "UPDATE MajorCourses SET majorID = (SELECT majorID FROM Majors WHERE name = %s), courseID = (SELECT courseID FROM Courses WHERE courseName = %s) WHERE majorCourseID = %s;"
        data = (major_name, course_name, major_course_id)
        cursor = mysql.connection.cursor()
        cursor.execute(query, data)
        mysql.connection.commit()
        return get_major_courses()

@app.route("/StudentCourses", methods=["GET", "POST", "PUT"])
def studentCourses():
    def get_student_courses():
        query = "SELECT studentCourse.studentCourseID, CONCAT(student.firstName, ' ', student.lastName) as StudentName, course.courseName FROM StudentCourses studentCourse JOIN Students student ON studentCourse.studentID = student.studentID JOIN Courses course ON studentCourse.courseID = course.courseID ORDER BY studentCourseID;"
        db_connection = db.connect_to_database()
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("Students_Courses.j2", studentCourseList=results)

    # if the request is a GET request, then return the students page
    if request.method == "GET":
        return get_student_courses()

    # if the request is a POST request, then add the student to the database
    elif request.method == "POST":
        data = request.get_json()
        student_name = data["Student Name"]
        course_name = data["Course Name"]

        query = "INSERT INTO StudentCourses (studentID, courseID) VALUES ((SELECT studentID FROM Students WHERE CONCAT(firstName, ' ', lastName) = %s), (SELECT courseID FROM Courses WHERE courseName = %s));"
        data = (student_name, course_name)
        db_connection = db.connect_to_database()
        try:
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=data)
        except Exception as e:
            print(f"An error occurred while executing the query: {str(e)}")
            abort(400, description=f"{str(e)}")

        return get_student_courses()

    # if the request is a PUT request, then update the student in the database
    elif request.method == "PUT":
        data = request.get_json()
        student_course_id = data["Student Course ID"]
        student_name = data["Student Name"]
        course_name = data["Course Name"]

        query = "UPDATE StudentCourses SET studentID = (SELECT studentID FROM Students WHERE CONCAT(firstName, ' ', lastName) = %s), courseID = (SELECT courseID FROM Courses WHERE courseName = %s) WHERE studentCourseID = %s;"
        data = (student_name, course_name, student_course_id)
        db_connection = db.connect_to_database()
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=data)
        return get_student_courses()

@app.route('/resetDB')
def resetDB():
    db_connection = db.connect_to_database()
    cur = db_connection.cursor()
    with open('./database/DDL.sql', 'r') as f:
        sql_file = f.read()
    sql_commands = sql_file.split(';')

    for command in sql_commands:
        # Skip any command that is empty or only contains whitespace
        if command.strip() != '':
            cur.execute(command)
    cur.close()

    return redirect("/")

@app.route('/studentDropdown', methods=['GET'])
def studentDropdown():
    if request.method == 'GET':
        db_connection = db.connect_to_database()
        query = "SELECT CONCAT(student.firstName, ' ', student.lastName) as studentName FROM Students student ORDER BY studentID"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return jsonify(results)

@app.route('/courseDropdown', methods=['GET'])
def courseDropdown():
    if request.method == 'GET':
        db_connection = db.connect_to_database()
        query = "SELECT courseName FROM Courses ORDER BY courseID"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return jsonify(results)

@app.route('/majorDropdown', methods=['GET'])
def majorDropdown():
    if request.method == 'GET':
        db_connection = db.connect_to_database()
        query = "SELECT name FROM Majors ORDER BY majorID"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return jsonify(results)

@app.route('/dormDropdown', methods=['GET'])
def dormDropdown():
    if request.method == 'GET':
        db_connection = db.connect_to_database()
        query = "SELECT name FROM Dorms ORDER BY dormID"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return jsonify(results)

# Listener
if __name__ == "__main__":
    #app.run(host="flip4.engr.oregonstate.edu", port=54826, debug = True)
    app.run(port=54826, debug=True)


    
