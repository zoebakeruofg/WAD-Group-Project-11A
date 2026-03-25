$(document).ready(function () {
        $(document).on("contextmenu", "#play-art-image", function (e) {
        e.preventDefault();
    });

    $(document).on("dragstart", "#play-art-image", function (e) {
        e.preventDefault();
    });
    $("#continent").change(function () {
        let selectedContinent = $(this).val();

        $("#region").val("");
        $("#country").val("");

        $("#region option").each(function () {
            let continent = $(this).data("continent");

            if (!continent || selectedContinent === "" || continent === selectedContinent) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });

        $("#country option").show();
    });

    $("#region").change(function () {
        let selectedRegion = $(this).val();

        $("#country").val("");

        $("#country option").each(function () {
            let region = $(this).data("region");

            if (!region || selectedRegion === "" || region === selectedRegion) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    $("#guess-form").submit(function (e) {
        e.preventDefault();

        $("#play-message").hide().text("");
        $("#guess-form input, #guess-form select").removeClass("play-input-error");

        let continent = $("#continent").val().trim();
        let region = $("#region").val().trim();
        let country = $("#country").val().trim();
        let artist = $("#artist").val().trim();
        let year = $("#year").val().trim();
        let csrfToken = $("input[name=csrfmiddlewaretoken]").val();

        if (continent === "") {
            $("#play-message").text("Please select a continent.").fadeIn();
            $("#continent").addClass("play-input-error");
            return;
        }

        if (region === "") {
            $("#play-message").text("Please select a region.").fadeIn();
            $("#region").addClass("play-input-error");
            return;
        }

        if (country === "") {
            $("#play-message").text("Please select a country.").fadeIn();
            $("#country").addClass("play-input-error");
            return;
        }

        if (artist === "") {
            $("#play-message").text("Please enter an artist.").fadeIn();
            $("#artist").addClass("play-input-error");
            return;
        }

        if (year === "") {
            $("#play-message").text("Please enter a year.").fadeIn();
            $("#year").addClass("play-input-error");
            return;
        }

        $.ajax({
            url: "/submit-guess/",
            type: "POST",
            data: {
                continent: continent,
                region: region,
                country: country,
                artist: artist,
                year: year,
                csrfmiddlewaretoken: csrfToken
            },
            success: function (response) {
                if (response.success) {
                    sessionStorage.setItem("resultData", JSON.stringify(response));

                    $("#play-message")
                        .text("Your guess was submitted successfully.")
                        .fadeIn();

                    setTimeout(function () {
                        window.location.href = "/result/";
                    }, 600);
                } else {
                    $("#play-message").text(response.message).fadeIn();
                }
            },
            error: function () {
                $("#play-message").text("Something went wrong while submitting your guess.").fadeIn();
            }
        });
    });
});