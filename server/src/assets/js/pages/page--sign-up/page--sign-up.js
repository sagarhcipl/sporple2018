/*
 * Functions for sign up funnel
 *
 */

var profilePicEditor = require('./../../components/profile-pic-editor');
var modal = require('./../../components/modal');
require('./../../components/select-to-autocomplete');

module.exports = function() {

    var $progressCont = undefined;
    
    /*
     * set up step 3 form style
     * modern browsers get a smarter form
     */
    function moderniseForm3($form) {

        if(!$form.length || !config.isModern() ) return false;

        var hasCropped = false;
        var $profilePicCont = $('div.sign-up-form__step-1');
        var $fileUpload = $('#uploadFile');
        var $multipleSelect = $('select#registration_positions');
        var $singleSelect = $multipleSelect.clone();
        var $selectWrapper = $(config.forms.selectWrapperHtml);
        var $countrySelect = $('select#registration_address_country_id');
        var $countryTextbox = undefined;
        var $positionsList = $('#sign-up-form__positions-list');
        var $valueLists = $('ul.sign-up-form__value-list');
        var selectedPositionHTML = '<li><a class="sign-up-form__delete-position" data-target="{{VALUE}}"></a>{{TEXT}}</li>';
        var excludedFields = '.ui-autocomplete-input, #user_positions';
        var selectedValues = [];

        if(! window.File){
            $profilePicCont.addClass('show-file-input');
        }

        //add a single select that binds to the multiple select
        $singleSelect
            .attr({
                'id': 'user_positions',
                'name': 'user_positions',
                'multiple': false
            })
            .prepend($("<option></option>")
                    .attr("value", "")
                    .text("Select Your Positions(s)"))
            .removeAttr('data-parsley-nonempty data-parsley-trigger data-parsley-maxcheck')
            .removeClass('no-style')

            .on('change', function () {
                var text = this.options[this.selectedIndex].innerHTML;
                var value = this.options[this.selectedIndex].value;
                var $multipleSelectOption = $multipleSelect.children('option[value="' + value + '"]');


                //update UI list
                if($multipleSelectOption.length && ! $multipleSelectOption.attr('selected') && !! value) {

                    var positionLi = selectedPositionHTML.replace('{{VALUE}}', value).replace('{{TEXT}}', text);

                    //remove selected empty option
                    $multipleSelect.children('option[value=""]').attr('selected', false);
                    
                    //select position on the hidden multiple select
                    $multipleSelectOption.attr('selected', 'selected');

                    //force change event for validation
                    $multipleSelect.change();
                    
                    //add to DOM
                    $positionsList.append(positionLi);
                }

                //reset single select
                $(this).prop('selectedIndex', 0);
            });


            //wrap in select wrapper and add single select to DOM
            //@TODO: if we are dynamically added selcts a lot then we need to make this a function in the forms module
            $selectWrapper.prepend($singleSelect)
                .children('span.select-wrapper__label').text('Select your position(s)');

            $multipleSelect.after( 
                $selectWrapper.prepend($singleSelect)
            );


        //bind cropper tool
        $fileUpload.change(function() {
            var _this = this;
            //if file and browser supports it, open cropper
            if($(this).parsley().isValid(true) && window.FileReader){
                var file = _this.files[0];
                if(file){
                    profilePicEditor.drawImage(file, 'registration');
                    hasCropped = true;
                }
            }
        });


        $countrySelect.on('change', function () {
            var optionSelected = $("option:selected", this);
            var text = optionSelected.innerHTML;
            var value = optionSelected.value;
            var countryLi = selectedPositionHTML.replace('{{VALUE}}', value).replace('{{TEXT}}', text);
        });


        $countrySelect.selectToAutocomplete({
            'copy-attributes-to-text-field': false
        });

        //save jQ object in cache
        $countryTextbox = $('input.ui-autocomplete-input');

        //add place holder so user knows what this is
        $countryTextbox.val('Choose your country');

        //bind delete action to position list
        $valueLists.on('click', 'a.sign-up-form__delete-position', function () {
            var $li = $(this).parent();
            var transitionDuration = 210;

            //remove from the UI, animation or standard
            if(Modernizr.csstransforms && config.isModern() ){
                $li.addClass('remove');
                setTimeout(function(){
                    $li.remove();
                }, transitionDuration);
            }else{
                $li.remove();
            }

            //remove value from correct select element
            if( $li.parent('ul').is('#sign-up-form__positions-list') ){
                $multipleSelect
                    .children('option[value="' + $(this).data('target') + '"]').removeAttr('selected');

                //force validation
                $multipleSelect.parsley().validate(true);
            }else{
                $countrySelect
                    .children('option[value="' + $(this).data('target') + '"]').attr('selected', false);

                //remove from autocomplete textbox if present
                if(!!$countryTextbox && $countryTextbox.length){
                    $countryTextbox.val('');
                }

                //force change event for validation
                $countrySelect.parsley().validate(true);
            }   
        });

        //set validation
        $form.parsley(config.parsleyDefaultConfig);

        //we have to remove the added fields (i.e. single position select) before we submit the form
        $form.submit(function () {
            //update ui to loading
            $(this).children('#btn--submit').addClass('btn--loading');
 
            if($('#user_positions').length) {
               $singleSelect.remove();
               $form.submit();
               return false; 
            }
        });
    }


    $(function() {
        'use strict';

        //save jq elements
        $progressCont = $('#sign-up__progress');

        //can we modernise the form?
        moderniseForm3( $('#sign-up-form--3') );
    });
};
