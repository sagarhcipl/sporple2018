/*
 * Media (cover image/showreal & images) functionality on profile page
 *
 */

var parsley = require('parsleyjs');
var forms = require('./../../base/forms');
var profilePicEditor = require('./../../components/profile-pic-editor');
var $mediaCont = undefined;

var _bindEdit = function() {
    var $form = $('#profile__edit-cover-form');
    var $vidUrl = $('#profile__edit-vid-url');
    var coverOptions = {
        target: $mediaCont,
        success: function() {
            $mediaCont.removeClass('edit-mode');
            _bind();
        }
    };

    //bind functionality & validation to form
    if ($form) {
        forms.bind();
        $form.parsley(config.parsleyDefaultConfig);
        $form.ajaxForm(coverOptions);
    }

    $mediaCont
        //bind add video url 
        .off('click', '#profile__edit-vid-btn')
        .on('click', '#profile__edit-vid-btn', function(e) {
            e.preventDefault();
            
            var _$this = $(this);
            var vidUrl = $vidUrl.val();

            if (!! $.trim(vidUrl) && vidUrl.substring(0,4) !== 'http') {

                $vidUrl.val('https://' + vidUrl);
            }

            _$this.addClass('btn--loading');
            $form.submit();

        })

        //bind cover img cropper
        .off('change', '#profile__edit-img-file')
        .on('change', '#profile__edit-img-file', function(e) {

            var _this = this;
            var $btn = $(this).parent('.btn');
            var file = undefined;

            //reading file can take a while so set the loader
            $btn.addClass('btn--loading');

            //if file and browser supports it, open cropper
            if ($(this).parsley().isValid(true) && window.FileReader) {
                
                file = _this.files[0];

                if (file) {
                    //remove loader when file is read. then start again on submit
                    $btn.removeClass('btn--loading');

                    var editorOptions = {
                        inputPrefix: 'media_upload',
                        modalClassName: 'photo-crop--cover-pic',
                        aspectRatio: 16 / 9,
                        callback: function(){
                            $vidUrl.val('');
                            $btn.addClass('btn--loading');
                            $form.submit();
                        }
                    };
                    profilePicEditor.setup(file, editorOptions);
                } else {
                    $btn.removeClass('btn--loading');
                }

            } else if ($(this).parsley().isValid(true) && ! window.FileReader) {
                $vidUrl.val('');
                $form.submit();
            } else {
                $btn.removeClass('btn--loading');
            }
        })

        //cancel (Done) button
        .off('click', '#profile__edit-media-cancel')
        .on('click', '#profile__edit-media-cancel', function(e) {
            e.preventDefault();

            var urlPart = $(this).attr('href');

            $mediaCont
            .removeClass('edit-mode')
            .addClass('module--loading')
            .load('/profile/player_media', function() {
                
                $(this).removeClass('module--loading');
                _bind();
            });

        });
};

var _bind = function() {
    //edit button
    $('.profile__edit-media').click(function(e) {
        var $this = $(this);
        var url = $this.attr('href') || $this.attr('data-url');

        $mediaCont
        .addClass('module--loading')
        .load(
            url, 
            function() {
                $(this).removeClass('module--loading').addClass('edit-mode');
                _bindEdit();
            });
        return false;
    });

};


var setup = function() {
    $mediaCont = $('.profile-media');
    if ($mediaCont.length) {
        _bind();
    }
};


module.exports = {
    setup: setup
};
