$(document).ready(function () {
    window.oldBrowserMode = false;

    if (!('FileList' in window) || typeof window.FileList === 'undefined') {
        window.oldBrowserMode = true;
    }

    registration.init();
});

var registration = {

    init: function () {
        registration.bindEventHandlers();

        $('#lifestyle_selection').show();
        $('#registration_lifestyle_id').parent().hide();

        $('#sport_selection').show();
        $('#registration_sport_id').parent().hide();

        registration.initUserPositionList();

        var $registrationHasAgentElement = $('#registration_has_agent_1');

        if (!$registrationHasAgentElement.is(":checked")) {
            registration.enable_fields(false, ['registration_agent_firstname', 'registration_agent_lastname', 'registration_agent_email']);
        }

        $('#registration_form_submit').click(function (event) {
            var age = registration.calculateAge();
            if (age < 13) {
                $('#popup').bPopup({
                    contentContainer: '#popupcontent',
                    loadUrl: '/registration/ageLimit',
                    loadCallback: function () {
                        return undefined;
                    },
                    onClose: function () {
                        return undefined;
                    }
                });

                event.preventDefault();

                return false;
            }

            return true;
        });
    },

    bindEventHandlers: function () {
        //select_option(this, 'registration_lifestyle_id', 'school');return false;
        $('#lifestyle_selection_school').on('click', function () {
            registration.select_option(this, 'registration_lifestyle_id', '1');
            return false;
        });
        $('#lifestyle_selection_college').on('click', function () {
            registration.select_option(this, 'registration_lifestyle_id', '2');
            return false;
        });
        $('#lifestyle_selection_occupation').on('click', function () {
            registration.select_option(this, 'registration_lifestyle_id', '3');
            return false;
        });

        $('#sport_selection_rugby').on('click', function () {
            registration.select_sport_option(this, 'registration_sport_id', '2');
            return false;
        });
        $('#sport_selection_football').on('click', function () {
            registration.select_sport_option(this, 'registration_sport_id', '1');
            return false;
        });
        $('#sport_selection_baseball').on('click', function () {
            registration.select_sport_option(this, 'registration_sport_id', '3');
            return false;
        });
        $('#sport_selection_basketball').on('click', function () {
            registration.select_sport_option(this, 'registration_sport_id', '4');
            return false;
        });

        $('#registration_user_position_list').on('change', function () {
            var text = this.options[this.selectedIndex].innerHTML,
                value = this.options[this.selectedIndex].value;

            registration.add_position(text, value);
            $('#registration_user_position_list').prop('selectedIndex', -1);
            return false;
        });

        $('#registration_has_agent_0').on('click', function () {
            registration.enable_fields(false, ['registration_agent_firstname', 'registration_agent_lastname', 'registration_agent_email']);
        });

        $('#registration_has_agent_1').on('click', function () {
            registration.enable_fields(true, ['registration_agent_firstname', 'registration_agent_lastname', 'registration_agent_email']);
        });

        $('#registration_image').on('change', function () {
            if (window.oldBrowserMode) {
                oldBrowserFileSelectHandler();
            } else {
                fileSelectHandler();
            }
        });
    },

    initUserPositionList: function () {
        //add positions for all selected
        $('#registration_user_position_list > option:selected').each(function () {
            registration.add_position($(this).text(), $(this).val());
            $(this).removeAttr('selected');
        });

        //UNSELECT ALL VALUES
        $('#registration_user_position_list').removeAttr('multiple');
        $('#registration_user_position_list').prop('selectedIndex', -1);
    },
    select_option: function (el, field, value) {
        for (var b = 0; b < el.parentNode.parentNode.children.length; b++) {
            el.parentNode.parentNode.children[b].children[0].className = (el.parentNode.parentNode.children[b].children[0] == el ? 'selected' : '');
        }

        $('#' + field).val(value);
    },
    select_sport_option: function (el, field, value) {
        if ($('#' + field).attr('multiple')) {
            //has multiple so we have to turn it off / on
            $(el).toggleClass('selected');

            var data = $('#' + field).val();
            if (!data) {
                data = new Array();
            }
            if (jQuery.inArray(value, data) >= 0) {
                data.splice($.inArray(value, data), 1);
            }
            else {
                data.push(value);
            }
            $('#' + field).val(data);
        } else {
            registration.select_option(el, field, value);
        }
    },

    add_position: function (text, value) {
        var positions = $('#positions');


        var add = true;
        if ($('#positions :input[value="' + value + '"]').length) {
            add = false;
        }

        if (add) {
            positions.append('<span><input type="hidden" name="registration[user_position_list][]" value="' + value + '"/><a href="#" >x</a> ' + text + '</span>');
            positions.find('a').last().on('click', function () {
                registration.remove_position(this);
                return false;
            });
        }

    },

    remove_position: function (el) {
        el.parentNode.parentNode.removeChild(el.parentNode);
    },

    enable_fields: function (enable, fields) {
        for (var a in fields) {
            var field = document.getElementById(fields[a]);
            if (field) {
                field.disabled = enable ? '' : 'disabled';
            }
        }
    },
    calculateAge: function () {
        var birthYear = $('#registration_birthday_year').val(),
            birthMonth = $('#registration_birthday_month').val(),
            birthDay = $('#registration_birthday_day').val(),
            todayDate = new Date(),
            todayYear = todayDate.getFullYear(),
            todayMonth = todayDate.getMonth(),
            todayDay = todayDate.getDate(),
            age = todayYear - birthYear;

        if (todayMonth < (birthMonth - 1)) {
            age--;
        }

        if ((birthMonth - 1) === todayMonth && todayDay < birthDay) {
            age--;
        }
        return age;
    }
}


