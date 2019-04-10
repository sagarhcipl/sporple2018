/*
 * Functions for sign up funnel
 *
 */

'use strict';

var $pageCont = undefined;
var _field_count = 0;
var _addMoreFields = function(field, $form) {
    $('#email' + field).keyup(function() {
        if ($(this).val() != '') {
            $form.append('<div class="row">' +
                '<div class="col-xs-12 col-md-6"><input type="email" id="email' + (field + 1) + '" name="emails[]" class="col-xs-11 col-centered"/></div>' +
                '<div class="col-xs-12 col-md-6"><input type="email" id="email' + (field + 2) + '" name="emails[]" class="col-xs-11 col-centered"/></div>' +
                '</div>');
            
            $(this).unbind('keyup');
            _addMoreFields(field + 2, $form);
        }
    });
};

var _bindFacebook = function () {
    var $fbBtn = $('#invite-fb-friends');
    $fbBtn.click(function() {
        if(!FB) {
            alert("No Facebook plugin found");
            return;
        }
        if(config.getBreakpoint() !== 'desktop' ){
            FB.ui({
                method: 'share',
                href: 'https://www.sporple.com/',
                quote: 'Join me on Sporple and find Sporting opportunities globally!',
            }, function(response){});
        } else {
            FB.ui({
                method: 'send',
                link: 'https://www.sporple.com/',
            });
        }
    });
};

var _bindForm = function() {
    var $form = $pageCont.find('form');
    if ($form.length) {
        _addMoreFields(4, $form);
        $pageCont.find('.send-invite').click(function() {
            $form.submit();
        });
    }
};

var setup = function() {
    $pageCont = $('section.invite-email');
    if ($pageCont.length) {
      _bindFacebook();
      _bindForm();
    }
};

module.exports = {
    setup: setup
};
