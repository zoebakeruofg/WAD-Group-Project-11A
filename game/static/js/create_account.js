$(document).ready(function(){

    $("#account_type").change(function(){

        var selectedRole = $(this).val();

        if(selectedRole === "admin"){
            $("#guid-field").slideDown();
        } else {
            $("#guid-field").slideUp();
        }

    });

});


$(document).ready(function () {
    $("#account_type").change(function () {
        var selectedRole = $(this).val();

        if (selectedRole === "admin") {
            $("#guid-field").slideDown();
        } else {
            $("#guid-field").slideUp();
        }
    });

    $("#createAccountForm").submit(function (e) {
        var email = $("#email").val().trim();
        var username = $("#username").val().trim();
        var password = $("#password").val();
        var confirmPassword = $("#confirm_password").val();
        var role = $("#account_type").val();
        var guid = $("#guid").val().trim();

        // clear old errors
        $("#form-error-message").hide().text("");
        $("input, select").removeClass("input-error");

        if (email === "") {
            e.preventDefault();
            $("#form-error-message").text("Email is required.").fadeIn();
            $("#email").addClass("input-error");
            return;
        }

        if (username === "") {
            e.preventDefault();
            $("#form-error-message").text("Username is required.").fadeIn();
            $("#username").addClass("input-error");
            return;
        }

        if (password === "") {
            e.preventDefault();
            $("#form-error-message").text("Password is required.").fadeIn();
            $("#password").addClass("input-error");
            return;
        }

        if (confirmPassword === "") {
            e.preventDefault();
            $("#form-error-message").text("Please confirm your password.").fadeIn();
            $("#confirm_password").addClass("input-error");
            return;
        }

        if (password !== confirmPassword) {
            e.preventDefault();
            $("#form-error-message").text("Passwords do not match.").fadeIn();
            $("#password").addClass("input-error");
            $("#confirm_password").addClass("input-error");
            return;
        }

        if (role === "admin" && guid === "") {
            e.preventDefault();
            $("#form-error-message").text("GUID is required for admin accounts.").fadeIn();
            $("#guid").addClass("input-error");
            return;
        }
    });
});

