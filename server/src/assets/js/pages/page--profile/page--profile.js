/*
 * Functions greneric to all profile pages
 *
 */
'use strict'; 

var forms = require('./../../base/forms');
var profilePicEditor = require('./../../components/profile-pic-editor');
var media = require('./media');
var follow = require('./../../components/follow-user');
var twitter = require('./twitter');
var listings = require('./listings');
var modal = require('./../../components/modal');
var parsley = require('parsleyjs');
var gallery = require('./../../components/gallery');
require('./../../components/jquery-form');


var athlete = require('./athlete');
var club = require('./club');

var $pageCont = undefined;
var isOwner = undefined;

var _bindProfilePhoto = function() {
    var $uploadForm = $('#profile__photo-form');
    if ($uploadForm.length) {
        forms.bind();
        $uploadForm.parsley(config.parsleyDefaultConfig);
        $uploadForm.ajaxForm({
            success: function(data) {
                window.location.reload();
            },
            error: function(xhr, textStatus, error) {
                alert(error);
            }
        });
    
        var $uploadInput = $uploadForm.find('#profile__add-profile-photo'),
            $uploadBtn = $uploadForm.find('.edit-image');
        $uploadInput.change(function() {
            if ($uploadInput.parsley().isValid(true) && window.FileReader) {
                $uploadBtn.find('.fa-pulse').removeClass('hidden');
                var file = this.files[0];
                if (file) {
                    var editorOptions = {
                        inputPrefix: 'profile',
                        callback: function(){
                            $uploadForm.submit();
                        }
                    };
                    profilePicEditor.setup(file, editorOptions);
                } else {
                    $uploadBtn.find('.fa-pulse').addClass('hidden');
                }
            } else if ($uploadInput.parsley().isValid(true)) {
                $uploadForm.submit();
            }
        });
    }
};


var _bindUpload = function() {
    $('.upload-resizer').change(function () {
        var $this = $(this);
        if ($this.parsley().isValid(true) && window.FileReader) {
            var file = this.files[0];
            if (file) {
                var editorOptions = {
                    inputPrefix: $this.attr('data-prefix')
                };
                profilePicEditor.setup(file, editorOptions);
            }
        }
    });
};

var _bindGallery = function() {
    var $gallery = $('.gallery');
    if ($gallery.length) {
        var $tab = $gallery.find('.image-container'),
            $up = $gallery.find('.up-arrow'),
            $down = $gallery.find('.down-arrow');
        $up.click(function() {
            var current = $tab.scrollTop();
            $tab.animate({scrollTop: current-132}, 300);
        });
        $down.click(function() {
            var current = $tab.scrollTop();
            $tab.animate({scrollTop: current+132}, 300);
        });
    }

    // also setup upload form
    var $uploadForm = $('#profile__media-gallery-form');
    if ($uploadForm.length) {
        forms.bind();
        $uploadForm.parsley(config.parsleyDefaultConfig);
    
        var $uploadInput = $uploadForm.find('#profile__media-add-photo'),
            $uploadBtn = $uploadForm.find('.btn--info');
        $uploadInput.change(function() {
            if ($uploadInput.parsley().isValid(true)) {
                $uploadBtn.find('.loading').removeClass('hidden');
                $uploadForm.ajaxSubmit({
                    success: function(data) {
                        window.location.reload();
                    },
                    error: function(xhr, textStatus, error) {
                        alert(error);
                    }
                });
            }
        });
    }
};


var _bindInPlaceForm = function($btn, $container) {
    var $secondaryBtn = $container.find('.btn--secondary'),
        $primaryBtn = $container.find('#btn--submit');
    var cancelUrl = $btn.attr('data-cancel-url');

    $secondaryBtn.click(function() {
        $secondaryBtn.addClass('btn--loading');
        $container.load(cancelUrl);
        return false;
    });
    $('#add-another-client').click(function() {
        var $this = $(this);
        var url = $this.attr('data-url') || $this.attr('href');
        var $targetDiv = $('#' + $this.attr('data-target-id'));
        mixpanel.track('add-another-client');
        $targetDiv.load(url, function() {
            _bindInPlaceForm($this, $targetDiv);
        });
        return false;
    });
    _bindUpload();

    $form = $container.find('form');
    if ($form.length) {
        forms.wrapSelects();
        forms.bind();
        // form validation
        $form.parsley(config.parsleyDefaultConfig);
        $form.submit(function() {
            var $this = $(this);
            $primaryBtn.addClass('btn--loading');
            mixpanel.track($this.attr('id') || 'unknown');
            $this.ajaxSubmit({
                success: function(response) {
                    if (response == 'success') {
                        // TODO(ankit): Do something about success.
                        window.location.reload();
                    } else {
                        $container.html(response);
                        _bindInPlaceForm($btn, $container);
                    }
                },
                error: function(xhr, textStatus, error) {
                    alert(error);
                }
            });
            return false;
        });
    }
};


