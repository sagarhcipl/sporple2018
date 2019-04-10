/*
 * Send message modal functions
 *
 */

var $followBtns = undefined;

var toggleFollow = function($btn) {

    var userId = $btn.attr('data-user-id');
    var action = ($btn.hasClass('active')) ? unfollow_user_url : follow_user_url;

    if (! action || ! userId) {
        
        alert('Sorry, something is wrong. Please reload the page and try again.')
        
        return false;
    }

    $btn.addClass('btn--loading');

    $.post(
        action,
        { user_id: userId },
        function(data) {

            $btn.removeClass('btn--loading');

            if (data.status === 1) {

                $btn
                    .attr('data-action', 'unfollow')
                    .addClass('active')
                    .text('Following');

            } else if (data.status === 0) {

                $btn
                    .attr('data-action', 'follow')
                    .removeClass('active')
                    .text('Follow');
            }

        },
        'json'
    );

};

var bind = function() {

    $followBtns.click(function(e) {
        e.preventDefault();
        var $btn = $(this);
        toggleFollow($btn);
    });

};

var setup = function() {
    
    $followBtns = $('a.btn--follow, button.btn--follow');

    if ($followBtns.length) {
        bind();
    }

};


module.exports = {
    setup: setup,
    bind: bind,
    toggle: toggleFollow
};
