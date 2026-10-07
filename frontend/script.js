// ---------------- LOGIN ----------------

const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", function(event) {

        event.preventDefault();

        const username =
            document.getElementById("username").value;

        const password =
            document.getElementById("password").value;

        const error =
            document.getElementById("loginError");


        // Demo username and password

        if (username === "admin" && password === "1234") {

            // Save login status
            localStorage.setItem("loggedIn", "true");

            // Go to Home
            window.location.href = "home.html";

        } else {

            error.innerText =
                "Invalid username or password";

        }

    });

}


// ---------------- HOME → JOBS ----------------

function goToJobs() {

    window.location.href = "jobs.html";

}


// ---------------- LOGOUT ----------------

function logout() {

    localStorage.removeItem("loggedIn");

    window.location.href = "login.html";

}


// ---------------- APPLY JOB ----------------

function applyJob(jobName) {

    alert(
        "You have applied for " +
        jobName +
        " successfully!"
    );

}