// convert bytes into friendly format
function bytesToSize(bytes) {
    var sizes = ['Bytes', 'KB', 'MB'];
    if (bytes == 0) return 'n/a';
    var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
    return (bytes / Math.pow(1024, i)).toFixed(1) + ' ' + sizes[i];
};

// clear info by cropping (onRelease event handler)
function clearInfo() {
    $('#profile_image_w').val('');
    $('#profile_image_h').val('');
};

// get selected file
function fileSelectHandler() {
    var oFile = $('#registration_image')[0].files[0],
        jcrop_api;

    $('#popup .follow').click(function () {
        $('#popup').bPopup().close();
    });

    $('#popup').css({'display': 'block'});
    $('#popup').bPopup({
        position: [$(window).width() / 2 - $('#popup').width() / 2, 50],
        positionStyle: 'fixed',
        onClose: function () {
            if (typeof jcrop_api !== 'undefined') {
                jcrop_api.destroy();
            }
        }
    });

    // check for image type (jpg and png are allowed)
    var rFilter = /^(image\/jpeg|image\/png)$/i;
    if (!rFilter.test(oFile.type)) {
        $('.error').html('Please select a valid image file (jpg and png are allowed)').show();
        return;
    }

    // check for file size
    if (oFile.size > 8250 * 1024) {
        $('.error').html('You have selected too big file, please select a one smaller image file').show();
        return;
    }

    // preview element
    var oImage = document.getElementById('preview');

    // prepare HTML5 FileReader
    var oReader = new FileReader();
    oReader.onload = function (e) {

        // e.target.result contains the DataURL which we can use as a source of the image
        oImage.src = e.target.result;
        document.getElementById('picture').src = e.target.result;
        $('.profile figure').addClass('thumbnail_selected');

        oImage.onload = function () { // onload event handler

            // display some basic image info
            var sResultFileSize = bytesToSize(oFile.size);
            $('#filesize').val(sResultFileSize);
            $('#filetype').val(oFile.type);
            $('#filedim').val(oImage.naturalWidth + ' x ' + oImage.naturalHeight);

            // Create variables (in this scope) to hold the Jcrop API and image size
            var jcrop_api, boundx, boundy;

            // destroy Jcrop if it is existed
            if (typeof jcrop_api !== 'undefined') {
                jcrop_api.destroy();
            }

            var $regImageX1 = $('#registration_image_x1'),
                $regImageY1 = $('#registration_image_y1'),
                $regImageX2 = $('#registration_image_x2'),
                $regImageY2 = $('#registration_image_y2'),
                $regImageW = $('#registration_image_w'),
                $regImageH = $('#registration_image_h');

            // update info by cropping (onChange and onSelect events handler)
            updateInfo = function (e) {
                $regImageX1.val(parseInt(e.x));
                $regImageY1.val(parseInt(e.y));
                $regImageX2.val(parseInt(e.x2));
                $regImageY2.val(parseInt(e.y2));
                $regImageW.val(parseInt(e.w));
                $regImageH.val(parseInt(e.h));

                var rx = 110 / parseInt(e.w),
                    ry = 110 / parseInt(e.h);

                $('#picture').css({
                    width: Math.round(rx * oImage.naturalWidth) + 'px',
                    height: Math.round(ry * oImage.naturalHeight) + 'px',
                    marginLeft: '-' + Math.round(rx * parseInt(e.x)) + 'px',
                    marginTop: '-' + Math.round(ry * parseInt(e.y)) + 'px'
                });

            };

            // initialize Jcrop
            $('#preview').Jcrop({
                minSize: [32, 32], // min crop size
                aspectRatio: 1, // keep aspect ratio 1:1
                bgFade: true, // use fade effect
                bgOpacity: .3, // fade opacity
                onChange: updateInfo,
                onSelect: updateInfo,
                onRelease: clearInfo,
                boxWidth: 450,
                boxHeight: 400,
                setSelect: [0, 0, Math.min(oImage.naturalWidth, oImage.naturalHeight), Math.min(oImage.naturalWidth, oImage.naturalHeight)],
                allowSelect: false
            }, function () {
                // Store the Jcrop API in the jcrop_api variable
                jcrop_api = this;
            });
        };
    };

    // read selected file as DataURL
    oReader.readAsDataURL(oFile);
}

