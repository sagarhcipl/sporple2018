$(document).ready(function () {
    var $relatedProfilesList = $('ul.suggested-profiles-list'),
        $totalRelatedProfiles = $('ul.suggested-profiles-list li').length,
        $nextRelatedProfilesPage = 2,
        $hasRelatedProfiles = true,
        $foundRelatedProfiles,
        $profilesLoading = false,
        $profileplaceholder = '<li style="display:none"><div class="suggested-profile-placeholder"><img src="/images/suggested-profile-placeholder.jpg" alt="Sporple Suggested Profile"></div></li>';

    $relatedProfilesList.off().on("click", 'a.connection, a.remove', function (e) {
        e.preventDefault();

        var
            $this = $(e.target || e.currentTarget),
            $other_user_id = $this.data('user-id'),
            $current, $target;

        if ($this.hasClass('connection')) {
            if ($this.hasClass('follow')) {
                $current = 'follow';
                $target = 'unfollow';
                $url = follow_user_url;
            } else {
                $current = 'unfollow';
                $target = 'follow'
                $url = unfollow_user_url;
            }

            $.ajax({
                type: 'GET',
                url: $url,
                data: { user_id: $other_user_id },
                success: function (response) {
                    $this.html($target.slice(0,1).toUpperCase() + $target.slice(1)).removeClass($current).addClass($target);
                },
                error: function(response) {}
            });
        } else {
            if (($totalRelatedProfiles <= 5 && $hasRelatedProfiles)) {
                $profilesLoading = true;
                if ($totalRelatedProfiles == 1) {
                    $nextRelatedProfilesPage = 1;
                }

                $.ajax({
                    type: 'GET',
                    url: related_profiles_url,
                    data: { user_id: user_id, page: $nextRelatedProfilesPage, seed: seed },
                    success: function (response) {
                        $relatedProfilesList.append(response);
                        $foundRelatedProfiles = $(response).filter('li').length;

                        if($foundRelatedProfiles > 5) {
                            $hasRelatedProfiles = true;
                            $nextRelatedProfilesPage++
                        } else {
                            $relatedProfilesList.append($profileplaceholder);
                            $hasRelatedProfiles = false;
                        }

                        if ($foundRelatedProfiles > 1) {
                            $totalRelatedProfiles += $foundRelatedProfiles;
                        }

                        $profilesLoading = false;
                    },
                    error: function(response) {}
                });
            } else if ($totalRelatedProfiles <= 3) {
                $('a.remove').remove();
            }

            if (!$profilesLoading) {
                $totalRelatedProfiles--;
                $this.parent('li').remove();
                $relatedProfilesList.find('li:hidden:first').show();
            }
        }
    });
});