var _bindModalForm = function() {
    var $secondaryBtn = config.jQEles.$modal.find('.btn--secondary'),
        $primaryBtn = config.jQEles.$modal.find('#btn--submit');
    $secondaryBtn.click(function() {
        modal.close();
        return false;
    });
    var $form = config.jQEles.$modal.find('form');
    if ($form.length) {
        _multipleSelects();
        forms.wrapSelects();
        forms.bind();
        // form validation
        $form.parsley(config.parsleyDefaultConfig);

        $form.submit(function() {
            var $this = $(this);
            $primaryBtn.addClass('btn--loading');
            mixpanel.track($this.attr('id') || 'unknown');
            $this.ajaxSubmit({
                success: function(response) {
                    if (response == 'success') {
                        // TODO (ankit): Do something about success.
                        window.location.reload();
                    } else {
                        modal.refresh(response);
                        _bindModalForm();
                    }
                },
                error: function(xhr, textStatus, error) {
                    alert(error);
                }
            });
            return false;
        });

        $form.find("input[type='date']").datepicker();
    };
};


var _bindOpenForm = function() {
    // used for opportunity center
    var $form  = $('form.form');
    if ($form.length) {
        _multipleSelects();
        forms.wrapSelects();
        forms.bind();
        $form.parsley(config.parsleyDefaultConfig);
    }
};


var _bindInPlaceEdit = function() {
    $('.open-edit-inplace').click(function() {
        var $this = $(this);
        var url = $this.attr('data-url') || $this.attr('href');
        var $targetDiv = $('#' + $this.attr('data-target-id'));
        mixpanel.track('open-inplace');
        $targetDiv.load(url, function() {
            _bindInPlaceForm($this, $targetDiv);
        });
        return false;
    });
};


var _bindEditModals = function() {
    $('.open-edit-modal').click(function() {
        var $this = $(this);
        var url = $this.attr('data-url') || $this.attr('href'),
            title = $this.attr('data-title') || '';
        mixpanel.track(title);
    
        // close any previous modal
        modal.close();
        modal.setup(undefined, {
                title: title,
                contentUrl: url,
                noBtns: true,
                callback: function() {
                    _bindModalForm();
                }
        });

        setTimeout(function() {
            modal.open();
        }, 300);
        return false;
    });
};

var _bindDeleteModals = function() {
    var deleteHtml = '<p class"center">Are you sure you want to delete? This action cannot be undone. </p>';
    $('.delete').click(function() {
        var $this = $(this);
        var url = $this.attr('data-url') || $this.attr('href');
        // close any previous modal
        modal.close();
        modal.setup(deleteHtml, {
            title: 'Confirm Delete',
            noBtns: false,
            twoBtns: true,
            success: function() {
                config.jQEles.$modal.find('#modal__confirm').addClass('btn--loading');
                $.ajax({
                    type: 'GET',
                    url: url,
                    success: function(response) {
                        window.location.reload();
                    }
                });
            },
        });

        setTimeout(function() {
            modal.open();
        }, 300);
        return false;
    });
};


var _bindTeamEvents = function() {
    if ($pageCont.hasClass('club')) {
        $pageCont.find('.current-team').click(function() {
            var $this = $(this);
            if (!$this.hasClass('active')) {
                $('.past-team-list').addClass('hidden');
                $('.current-team-list').removeClass('hidden');
                $this.addClass('active');
                $pageCont.find('.past-team').removeClass('active');
            }
            return false;
        });
        $pageCont.find('.past-team').click(function() {
            var $this = $(this);
            if (!$this.hasClass('active')) {
                $('.past-team-list').removeClass('hidden');
                $('.current-team-list').addClass('hidden');
                $this.addClass('active');
                $pageCont.find('.current-team').removeClass('active');
            }
            return false;
        });
    }
};


var _addMultipleSelectValue = function(text, value, $mS, $pL, force) {

    var $multipleSelectOption = $mS.children('option[value="' + value + '"]');
    var multipleSelectId = $mS.attr('id');
    var selectedPositionHTML = '<li><a class="multiple-select-list__delete" data-target="{{VALUE}}" for="{{FORID}}"></a>{{TEXT}}</li>';

    //update UI list
    if($multipleSelectOption.length && (! $multipleSelectOption.attr('selected') || force) && !! value) {

        var positionLi = selectedPositionHTML.replace('{{VALUE}}', value).replace('{{TEXT}}', text).replace('{{FORID}}', multipleSelectId);

        //remove selected empty option
        $mS.children('option[value=""]').attr('selected', false);
        
        //select position on the hidden multiple select
        $multipleSelectOption.attr('selected', 'selected');

        //force change event for validation
        $mS.change();
        
        //add to DOM
        $pL.append(positionLi);
    }

};

