/*
 * Functionality for the Connections page
 *
 */

var follow = require('./../components/follow-user');

var $pageCont = undefined;


var _bind = function() {

    var $resultsList = $pageCont.find('#connection-list');

    $resultsList
        .on('click', 'a.btn--follow', function(e) {
            e.preventDefault();

            var $btn = $(this);

            follow.toggle($btn);

        });

};

var setup = function() {
    
    $pageCont = $('section.page--connections');

    if ($pageCont.length) {

        _bind();

    }

};


module.exports = {
    setup: setup
};
