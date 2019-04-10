/*
 * Check if user can apply - modal functions
 *
 */

var modal = require('./modal');
var $sendMsgCont = undefined;
var open = function(html) {
    //close any previous modal
    modal.close();
    modal.setup(
        html,
        {
            title: 'Unable to Apply',
            classes: 'modal--send-message',
            noBtns: true,
            callback: function() {
                _bind();
            }
        }
    ); 

    //need to wait a little time because of adding the class sets off a width transition
    setTimeout(function() {
        modal.open();
    }, 300);
};

var _bind = function() {
    $sendMsgCont = config.jQEles.$modal.find('div.incomplete-profile');
    if( $sendMsgCont.length ){
        //bind cancel
        $sendMsgCont.find('#incomplete-profile__cancel-btn').click(function(e) {
            e.preventDefault();
            modal.close();
            mixpanel.track('cancel-incomplete');
        });

        $sendMsgCont.find('#incomplete-profile__go-btn').click(function(e) {
            mixpanel.track('goto-incomplete');
            // Do not prevent default.
        });
    }
};

module.exports = {
    open: open
};
