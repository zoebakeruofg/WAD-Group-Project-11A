$(document).ready(function () {
    function clearForm() {
        $("#artwork-id").val("");
        $("#artwork-title").val("");
        $("#artwork-artist").val("");
        $("#artwork-country").val("");
        $("#artwork-year").val("");
        $("#artwork-image").val("");
    }

    $("#add-artwork-btn").click(function () {
        clearForm();
        $("#artwork-form-wrapper").slideDown();
        $("#artwork-action-message").hide().text("");
    });

    $(document).on("click", ".edit-artwork-btn", function () {
        let row = $(this).closest(".manage-artworks-row");

        $("#artwork-id").val(row.data("artwork-id"));
        $("#artwork-title").val(row.find(".artwork-title").text().trim());
        $("#artwork-artist").val(row.find(".artwork-artist").text().trim());
        $("#artwork-country").val(row.find(".artwork-country").text().trim());
        $("#artwork-year").val(row.find(".artwork-year").text().trim());
        $("#artwork-image").val("");

        $("#artwork-form-wrapper").slideDown();
        $("#artwork-action-message").hide().text("");
    });

    $("#artwork-form").submit(function (e) {
        e.preventDefault();

        let artworkId = $("#artwork-id").val().trim();
        let title = $("#artwork-title").val().trim();
        let artist = $("#artwork-artist").val().trim();
        let country = $("#artwork-country").val().trim();
        let year = $("#artwork-year").val().trim();
        let imageFile = $("#artwork-image")[0].files[0];
        let csrfToken = $("input[name=csrfmiddlewaretoken]").val();

        let url = artworkId
            ? "/manage-artworks/edit/" + artworkId + "/"
            : "/manage-artworks/add/";

        let formData = new FormData();
        formData.append("title", title);
        formData.append("artist", artist);
        formData.append("country", country);
        formData.append("year", year);
        formData.append("csrfmiddlewaretoken", csrfToken);

        if (imageFile) {
            formData.append("image", imageFile);
        }

        $.ajax({
            url: url,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response.success) {
                    $(".no-artworks-row").remove();

                    if (artworkId) {
                        let row = $('.manage-artworks-row[data-artwork-id="' + artworkId + '"]');
                        row.find(".artwork-title").text(response.artwork.title);
                        row.find(".artwork-artist").text(response.artwork.artist);
                        row.find(".artwork-country").text(response.artwork.country);
                        row.find(".artwork-year").text(response.artwork.year);

                        $("#artwork-action-message")
                            .text("Artwork updated successfully.")
                            .fadeIn();
                    } else {
                        let newRow = `
                            <div class="manage-row manage-artworks-row" data-artwork-id="${response.artwork.id}">
                                <span class="artwork-id">${response.artwork.id}</span>
                                <span class="artwork-title">${response.artwork.title}</span>
                                <span class="artwork-artist">${response.artwork.artist}</span>
                                <span class="artwork-country">${response.artwork.country}</span>
                                <span class="artwork-year">${response.artwork.year}</span>
                                <span class="action-buttons">
                                    <button type="button" class="btn-edit edit-artwork-btn">Edit</button>
                                    <button type="button" class="btn-delete delete-artwork-btn">Delete</button>
                                </span>
                            </div>
                        `;
                        $(".manage-artworks-table").append(newRow);

                        $("#artwork-action-message")
                            .text("Artwork added successfully.")
                            .fadeIn();
                    }

                    clearForm();
                    $("#artwork-form-wrapper").slideUp();
                } else {
                    $("#artwork-action-message")
                        .text(response.message)
                        .fadeIn();
                }
            },
            error: function (xhr) {
                $("#artwork-action-message")
                    .text("Something went wrong while saving the artwork.")
                    .fadeIn();
                console.log(xhr.responseText);
            }
        });
    });

    $(document).on("click", ".delete-artwork-btn", function () {
        let row = $(this).closest(".manage-artworks-row");
        let artworkId = row.data("artwork-id");
        let csrfToken = $("input[name=csrfmiddlewaretoken]").val();

        $.ajax({
            url: "/manage-artworks/delete/" + artworkId + "/",
            type: "POST",
            data: {
                csrfmiddlewaretoken: csrfToken
            },
            success: function (response) {
                if (response.success) {
                    row.remove();

                    $("#artwork-action-message")
                        .text("Artwork deleted successfully.")
                        .fadeIn();
                } else {
                    $("#artwork-action-message")
                        .text(response.message)
                        .fadeIn();
                }
            },
            error: function (xhr) {
                $("#artwork-action-message")
                    .text("Something went wrong while deleting the artwork.")
                    .fadeIn();
                console.log(xhr.responseText);
            }
        });
    });
});