var _deleteMultipleSelectValue = function($target) {
    var $li = $target.parent();
    var transitionDuration = 210;
    var $mS = $('#' + $target.attr('for'));

    //remove from the UI, animation or standard
    if(Modernizr.csstransforms && config.isModern()){

        $li.addClass('remove');

        setTimeout(function(){

            $li.remove();

        }, transitionDuration);
    }else{

        $li.remove();

    }

    //remove value from correct select element
    $mS
        .children('option[value="' + $target.data('target') + '"]').removeAttr('selected');

    //force validation
    $mS.parsley().validate(true);

};

var _multipleSelects = function() {
    var $multipleSelects = $('select[multiple]');

    for(var i = 0; i < $multipleSelects.length; i++){
        var $multipleSelect = $($multipleSelects[i]);
        var multipleSelectId = $multipleSelect.attr('id');
        var $selectedOptions = $multipleSelect.children('option:selected');
        var $singleSelect = $multipleSelect.clone();
        var $positionsList = $('#' + multipleSelectId + '-list');
        var singleSelectId = multipleSelectId+'--single';

        //remove any old versions
        if ($('#'+singleSelectId).length){

            var $oldSS = $('#'+singleSelectId);
            var $oldSSWrap = $oldSS.parent('.select-wrapper');

            if ($oldSSWrap.length){
                $oldSSWrap.remove();
            } else {
                $oldSS.remove();
            }
        }

        //set up single select with attributes and behaviours
        $singleSelect
            .attr({
                'id': singleSelectId,
                'class': 'remove-before-submit',
                'multiple': false,
                'for': multipleSelectId,
            })
            .removeAttr('name data-parsley-nonempty data-parsley-trigger data-parsley-maxcheck')
            .removeClass('no-style')

            .on('change', function() {
                var $this = $(this);
                var $forSelect = $('#' + $this.attr('for'));
                var $list = $('#' + $this.attr('for') + '-list');
                var text = this.options[this.selectedIndex].innerHTML;
                var value = this.options[this.selectedIndex].value;

                //update UI list
                _addMultipleSelectValue(text, value, $forSelect, $list);

                //reset single select
                $(this).prop('selectedIndex', 0);

            });

        //place single select in DOM
        if( config.getBreakpoint() === 'mobile' ) {

            $multipleSelect.after( $singleSelect );

        } else {

            $multipleSelect.after($singleSelect);

        }

        //clear & bind delete action to position list
        $positionsList
        .html('')
        .off('click', 'a.multiple-select-list__delete')
        .on('click', 'a.multiple-select-list__delete', function() {

            _deleteMultipleSelectValue($(this));
        });

        //add any currently selected vals to the list
        for(var j = 0; j < $selectedOptions.length; j++){

            var $option = $($selectedOptions[j]);
            
            _addMultipleSelectValue($option.text(), $option.val(), $multipleSelect, $positionsList, true);
        }
    }
};

var _setupCountrySelect = function() {

    //if we are larger then mob, set up autocomplete country list
    if(config.getBreakpoint() !== 'mobile' ){

        var $countrySelect = $('select.country-select');
        var $countryTextbox = undefined;

        $countrySelect.selectToAutocomplete({
            'copy-attributes-to-text-field': false
        });

        //save jQ object in cache
        $countryTextbox = $('input.ui-autocomplete-input');

        //add place holder so user knows what this is
        $countryTextbox.val('Choose your country');

    }

};


var _bind = function() {

    var $mainCol = $pageCont.find('div.page__main-col');
    //DO WE NEED TO BIND EDIT STUFF?
    if (isOwner) {

        //img cropper tool
        $('input.profile-pic-upload')
        .off('change')
        .change(function() {

            var _this = this;
            var prefix = $(this).attr('data-prefix') || 'profile';

            //if file and browser supports it, open cropper
            if($(this).parsley().isValid(true) && window.FileReader){
                
                var file = _this.files[0];

                if(file){
                    profilePicEditor.drawImage(file, prefix);
                }
            }

        });

    } else {
        //bind follow button if not owners page
        follow.setup();
    }
};

var setup = function() {

    $pageCont = $('div.profile-page');
    listings.setup();
    athlete.setup();
    club.setup();
    twitter.setup();
    gallery.setup();

    if ($pageCont.length){

        isOwner = $pageCont.hasClass('is-owner');
        //_bind();
        _bindGallery();
        _bindEditModals();
        _bindDeleteModals();
        _bindProfilePhoto();
        _bindInPlaceEdit();
        _bindTeamEvents();

        //setup media module
        media.setup();
        if (isOwner !== true) {
            follow.setup();
        } else {
            isOwner = false;
        }
    } else {
        _bindOpenForm();
    }

};


module.exports = {
    setup: setup
};
