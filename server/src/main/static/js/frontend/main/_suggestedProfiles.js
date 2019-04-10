$(function () {
    var $suggestedProfiles = $('ul#suggestedProfiles'),
        totalSuggestedProfiles = $('ul#suggestedProfiles li').length,
        nextSuggestedProfilesPage = 2,
        hasSuggestedProfiles = true,
        foundSuggestedProfiles,
        suggestedProfilesLoading = false,
        $placeholder = '<li style="display:none"><div class="opportunity-profiles-placeholder"><img src="/images/suggested-profile-placeholder.jpg" alt="Sporple Suggested Profile"></div></li>';

    if (totalSuggestedProfiles < 10) {
        hasSuggestedProfiles = false;
        $suggestedProfiles.append($placeholder);
    }

    $suggestedProfiles.off().on('click', 'a.remove', function (e) {
        e.preventDefault();

        var $this = $(e.target || e.currentTarget);

        if ((totalSuggestedProfiles <= 9 && hasSuggestedProfiles)) {
            suggestedProfilesLoading = true;
            if (totalSuggestedProfiles == 1) {
                nextSuggestedProfilesPage = 1;
            }

            $.ajax({
                type: 'GET',
                url: suggested_profiles_url,
                data: { page: nextSuggestedProfilesPage },
                success: function (response) {
                    $suggestedProfiles.append(response);
                    foundSuggestedProfiles = $(response).filter('li').length;

                    if(foundSuggestedProfiles > 9) {
                        hasSuggestedProfiles = true;
                        nextSuggestedProfilesPage++;
                    } else {
                        hasSuggestedProfiles = false;
                    }

                    if (foundSuggestedProfiles > 1) {
                        totalSuggestedProfiles += foundSuggestedProfiles;
                    }

                    suggestedProfilesLoading = false;
                },
                error: function(response) {}
            });
        } else if (totalSuggestedProfiles <= 7) {
            $('ul#suggestedProfiles a.remove').remove();
        }

        if (!suggestedProfilesLoading) {
            totalSuggestedProfiles--;
            $this.parent('li').remove();
            $suggestedProfiles.find('li:hidden:first').show();
        }
    });
});
