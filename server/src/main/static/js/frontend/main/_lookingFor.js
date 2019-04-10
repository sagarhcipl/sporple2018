$(function () {
    var $lookingFor = $('ul#looking-for'),
        totalLookingFor = $('ul#looking-for li').length,
        nextLookingForPage = 2,
        hasLookingForResults = true,
        foundLookingForResults,
        lookingForResultsLoading = false,
        $placeholder = '<li style="display:none"><div class="suggested-profile-placeholder"><img src="/images/suggested-profile-placeholder.jpg" alt="Sporple Suggested Profile"></div></li>';

    if (totalLookingFor < 10) {
        hasLookingForResults = false;
        $lookingFor.append($placeholder);
    }

    $lookingFor.off().on('click', 'a.remove', function (e) {
        e.preventDefault();

        var $this = $(e.target || e.currentTarget);

        if ((totalLookingFor <= 9 && hasLookingForResults)) {
            lookingForResultsLoading = true;
            if (totalLookingFor == 1) {
                nextLookingForPage = 1;
            }

            $.ajax({
                type: 'GET',
                url: looking_for_url,
                data: { page: nextLookingForPage },
                success: function (response) {
                    $lookingFor.append(response);
                    foundLookingForResults = $(response).filter('li').length;

                    if(foundLookingForResults > 9) {
                        hasLookingForResults = true;
                        nextLookingForPage++
                    } else {
                        $lookingFor.append($placeholder);
                        hasLookingForResults = false;
                    }

                    if (foundLookingForResults > 1) {
                        totalLookingFor += foundLookingForResults;
                    }

                    lookingForResultsLoading = false;
                },
                error: function(response) {}
            });
        } else if (totalLookingFor <= 7) {
            $('ul#looking-for a.remove').remove();
        }

        if (!lookingForResultsLoading) {
            totalLookingFor--;
            $this.parent('li').remove();
            $lookingFor.find('li:hidden:first').show();
        }
    });
});
