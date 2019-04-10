/**
 * Functions used for auto register
 */
'use strict';

var forms = require('./../base/forms');
var profilePicEditor = require('./../components/profile-pic-editor');
var parsley = require('parsleyjs');
require('./../components/jquery-form');

var $pageCont = undefined;

var _bindProfileUpload = function() {
    var $form = $pageCont.find('form');
    if ($form.length) {
        forms.bind();
        $form.parsley(config.parsleyDefaultConfig);
        var $uploadInput = $form.find('#upload-profile-image');
        $uploadInput.change(function() {
            if ($uploadInput.parsley().isValid(true) && window.FileReader) {
                var file = this.files[0];
                if (file) {
                    var editorOptions = {
                        inputPrefix: 'profile',
                    };
                    profilePicEditor.setup(file, editorOptions);
                }
            }
        });
    }
};
var setup = function() {
    $pageCont = $('div.autoregister');
    if ($pageCont.length) {
        _bindProfileUpload();
    }
};    

module.exports = {
    setup: setup
};
