/*
 * Functionality for the Home page
 *
 */

var modal = require('./../../components/modal');

var $pageCont = undefined;
var $activityCont = undefined;

var _openMessageImg = function(imgUrl) {

    var modalHtml = '<div class="image-viewer__img-cont">' +
            '<img src="' + imgUrl + '" alt="">' +
        '</div>';

    //set up modal
    modal.setup(
        modalHtml,
        {
            classes: 'modal--image-viewer',
            noBtns: true,
            callback: function() {

                modal.open(); 
            }
        }
    );

};


var _bind = function() {

    //TODO: dont bind so high up. bind on the element and rerun bind when a new post is added
    $pageCont
        .on('click', 'a.attachment-link', function(e) {
            e.preventDefault();

            var imgUrl = $(this).attr('href');

            _openMessageImg(imgUrl);

        });

};


var setup = function() {
    
    $pageCont = $('section.page--home');
    $activityCont = $('#homepage_activity_container');

    if ($pageCont.length) {

        _bind();

    }

};


module.exports = {
    setup: setup
};
