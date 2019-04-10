$(function () {
    var $profileForm = $(".agent_or_athlete_form"),
        $clubForm = $(".club_form");

    $profileForm.find("a, input").click(function (e) {
        var $hasAgentSelected = $("#agent_option").hasClass('selected'),
            $hasAthleteSelected = $("#athlete_option").hasClass('selected');

        if (!$hasAgentSelected && !$hasAthleteSelected) {
            $profileForm.find('span.error').fadeIn().fadeOut(5000);
            e.preventDefault();
        }
    });

    $clubForm.find("a, input").click(function (e) {
        var $hasClubSelected = $("#club_option").hasClass('selected');

        if (!$hasClubSelected) {
            $clubForm.find('span.error').fadeIn().fadeOut(5000);
            e.preventDefault();
        }
    });
});
