/*
 * Functions greneric to all profile pages
 *
 */
'use strict'; 

var forms = require('./../../base/forms');
require('./../../components/jquery-form');

var $widget = undefined;

var _bind = function() {
    var $editBtn = $('#profile__edit-twitter');
    var $form = $('#profile__twitter-form');

    if ($editBtn.length){
        $editBtn.on('click', function (event) {
            $widget.load(
                $(this).attr('data-url'), 
                function() {
                    _bind();
                }
            );
            return false;
        });
    }

    if ($form.length){
        forms.bind();
        $form.parsley(config.parsleyDefaultConfig);
        $form.submit(function() {
            var twitter_account = $('#twitter_account').val();
            $(this)
                .children('#profile__twitter-submit').addClass('btn--loading');

            $(this).ajaxSubmit({
                success: function(data) {
                    window.location.reload();
                },
                error: function(data) {
                    $widget.html(data);
                    _bind();
                }
            }); 
            return false;
        }); 
    }
}

var setup = function() {
    $widget = $('.twitter');
    if ($widget.length){
        _bind();
    }
};


module.exports = {
    setup: setup
};
