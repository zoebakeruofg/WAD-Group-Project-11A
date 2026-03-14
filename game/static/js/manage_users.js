$(document).ready(function () {

    $(".disable-user-btn").click(function () {
        var row = $(this).closest(".manage-users-row");
        var userId = row.data("user-id");
        var statusCell = row.find(".user-status");

        // fake AJAX structure for now
        $.ajax({
            url: "#",
            type: "POST",
            data: {
                user_id: userId,
                action: "disable"
            },
            success: function () {
                statusCell.text("Disabled");
                statusCell.removeClass("active-status").addClass("disabled-status");

                $("#user-action-message")
                    .text("User " + userId + " has been disabled.")
                    .fadeIn()
                    .delay(1500)
                    .fadeOut();
            },
            error: function () {
                statusCell.text("Disabled");
                statusCell.removeClass("active-status").addClass("disabled-status");

                $("#user-action-message")
                    .text("User " + userId + " has been disabled.")
                    .fadeIn()
                    .delay(1500)
                    .fadeOut();
            }
        });
    });

    $(".enable-user-btn").click(function () {
        var row = $(this).closest(".manage-users-row");
        var userId = row.data("user-id");
        var statusCell = row.find(".user-status");

        // fake AJAX structure for now
        $.ajax({
            url: "#",
            type: "POST",
            data: {
                user_id: userId,
                action: "enable"
            },
            success: function () {
                statusCell.text("Active");
                statusCell.removeClass("disabled-status").addClass("active-status");

                $("#user-action-message")
                    .text("User " + userId + " has been enabled.")
                    .fadeIn()
                    .delay(1500)
                    .fadeOut();
            },
            error: function () {
                statusCell.text("Active");
                statusCell.removeClass("disabled-status").addClass("active-status");

                $("#user-action-message")
                    .text("User " + userId + " has been enabled.")
                    .fadeIn()
                    .delay(1500)
                    .fadeOut();
            }
        });
    });

});