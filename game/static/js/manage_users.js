$(document).ready(function () {
    function getCsrfToken() {
        let cookieValue = null;
        let cookies = document.cookie.split(";");

        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.startsWith("csrftoken=")) {
                cookieValue = cookie.substring("csrftoken=".length, cookie.length);
                break;
            }
        }

        return cookieValue;
    }

    $("#user-search").on("keyup", function () {
        let value = $(this).val().toLowerCase();

        $(".manage-users-row").each(function () {
            let username = $(this).find(".manage-username").text().toLowerCase();
            $(this).toggle(username.indexOf(value) > -1);
        });
    });

    $(".enable-user-btn").click(function () {
        let row = $(this).closest(".manage-users-row");
        let userId = row.data("user-id");

        $.ajax({
            url: "/manage-users/enable/" + userId + "/",
            type: "POST",
            headers: {
                "X-CSRFToken": getCsrfToken()
            },
            success: function (response) {
                if (response.success) {
                    row.find(".user-status")
                        .text("Active")
                        .removeClass("disabled-status")
                        .addClass("active-status");

                    $("#user-action-message")
                        .text("User enabled successfully.")
                        .fadeIn();
                } else {
                    $("#user-action-message")
                        .text(response.message)
                        .fadeIn();
                }
            },
            error: function () {
                $("#user-action-message")
                    .text("Something went wrong while enabling the user.")
                    .fadeIn();
            }
        });
    });

    $(".disable-user-btn").click(function () {
        let row = $(this).closest(".manage-users-row");
        let userId = row.data("user-id");

        $.ajax({
            url: "/manage-users/disable/" + userId + "/",
            type: "POST",
            headers: {
                "X-CSRFToken": getCsrfToken()
            },
            success: function (response) {
                if (response.success) {
                    row.find(".user-status")
                        .text("Disabled")
                        .removeClass("active-status")
                        .addClass("disabled-status");

                    $("#user-action-message")
                        .text("User disabled successfully.")
                        .fadeIn();
                } else {
                    $("#user-action-message")
                        .text(response.message)
                        .fadeIn();
                }
            },
            error: function () {
                $("#user-action-message")
                    .text("Something went wrong while disabling the user.")
                    .fadeIn();
            }
        });
    });
});