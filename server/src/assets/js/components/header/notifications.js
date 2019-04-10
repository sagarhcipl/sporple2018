/*
 * fetch notif count for messages and notifications
 *
 */


var $messageNotif = undefined;
var fetchInterval = 30000;

var _fetchMsgCount = function() {
    config.getUserData(function() {
        //on callback update notif marker
        _setMsgCount(config.userData.message);
    });
};

var _setMsgCount = function(data) {

    if (!! data) {

        var newMsgCount = data.nb_unread_messages;

        $messageNotif.html(newMsgCount);
        
        if (newMsgCount > 0) {
            $messageNotif.addClass('show');
        } else {
            $messageNotif.removeClass('show');
        }

    } else {

        $messageNotif.removeClass('show');
    }

};


var setup = function() {
    
    $messageNotif = $('#site-header__nav-notif--messages');

    if(config.userData && config.userData.user.is_authenticated && $messageNotif.length) {

        _setMsgCount(config.userData.message);

        //look for notifications on an interval
        setTimeout(function(){
            _fetchMsgCount();
        }, fetchInterval);

    }

};

module.exports = {
    setup: setup
};
