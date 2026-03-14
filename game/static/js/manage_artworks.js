$(document).ready(function () {

    $("#add-artwork-btn").click(function () {
        $("#artwork-action-message")
            .text("Add Artwork form will be connected later.")
            .fadeIn()
            .delay(1500)
            .fadeOut();
    });

    $(".edit-artwork-btn").click(function () {
        var row = $(this).closest(".manage-artworks-row");
        var artworkId = row.data("artwork-id");

        $.ajax({
            url: "#",
            type: "POST",
            data: {
                artwork_id: artworkId,
                action: "edit"
            },
            success: function () {
                $("#artwork-action-message")
                    .text("Edit action selected for artwork " + artworkId + ".")
                    .fadeIn()
                    .delay(1500)
                    .fadeOut();
            },
            error: function () {
                $("#artwork-action-message")
                    .text("Edit action selected for artwork " + artworkId + ".")
                    .fadeIn()
                    .delay(1500)
                    .fadeOut();
            }
        });
    });

    $(".delete-artwork-btn").click(function () {
        var row = $(this).closest(".manage-artworks-row");
        var artworkId = row.data("artwork-id");

        $.ajax({
            url: "#",
            type: "POST",
            data: {
                artwork_id: artworkId,
                action: "delete"
            },
            success: function () {
                row.fadeOut(400, function () {
                    $(this).remove();
                });

                $("#artwork-action-message")
                    .text("Artwork " + artworkId + " has been deleted.")
                    .fadeIn()
                    .delay(1500)
                    .fadeOut();
            },
            error: function () {
                row.fadeOut(400, function () {
                    $(this).remove();
                });

                $("#artwork-action-message")
                    .text("Artwork " + artworkId + " has been deleted.")
                    .fadeIn()
                    .delay(1500)
                    .fadeOut();
            }
        });
    });

});