function oldBrowserFileSelectHandler() {
    if ($('#registration_image').val() === '') {
        return;
    }

    $('#registration_form').ajaxSubmit({
        data: {'oldBrowserMode' : true},
        clearForm: false,
        resetForm: false,
        success: function (responseText, statusText, xhr, $form) {
            var oImage = document.getElementById('preview'),
                jcrop_api;

            oImage.src = responseText;
            document.getElementById('picture').src = responseText;

            $('#popup .follow').click(function () {
                $('#popup').bPopup().close();
            });

            $('#popup').css({'display': 'block'});
            $('#popup').bPopup({
                position: [$(window).width() / 2 - $('#popup').width() / 2, 50],
                positionStyle: 'fixed',
                onClose: function () {
                    if (typeof jcrop_api !== 'undefined') {
                        jcrop_api.destroy();
                    }
                }
            });

            var $regImageX1 = $('#registration_image_x1'),
                $regImageY1 = $('#registration_image_y1'),
                $regImageX2 = $('#registration_image_x2'),
                $regImageY2 = $('#registration_image_y2'),
                $regImageW = $('#registration_image_w'),
                $regImageH = $('#registration_image_h');

            updateInfo = function (e) {
                $regImageX1.val(parseInt(e.x));
                $regImageY1.val(parseInt(e.y));
                $regImageX2.val(parseInt(e.x2));
                $regImageY2.val(parseInt(e.y2));
                $regImageW.val(parseInt(e.w));
                $regImageH.val(parseInt(e.h));

                var rx = 110 / parseInt(e.w),
                    ry = 110 / parseInt(e.h);
                $('#picture').css({
                    width: Math.round(rx * oImage.naturalWidth) + 'px',
                    height: Math.round(ry * oImage.naturalHeight) + 'px',
                    marginLeft: '-' + Math.round(rx * parseInt(e.x)) + 'px',
                    marginTop: '-' + Math.round(ry * parseInt(e.y)) + 'px'
                });

            };

            oImage.onload = function() {
                var $minDimension = Math.min(oImage.naturalWidth, oImage.naturalHeight),
                    $selectionWidth = $minDimension/2,
                    $selectionHeight = $minDimension/2,
                    $selectionX = oImage.naturalWidth/2 - $selectionWidth/2,
                    $selectionY = oImage.naturalHeight/2 - $selectionHeight/2,
                    $selectionX1 = $selectionX + $selectionWidth,
                    $selectionY1 = $selectionY + $selectionHeight;

                $('#preview').Jcrop({
                    minSize: [32, 32],
                    aspectRatio: 1,
                    bgFade: true,
                    bgOpacity: .3,
                    onChange: updateInfo,
                    onSelect: updateInfo,
                    onRelease: clearInfo,
                    boxWidth: 450,
                    boxHeight: 400,
                    setSelect: [$selectionX, $selectionY, $selectionX1, $selectionY1],
                    allowSelect: false
                }, function () {
                    jcrop_api = this;
                });
            };
        }
    });
}
