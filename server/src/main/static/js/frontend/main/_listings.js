$(function () {
    var $listings = $('ul#listings'),
        totalListings = $('ul#listings li').length,
        nextListingsPage = 2,
        hasListings = true,
        foundListings,
        listingsLoading = false,
        $placeholder = '<li style="display:none"><div class="opportunity-profiles-placeholder"><img src="/images/suggested-profile-placeholder.jpg" alt="Sporple Suggested Profile"></div></li>';

    if (totalListings < 10) {
        hasListings = false;
        $listings.append($placeholder);
    }

    $listings.off().on('click', 'a.remove', function (e) {
        e.preventDefault();

        var $this = $(e.target || e.currentTarget);

        if ((totalListings <= 9 && hasListings)) {
            listingsLoading = true;
            if (totalListings == 1) {
                nextListingsPage = 1;
            }

            $.ajax({
                type: 'GET',
                url: listings_url,
                data: { page: nextListingsPage },
                success: function (response) {
                    $listings.append(response);
                    foundListings = $(response).filter('li').length;

                    if(foundListings > 9) {
                        hasListings = true;
                        nextListingsPage++;
                    } else {
                        hasListings = false;
                    }

                    if (foundListings > 1) {
                        totalListings += foundListings;
                    }

                    listingsLoading = false;
                },
                error: function(response) {}
            });
        } else if (totalListings <= 7) {
            $('ul#listings a.remove').remove();
        }

        if (!listingsLoading) {
            totalListings--;
            $this.parent('li').remove();
            $listings.find('li:hidden:first').show();
        }
    });
});
