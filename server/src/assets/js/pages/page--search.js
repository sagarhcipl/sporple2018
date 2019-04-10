/*
 * Functionality for the Search results page
 *
 */

var modal = require('./../components/modal');
var follow = require('./../components/follow-user');

var $pageCont = undefined;

var _openShowreel = function(iframe) {

    var modalHtml = '<div class="image-viewer__img-cont">' +
        '<div class="iframe-cont aspect-wrap ratio-16-9">' + iframe + '</div>' +
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

    var $resultsList = $pageCont.find('ul.search-results');

    $resultsList
        .on('click', 'a.show-showreel', function(e) {
            e.preventDefault();

            var iframe = $(this).attr('data-video-iframe');

            _openShowreel(iframe);

        })
        .on('click', 'a.btn--follow', function(e) {
            e.preventDefault();

            var $btn = $(this);

            follow.toggle($btn);

        });

};


var setup = function() {
    
    $pageCont = $('section.page--search');

    if ($pageCont.length) {

        _bind();

    }

};


module.exports = {
    setup: setup
};
