$(document).ready(function () {
    let resultData = sessionStorage.getItem("resultData");

    if (!resultData) {
        return;
    }

    let data = JSON.parse(resultData);

    $("#result-score-box").text(data.score + " / 100");

    $("#guess-continent").text(data.guesses.continent || "—");
    $("#guess-country").text(data.guesses.country || "—");
    $("#guess-artist").text(data.guesses.artist || "—");
    $("#guess-year").text(data.guesses.year || "—");

    $("#correct-continent").text(data.correct_answers.continent || "—");
    $("#correct-country").text(data.correct_answers.country || "—");
    $("#correct-artist").text(data.correct_answers.artist || "—");
    $("#correct-year").text(data.correct_answers.year || "—");
});