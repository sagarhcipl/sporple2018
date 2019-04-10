/*
 * New style listings
 */

 'strict mode';

var setup = function() {
    $('.show-more-athlete-info').click(function() {
        $('.profile__stats.more_details').removeClass('hidden');
        $('.positions-small').addClass('hidden');
        $('.athlete-info-more').addClass('hidden');
        return false;
    });
    $('.hide-more-athlete-info').click(function() {
        $('.profile__stats.more_details').addClass('hidden');
        $('.positions-small').removeClass('hidden');
        $('.athlete-info-more').removeClass('hidden');
        return false;
    });
};

module.exports = {
    setup: setup
};
