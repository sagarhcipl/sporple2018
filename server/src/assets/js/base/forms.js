/*
 * Some global form functions
 *
 */
'use strict';

var _addCustomValidators = function() {

    window.Parsley
        .addValidator('nonempty', {
            requirementType: 'string',
            validateMultiple: function(value, requirement) {
                var combined = value.join('');

                if(! value.length) {
                    return false;
                }else{
                    return combined.length > 0;
                }

            }
        })
        .addValidator('noselect', {
            requirementType: 'string',
            validateString: function(value, requirement) {
                if (!value.length || value === '__None') {
                    return false;
                } else {
                    return true;
                }
            }
        })
        .addValidator('profilepic', {
            requirementType: 'string',
            validateString: function(value, requirement) {
                //requirement is field id
                var $field = $('#'+requirement);
                var files = $field[0].files;

                //if no files object but we have a value then this is and old browser (ie9) that doesnt support files obj
                if(!files && !$field.val()) {

                    return false;

                } else if(!files && !!$field.val()) {

                    var fileName = $field.val();

                    if( /(\.jpeg|\.jpg|\.png)/i.test(fileName.toLowerCase()) ) {

                        return true;

                    }else{

                        return false;
                    }
                
                } else {

                    var file = files[0];
                    var maxBytes = 5000000;

                    //is there a file present?
                    if(file && /^(image\/jpeg|image\/png)$/i.test(file.type) && file.size <= maxBytes) {

                        return true;

                    }else{

                        return false;
                    }

                }

            },
            messages: {
                en: 'Please use a .jpg or .png, 5mb or less'
            }
        });

};


var bind = function() {

    /*
     * Placeholder style labels. cross browser
     */
    $('input[type="text"], input[type="password"], input[type="email"], input[type="url"], input.has-placeholder')
    .focus(function() {

        $(this).parent('.form__row').addClass('form__field-focused');

    })
    .change(function() {
        
        if( $(this).val() === '' ){

            $(this).parent('.form__row').removeClass('form__field-dirty');

        }else if( !$(this).hasClass('form__field-dirty') ){

            $(this).parent('.form__row').addClass('form__field-dirty');
        }

    })
    .blur(function() {

        if( $(this).val() === '' ){

            $(this).parent('.form__row').removeClass('form__field-dirty form__field-focused');

        }else{

            $(this).parent('.form__row').addClass('form__field-dirty').removeClass('form__field-focused');
        }

    })

    //call change event to check if they are pre-populated
    .change()

    .siblings('label.form__label')
    .click(function() {
        $(this).siblings('input[type="text"], input[type="password"], input[type="email"], input[type="url"], input.has-placeholder').focus();
    });

};


/*
 * custom Select elements
 * wrap select elements in a div so we can style them properly
 */
var wrapSelects = function($elements) {

    var $selects = $elements || $('select:not(.no-style)');

    for(var i = 0; i < $selects.length; i++){

        var $wrapper = $(config.forms.selectWrapperHtml);
        var $select = $($selects[i]);
        var selectId = $select.attr('id');
        var wrapId = (selectId.length) ? selectId+'-wrap' : '';
        var selectClasses = $select.attr('class');
        var wrapClasses = ! selectClasses ? '' : selectClasses.replace(/ /g, '-wrap ') + '-wrap'; //append '-wrap' to end of all class names
        var title = $select.attr('data-label') || $select.find("option:selected").text() || '';

        if (! $select.parent('.select-wrapper').length){

            $wrapper
                .attr('id', wrapId)
                .addClass(wrapClasses)
                .prepend( $select.clone(true) )
                .children('span.select-wrapper__label').text(title);
            $wrapper.find('select').change(function() {
                var $this = $(this);
                var text = $this.find("option:selected").text();
                $this.siblings('span.select-wrapper__label').text(text);
            });

            $select.replaceWith($wrapper);

        }
    }

    var $fxSelects = $('select.cs-select');
    $fxSelects.each(function() {
        new SelectFx($(this).get(0));
    });
};


var setup = function() {

    if( config.isModern() ){

        wrapSelects();
    }

    bind();


    _addCustomValidators();

};

module.exports = {
    setup: setup,
    bind: bind,
    wrapSelects: wrapSelects
};
