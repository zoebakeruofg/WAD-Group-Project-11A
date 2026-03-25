$(document).ready(function () {
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
        let csrfToken = $("input[name=csrfmiddlewaretoken]").val();

        $.ajax({
            url: "/manage-users/enable/" + userId + "/",
            type: "POST",
            data: {
                csrfmiddlewaretoken: csrfToken
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
        let csrfToken = $("input[name=csrfmiddlewaretoken]").val();

        $.ajax({
            url: "/manage-users/disable/" + userId + "/",
            type: "POST",
            data: {
                csrfmiddlewaretoken: csrfToken
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