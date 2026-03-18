$(document).ready(function () {
    let resultData = sessionStorage.getItem("resultData");

    if (!resultData) {
        return;
    }

    let data = JSON.parse(resultData);

    if (!data.artwork_info) {
        return;
    }

    $("#art-title").text(data.artwork_info.title || "N/A");
    $("#art-year").text(data.artwork_info.year || "N/A");
    $("#art-artist").text(data.artwork_info.artist || "N/A");
    $("#art-country").text(data.artwork_info.country || "N/A");
    $("#art-continent").text(data.artwork_info.continent || "N/A");

    if (data.artwork_info.image_url) {
        $("#art-info-image")
            .attr("src", data.artwork_info.image_url)
            .show();

        $("#art-info-placeholder").hide();
    }
});