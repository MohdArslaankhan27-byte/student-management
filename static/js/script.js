const searchBtn = document.getElementById("searchBtn");
const searchBox = document.getElementById("searchBox");

searchBtn.addEventListener("click", function () {
    searchBox.classList.toggle("show");

    if (searchBox.classList.contains("show")) {
        searchBox.querySelector("input").focus();
    }
});

function openEditModal() {
    document.getElementById("editModal").style.display = "flex";
}

function closeEditModal() {
    document.getElementById("editModal").style.display = "none";
}
function showEditInput() {

    let field = document.getElementById("editField").value;
    let inputBox = document.getElementById("editInputBox");

    if (field === "") {
        inputBox.innerHTML = "";
        return;
    }

    if (field === "photo") {

        inputBox.innerHTML = `
            <input type="file" id="newPhoto" accept="image/*">

            <button type="button" onclick="updateProfile()">
                Update
            </button>
        `;

    } else {

        inputBox.innerHTML = `
            <input type="text" id="newValue"
                    placeholder="Enter new value">

            <button type="button" onclick="updateProfile()">
                Update
            </button>
        `;
    }
}
function updateProfile() {

    let field = document.getElementById("editField").value;
    let formData = new FormData();

    formData.append("field", field);

    if (field === "photo") {

        let photo = document.getElementById("newPhoto").files[0];

        if (!photo) {
            alert("Please select a photo");
            return;
        }

        formData.append("photo", photo);

    } else {

        let value = document.getElementById("newValue").value;

        if (value.trim() === "") {
            alert("Please enter a value");
            return;
        }

        formData.append("value", value);
    }

    fetch("/update_profile", {
        method: "POST",
        body: formData
    })
    .then(response => response.text())
    .then(data => {

        if (data === "success") {
            alert("Profile updated successfully");
            closeEditModal();
            location.reload();
        } else {
            alert(data);
        }

    })
    .catch(error => {
        console.error(error);
        alert("Something went wrong");
    });
}


document.addEventListener("DOMContentLoaded", function () {




    setTimeout(function () {

        const messages = document.querySelectorAll(".flash-message");

        messages.forEach(function (message) {
            message.remove();
        });

    }, 3000);

});


let searchTimer;

document.getElementById("studentSearch").addEventListener("input", function () {

    clearTimeout(searchTimer);

    const results = document.getElementById("student-results");

    results.innerHTML = "<p>Searching...</p>";

    searchTimer = setTimeout(function () {

        searchStudents();

    }, 3000);

});


function searchStudents() {

    const query = document.getElementById("studentSearch").value;

    const course = document.getElementById("courseFilter").value;

    const section = document.getElementById("sectionFilter").value;

    const semester = document.getElementById("semesterFilter").value;


    const url = "/search_students?q=" + encodeURIComponent(query)
              + "&course=" + encodeURIComponent(course)
              + "&section=" + encodeURIComponent(section)
              + "&semester=" + encodeURIComponent(semester);


    const results = document.getElementById("student-results");

    results.innerHTML = "<p>Searching...</p>";


    fetch(url)
        .then(response => response.json())
        .then(students => {

            results.innerHTML = "";


            if (students.length === 0) {

                results.innerHTML = "<p>No students found.</p>";

                return;
            }


            students.forEach(student => {

    const div = document.createElement("div");

    div.className = "student-card";

    div.innerHTML = `
        <div class="student-info">
            <h3>${student.name}</h3>
            <p>Course: ${student.course}</p>
            <p>Section: ${student.section}</p>
            <p>Semester: ${student.semester}</p>
        </div>

        <a href="/student/${student.id}" class="student-arrow">
            →
        </a>
    `;

    results.appendChild(div);

});

        })
        .catch(error => {

            console.log(error);

            results.innerHTML = "<p>Something went wrong.</p>";

        });
}

