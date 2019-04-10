/*
 * Media (cover image/showreal & images) functionality on profile page
 *
 */

//TODO: this whole module should be refactored HTML and logic.
//this is a hack at the mo
var modal = require('./../../components/modal');
var sendMessage = require('./../../components/send-message');

var $pageCont = undefined;
var $mediaCont = undefined;


var _viewListing = function($listingCont) {

    var agentId = $listingCont.attr('data-user-id');
    var content = $listingCont.clone()[0];

    modal.setup(
        content,
        {
            title: 'Listing',
            classes: 'model--agent-listing',
            btnText: 'Message',
            success: function() {

                sendMessage.open(agentId); 
            },
            callback: function() {

                modal.open(); 
            }
        }
    );

};

var _bind = function() {

    $pageCont
        .on('click', 'a.view, a.looking_for_more', function(e) {
            e.preventDefault();

            var $content = $($(this).attr('data-target'));

            _viewListing($content);

        });

};


var setup = function() {
    
    $pageCont = $('section.page--profile');
    $mediaCont = $('#profile__agent-media');

    if ($mediaCont.length) {

        _bind();

    }

};


module.exports = {
    setup: setup
};
