/**
 * Citiation for the following code:
 * This module was adapted from the following source:
 * https://www.tutorialrepublic.com/codelab.php?topic=bootstrap&file=table-with-add-and-delete-row-feature
 * it provided the initial strcuture and it was modified to fit the needs of the project
 * except for the following functions that we developed:
 * 1. getStudentNames()
 * 2. getCourseNames()
 * 3. getMajorNames()
 * 4. getDormNames()
 * 5. validateInput()
 * 6. search bar functionality
 * 7. Custom add logic for StudentCourses and MajorCourses pages (including dropdowns) and Student and Dorms pages (including dropdowns)
 * 8. Custom edit logic for Students and Dorms pages (including dropdowns) and Student Courses and MajorCourses pages (including dropdowns)
 * 9. Custom get request logic for all page dropdowns (including StudentCourses and MajorCourses)
 * 10. Custom post request logic for all pages
 * 11. Custom put request logic for all pages
 * 12. Error handling for post and put requests and displaying the error message to the user
 */
$(document).ready(function(){
    // Initialize the counter with the highest current ID
    var highestId = parseInt($("table tbody tr:last-child td:first-child").text());

    $('[data-toggle="tooltip"]').tooltip();
    var saveButton = $("table td:nth-last-child(2)").html();
    var deleteButton = $("table td:last-child").html();
    $(".add-new").click(async function () {
        $(this).attr("disabled", "disabled");
        var index = $("table tbody tr:last-child").index();
        var numColumns = $("table").find("th").length - 2;
        var row = '<tr data-new-record="true">';

        //get the current page
        var currentPage = window.location.pathname.split('/')[1];

        if (currentPage === 'StudentCourses') {
            // Then, when adding a row:
            var id = highestId + 1;
            highestId = id;  // Update the counter
            row += '<td><input type="text" class="form-control" name="Student Course ID" id="studentId" value="' + id + '" style="background-color: #D3D3D3;" readonly></td>';
            row += '<td><select class="dropdown" name="Student Name" id="studentName" style="width: auto; padding: 10px;">';
            row += '<option value="">Select Student</option>';

            await getStudentNames().then((data) => {
                data.forEach((student) => {
                    row += '<option class="dropdown-item" value="' + student.studentName + '">' + student.studentName + '</option>';
                });
            });
            row += '<td><select class="dropdown" name="Course Name" id="courseName">';
            row += '<option value="">Select Course</option>';

            await getCourseNames().then((data) => {
                data.forEach((course) => {
                    row += '<option class="dropdown-item"  value="' + course.courseName + '">' + course.courseName + '</option>';
                });
                }
            );
        }
        else if(currentPage === 'MajorCourses') {
            // Then, when adding a row:
            var id = highestId + 1;
            highestId = id;  // Update the counter
            row += '<td><input type="text" class="form-control" name="Major Course ID" id="majorCourseId" value="' + id + '" style="background-color: #D3D3D3;" readonly></td>';
            row += '<td><select class="dropdown" name="Major Name" id="majorName">';
            row += '<option value="">Select Major</option>';

            await getMajorNames().then((data) => {
                data.forEach((major) => {
                    row += '<option class="dropdown-item" value="' + major.name + '">' + major.name + '</option>';
                });
            });
            row += '<td><select class="dropdown" name="Course Name" id="courseName">';
            row += '<option value="">Select Course</option>';

            await getCourseNames().then((data) => {
                data.forEach((course) => {
                    row += '<option class="dropdown-item" value="' + course.courseName + '">' + course.courseName + '</option>';
                });
                }
            );
        }
        else if(currentPage === 'Students') {
           for (var i = 0; i < numColumns; i++) {
                var columnName = $("table").find("th").eq(i).text();
                if (i == 0) {
                    // Then, when adding a row:
                    var id = highestId + 1;
                    highestId = id;  // Update the counter
                    row += '<td><input type="text" class="form-control" name="' + columnName + '" id="' + columnName + '" value="' + id + '" style="background-color: #D3D3D3;" readonly></td>';
                }
                // set the enrollment status column to a dropdown
                else if (i == 5) {
                    row += '<td><select class="dropdown" name="' + columnName + '" id="' + columnName + '">';
                    row += '<option value="">Select Status</option>';
                    row += '<option value="Full-time">Full Time</option>';
                    row += '<option value="Part-time">Part Time</option>';
                    row += '<option value="Graduated">Graduated</option>';
                }
                //set the major name column to a dropdown and fetch major names from /majorDropdown
                else if (i == 6) {
                    row += '<td><select class="dropdown" name="' + columnName + '" id="' + columnName + '">';
                    row += '<option value="">Select Major</option>';

                    await getMajorNames().then((data) => {
                        data.forEach((major) => {
                            row += '<option class="dropdown-item" value="' + major.name + '">' + major.name + '</option>';
                        });
                    });
                }
                // set the dorm name column to a dropdown and fetch dorm names from /dormDropdown
                else if (i == 7) {
                    row += '<td><select class="dropdown" name="' + columnName + '" id="' + columnName + '">';
                    row += '<option value="">Select Dorm</option>';

                    await getDormNames().then((data) => {
                        data.forEach((dorm) => {
                            row += '<option class="dropdown-item" value="' + dorm.name + '">' + dorm.name + '</option>';
                        });
                    });
                }
                else {
                    row += '<td><input type="text" class="form-control" name="' + columnName + '" id="' + columnName + '"></td>';
                }
            }
        }
        else if(currentPage === 'Dorms') {
             for (var i = 0; i < numColumns; i++) {
                var columnName = $("table").find("th").eq(i).text();
                if (i == 0) {
                    // Then, when adding a row:
                    var id = highestId + 1;
                    highestId = id;  // Update the counter
                    row += '<td><input type="text" class="form-control" name="' + columnName + '" id="' + columnName + '" value="' + id + '" style="background-color: #D3D3D3;" readonly></td>';
                }
                else if(i == 3) {
                    //set to number only input type
                    row += '<td><input type="text" class="form-control" name="' + columnName + '" id="' + columnName + '" oninput="validateInput(this)"></td>';
                }
                else {
                    row += '<td><input type="text" class="form-control" name="' + columnName + '" id="' + columnName + '"></td>';
                }

            }
        }
        else {
            for (var i = 0; i < numColumns; i++) {
                var columnName = $("table").find("th").eq(i).text();
                if (i == 0) {
                    // Then, when adding a row:
                var id = highestId + 1;
                highestId = id;  // Update the counter
                    row += '<td><input type="text" class="form-control" name="' + columnName + '" id="' + columnName + '" value="' + id + '" style="background-color: #D3D3D3;" readonly></td>';
                } else {
                    row += '<td><input type="text" class="form-control" name="' + columnName + '" id="' + columnName + '"></td>';
                }
            }
        }

        row += '<td>' + saveButton + '</td>';
        row += '<td>' + deleteButton + '</td>';
        row += '</tr>';
        $("table").append(row);
        $("table tbody tr").eq(index + 1).find(".add, .edit").toggle();
        $('[data-toggle="tooltip"]').tooltip();
    });
    // append row to table on add button click
   $(document).on("click", ".add", function(){
    var empty = false;
    var input = $(this).parents("tr").find('input[type="text"]');
    var data = {};
    var currentPage = window.location.pathname.split('/')[1]; // get the current page

    input.each(function(){
        // Skip validation for 'Dorm Name' field on 'Student' page
        if (currentPage === 'Students' && $(this).attr('name') === 'Dorm Name') {
            // if the dorm name is NULL, then set the value to NULL
            if (!$(this).val()) {
                data[$(this).attr('name')] = 'NULL';
                empty = true;
                return true; // continue to next iteration

            }
            else{
                data[$(this).attr('name')] = $(this).val();
                empty = true;
                return true; // continue to next iteration
            }
        }
        else if(!$(this).val()){
            $(this).addClass("error");
            empty = true;
        } else{
            $(this).removeClass("error");
            data[$(this).attr('name')] = $(this).val();
        }
        });
        var dropdown = $(this).parents("tr").find('select');
        dropdown.each(function(){
            if(!$(this).val()){
                $(this).addClass("error");
                empty = true;
            } else{
                $(this).removeClass("error");
                data[$(this).attr('name')] = $(this).val();
            }
        });
        console.log(data);
        $(this).parents("tr").find(".error").first().focus();
        if(!empty){
            input.each(function(){
                $(this).parent("td").html($(this).val());
            });
            $(this).parents("tr").find(".add, .edit").toggle();
            $(".add-new").removeAttr("disabled");

            var currentPage = window.location.pathname.split('/')[1];
            var isNewRecord = $(this).parents("tr").data('newRecord');
            var method = isNewRecord ? 'POST' : 'PUT';
            fetch('/' + currentPage, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            }).then((response) => {
                if (!response.ok && response.status === 400) {
                   return response.text().then((error) => {
                        // Create a new DOMParser
                        var parser = new DOMParser();
                        // Use the DOMParser to parse the error message
                        var doc = parser.parseFromString(error, "text/html");
                        // Extract the text within the <p> tags
                        var errorMessage = doc.querySelector("p").innerText;
                        // Display the error message
                        alert("An error occurred: " + errorMessage);
                        throw Error(errorMessage);
                    });
                }
                return response.text()
            }).then((res) => {
                if (res.status === 201) {
                    console.log("Post successfully created!")
                    // Reload the page
                    $ .ajax({
                url: '/' + currentPage,
                type: 'GET',
                success: function(result) {
                    // Do something with the result
                    window.location.href= '/' + currentPage;
                }
            });
                    

                }
            }).catch((error) => {
                console.log(error)
            })

            // Reset the data-new-record attribute
            $(this).parents("tr").data('newRecord', false);

            // Reload the page and convert the input fields back to table data

            //send a get request to the server to get the updated table
            $ .ajax({
                url: '/' + currentPage,
                type: 'GET',
                success: function(result) {
                    // Do something with the result
                    window.location.href= '/' + currentPage;
                }
            });




        }
    });
    // Edit row on edit button click
    $(document).on("click", ".edit", async function () {
        var currentPage = window.location.pathname.split('/')[1];
        //if the current page is StudentCourses, then we need to get the student and course names from the database to populate the dropdowns
        if (currentPage === 'StudentCourses') {
            var studentName = $(this).parents("tr").find("td:nth-child(2)").text();
            var courseName = $(this).parents("tr").find("td:nth-child(3)").text();
            var studentId = $(this).parents("tr").find("td:first-child").text();

            // change existing student ID to readonly input
            $(this).parents("tr").find("td:first-child").html('<input type="text" class="form-control" name="Student Course ID" id="studentId" value="' + studentId + '" style="background-color: #D3D3D3;" readonly>');
            // change existing student name to dropdown
            $(this).parents("tr").find("td:nth-child(2)").html('<select class="dropdown" name="Student Name" id="studentName">');
            var studentDropdown = $(this).parents("tr").find("td:nth-child(2)").find("select");
            await getStudentNames().then((data) => {
                data.forEach((student) => {
                    studentDropdown.append('<option value="' + student.studentName + '">' + student.studentName + '</option>');
                });
            });
            studentDropdown.val(studentName);

            // change existing course name to dropdown
            $(this).parents("tr").find("td:nth-child(3)").html('<select class="dropdown" name="Course Name" id="courseName">');
            var courseDropdown = $(this).parents("tr").find("td:nth-child(3)").find("select");
            await getCourseNames().then((data) => {
                data.forEach((course) => {
                    courseDropdown.append('<option value="' + course.courseName + '">' + course.courseName + '</option>');
                });
            });

            courseDropdown.val(courseName);
        }
        else if(currentPage === 'MajorCourses') {
            var majorName = $(this).parents("tr").find("td:nth-child(2)").text();
            var courseName = $(this).parents("tr").find("td:nth-child(3)").text();
            var majorCourseId = $(this).parents("tr").find("td:first-child").text();

            // change existing major course ID to readonly input
            $(this).parents("tr").find("td:first-child").html('<input type="text" class="form-control" name="Major Course ID" id="majorCourseId" value="' + majorCourseId + '" style="background-color: #D3D3D3;" readonly>');
            // change existing major name to dropdown
            $(this).parents("tr").find("td:nth-child(2)").html('<select class="dropdown" name="Major Name" id="majorName">');
            var majorDropdown = $(this).parents("tr").find("td:nth-child(2)").find("select");
            await getMajorNames().then((data) => {
                data.forEach((major) => {
                    majorDropdown.append('<option class="dropdown-item" value="' + major.name + '">' + major.name + '</option>');
                });
            });
            majorDropdown.val(majorName);

            // change existing course name to dropdown
            $(this).parents("tr").find("td:nth-child(3)").html('<select class="dropdown" name="Course Name" id="courseName">');
            var courseDropdown = $(this).parents("tr").find("td:nth-child(3)").find("select");
            await getCourseNames().then((data) => {
                data.forEach((course) => {
                    courseDropdown.append('<option class="dropdown-item" value="' + course.courseName + '">' + course.courseName + '</option>');
                });
            });

            courseDropdown.val(courseName);
        }
        else if(currentPage === 'Students') {
            var status = $(this).parents("tr").find("td:nth-child(6)").text();
            console.log(status);
             var majorName = $(this).parents("tr").find("td:nth-child(7)").text();
             var dormName = $(this).parents("tr").find("td:nth-child(8)").text();

            // change existing table data to input except the first column (id) and the last two columns (save and delete buttons)
            $(this).parents("tr").find("td:not(:first-child):not(:nth-last-child(2)):not(:last-child)").each(function () {
                //use the column name as the input name, so we can use it to update the database
                var index = $(this).index();
                var th = $(this).parents("tr").find("th").eq(index);
                var columnName = $(this).parents("table").find("thead th").eq($(this).index()).text();
                //if the first column is the id, then make it readonly
                $(this).html('<input type="text" class="form-control" name="'+columnName+'" value="' + $(this).text() + '">');
            });
            //get the column name of the first column
            var idColumn = $(this).parents("table").find("thead th").eq(0).text();
            //make the id readonly
            $(this).parents("tr").find("td:first-child").html('<input type="text" class="form-control" name="' + idColumn + '" value="' + $(this).parents("tr").find("td:first-child").text() + '" style="background-color: #D3D3D3;" readonly>');

            //change enrollment status to dropdown with three options
             $(this).parents("tr").find("td:nth-child(6)").html('<select class="dropdown" name="Enrollment Status" id="status">');
            var statusDropdown = $(this).parents("tr").find("td:nth-child(6)").find("select");

            statusDropdown.append('<option value="">Select Status</option>');
            statusDropdown.append('<option value="Full-time">Full Time</option>');
            statusDropdown.append('<option value="Part-time">Part Time</option>');
            statusDropdown.append('<option value="Graduated">Graduated</option>');

            statusDropdown.val(status);
            // change existing major name to dropdown and fetch major names from /majorDropdown
            $(this).parents("tr").find("td:nth-child(7)").html('<select class="dropdown" name="Major Name" id="majorName">');
            var majorDropdown = $(this).parents("tr").find("td:nth-child(7)").find("select");

            //add the default option
            majorDropdown.append('<option value="">Select Major</option>');
            await getMajorNames().then((data) => {
                data.forEach((major) => {
                    majorDropdown.append('<option class="dropdown-item" value="' + major.name + '">' + major.name + '</option>');
                });
            });
            majorDropdown.val(majorName);
            // change existing dorm name to dropdown and fetch dorm names from /dormDropdown
            $(this).parents("tr").find("td:nth-child(8)").html('<select class="dropdown" name="Dorm Name" id="dormName">');
            var dormDropdown = $(this).parents("tr").find("td:nth-child(8)").find("select");

            //add the default option
            dormDropdown.append('<option value="null">Select Dorm</option>');
            // add the null option
            dormDropdown.append('<option value="null">None</option>');
            await getDormNames().then((data) => {
                data.forEach((dorm) => {
                    dormDropdown.append('<option class="dropdown-item" value="' + dorm.name + '">' + dorm.name + '</option>');
                });
            });
            dormDropdown.val(dormName);
        }
        else if(currentPage === 'Dorms') {
            var dormName = $(this).parents("tr").find("td:nth-child(2)").text();
            var dormId = $(this).parents("tr").find("td:first-child").text();
            var address = $(this).parents("tr").find("td:nth-child(3)").text();
            var capacity = $(this).parents("tr").find("td:nth-child(4)").text();

            // change existing dorm ID to readonly input
            $(this).parents("tr").find("td:first-child").html('<input type="text" class="form-control" name="Dorm ID" id="dormId" value="' + dormId + '" style="background-color: #D3D3D3;" readonly>');
            // change existing dorm name to input
            $(this).parents("tr").find("td:nth-child(2)").html('<input type="text" class="form-control" name="Name" id="dormName" value="' + dormName + '">');
            // change existing address to input
            $(this).parents("tr").find("td:nth-child(3)").html('<input type="text" class="form-control" name="Address" id="address" value="' + address + '">');
            // change existing capacity to input
            $(this).parents("tr").find("td:nth-child(4)").html('<input type="text" class="form-control" name="Max Occupancy" id="capacity" value="' + capacity + '" oninput="validateInput(this)">');

        }
        else {
                // change existing table data to input except the first column (id) and the last two columns (save and delete buttons)
                $(this).parents("tr").find("td:not(:first-child):not(:nth-last-child(2)):not(:last-child)").each(function () {
                    //use the column name as the input name, so we can use it to update the database
                    var index = $(this).index();
                    var th = $(this).parents("tr").find("th").eq(index);
                    var columnName = $(this).parents("table").find("thead th").eq($(this).index()).text();
                    //if the first column is the id, then make it readonly
                    $(this).html('<input type="text" class="form-control" name="'+columnName+'" value="' + $(this).text() + '">');
                });
                //get the column name of the first column
                var idColumn = $(this).parents("table").find("thead th").eq(0).text();
                //make the id readonly
                $(this).parents("tr").find("td:first-child").html('<input type="text" class="form-control" name="' + idColumn + '" value="' + $(this).parents("tr").find("td:first-child").text() + '" style="background-color: #D3D3D3;" readonly>');
        }
        $(this).parents("tr").find(".add, .edit").toggle();
        $(".add-new").attr("disabled", "disabled");

    });
	// Delete row on delete button click
	$(document).on("click", ".delete", function(){
		var row = $(this).parents("tr");
		var studentId = row.find("td:first").text(); // assuming the student id is in the first column
		var currentPage = window.location.pathname.split('/')[1]; // get the current page name

		$.ajax({
        url: '/delete/'+ currentPage + '/' + studentId,
        type: 'GET',
        success: function(result) {
            // Do something with the result
            row.remove();
            $(".add-new").removeAttr("disabled");
        	}
    	});
	});
    // search bar functionality based on the second column
    $(".search-input").on("keyup", function() { // apply to all elements with class 'myInput'
    var value = $(this).val().toLowerCase();
    $("table tr").filter(function(index) { // pass the index to the filter function
        if(index !== 0) { // if it's not the first row
            $(this).toggle($('td', this).eq(1).text().toLowerCase().indexOf(value) > -1); // get the second column with eq(1)
        }
        });
    });
});

// async function to get the student names in the dropdown
async function getStudentNames() {
    const response = await fetch('/studentDropdown');
    const data = await response.json();
    return data;
}

// async function to get the course names in the dropdown
async function getCourseNames() {
    const response = await fetch('/courseDropdown');
    const data = await response.json();
    return data;
}

// async function to get the major names in the dropdown
async function getMajorNames() {
    const response = await fetch('/majorDropdown');
    const data = await response.json();
    return data;
}

// async function to get the dorm names in the dropdown
async function getDormNames() {
    const response = await fetch('/dormDropdown');
    const data = await response.json();
    return data;
}

function validateInput(input) {
    var value = input.value;
    if(isNaN(value)) {
        alert("Please enter a number");
       input.value = "";
    }
}