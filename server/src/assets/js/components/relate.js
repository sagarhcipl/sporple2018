/**
 *
 * Actions for defining relation between two users.
 */


var modal = require('./modal');
var alertMessage = require('./alerts');
var dropDownMenu = require('./dropdown-menu');

var $btnGroup = undefined;

var _bindConnect = function($btn) {
    $btnGroup.each(function() {
        var $btnConnect = $btnGroup.find('.btn--connect');
        var userId = $btnConnect.attr('data-user-id');
        $btnGroup.find('.dropdown-menu__list-cont li').click(function() {
            $btnConnect.addClass('btn--loading');
            dropDownMenu.toggle($btnGroup);
            var type = $(this).attr('data-type');
            $.post('/relate/create/' + type + '/' + userId, function(response) {
                $btnConnect.removeClass('btn--loading');
                alertMessage.show(response);
            });
        });
    });
    // setup modal
    /*modal.setup(
        undefined,
        {
            title: 'Connect',
            classes: '',
            contentUrl: $btn.attr('data-url'),
            noBtns: true,
            callback: function() {
                setTimeout(function() {
                    _bindPopup($btn.attr('data-user-id'));
                    config.jQEles.$modal.focus();
                }, 50);
            }
        });
    modal.open();*/
};


var setup = function() {
    $btnGroup = $('.dropdown-btn-group');
    if ($btnGroup.length) {
        _bindConnect();
    }
};

module.exports = {
    setup: setup
};

