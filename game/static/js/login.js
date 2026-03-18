$(document).ready(function () {
    $("#role").change(function () {
        let selectedRole = $(this).val();

        if (selectedRole === "admin") {
            $("#login-guid-field").slideDown();
        } else {
            $("#login-guid-field").slideUp();
        }
    });
});