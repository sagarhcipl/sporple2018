/*
 * Send message modal functions
 *
 */

var modal = require('./modal');

var $sendMsgCont = undefined;
var $sendBtns = undefined;
var userId = undefined;
/*
 * image cropper
 * 
 */
var open = function(id) {
    
    userId = id;
    //close any previous modal
    modal.close();

    modal.setup(
        undefined,
        {
            title: 'Send message',
            classes: 'modal--send-message',
            contentUrl: message_popup_url + '?target_user_id=' + id,
            noBtns: true,
            callback: function() {
                _bind();
                setTimeout(function() {
                    $('#send-message__textarea').focus();
                }, 1000);
            }
        }
    ); 

    //need to wait a little time because of adding the class sets off a width transition
    setTimeout(function() {

        modal.open();
    }, 300);

};

var _afterSend = function(data) {
    var $followForm = undefined;
    //add content
    $sendMsgCont.html(data);

    //store form
    $followForm = $('#send-message__form--follow');
    
    // BIND STUFF
    $('#send-message__submitted-close').click(function(e) {
        e.preventDefault();
        modal.close();
    });

    if ($followForm.length) {

        $followForm.submit(function(e) {

            var formUrl = $followForm.attr('action');

            //update ui
            $followForm
                .find('#send-message__follow-btn').addClass('btn--loading');

            $.post(
                formUrl, 
                function(data) {
                    _afterSend(data);

                    setTimeout(function() {
                        modal.close();
                    }, 4000);
                }
            );

            return false;
        });

    }
};

var _fetchMsgAttachment = function() {
    var fetchUrl = message_popup_retrieve_images_url + '?target_user_id=' + userId;
    $.get(
        fetchUrl,
        _showAttachmentPrev
    );
};

var _deleteMsgAttachment = function() {
    
    $.post(
        message_popup_delete_images_url,
        {
            target_user_id: userId
        },
        function() {

            //clear input val
            $('#send-message__file-input').val('');

            _fetchMsgAttachment();
        }
    );
};

var _showAttachmentPrev = function(data) {

    var $prevCont = $('#send-message__attachment-prev');
    var $latestAttachmentPrev = undefined;
    var transitionTime = 250;
    
    //if we have some data
    if (data.replace(/\s/ig, '') != '') {
        
        $prevCont
        .html(data)
        .parent()
            .addClass('has-attachment');

        //find preview
        $latestAttachmentPrev = $prevCont.find('div.message__attachment-prev');

        //bind delete
        $latestAttachmentPrev
            .find('img.message__attachment-delete').click(function() {

                var $prev = $(this).parent();

                //remove from UI
                //transition?
                if (Modernizr && Modernizr.csstransforms3d) {

                    $prev.removeClass('show');

                    setTimeout(function() {
                        $prev.remove();
                    }, transitionTime);

                } else {

                    $prev.removeClass('show').remove();
                }

                _deleteMsgAttachment();

            });

        //transition?
        if (Modernizr && Modernizr.csstransforms3d) {
            //wait some time for the bind etc to finish otherwise animation wont play
            setTimeout(function() {
                $latestAttachmentPrev.addClass('show');
            }, 250);
        }

    } else {

        $prevCont
        .html('')
        .parent()
            .removeClass('has-attachment');
    }
};


var _bind = function() {

    $sendMsgCont = config.jQEles.$modal.find('div.send-message');
    $fileForm = config.jQEles.$modal.find('#send-message__file-form');
    $fileMsg = config.jQEles.$modal.find('span.send-message__file-dropzone-msg');
    var defaultAttachmentText = 'Drop file here to attach.';
    var loadingAttachmentText = 'Uploading file...';
    var finishedAttachmentText = 'Finished uploading';

    if( $sendMsgCont.length ){

        //bind submit
        $sendMsgCont
            .find('#send-message__form').submit(function(e) {
                e.preventDefault();

                var action = $(this).attr('action');
                var formData = $(this).serialize();
                var $submitBtn = $(this).find('#send-message__submit-btn');

                //update ui
                $submitBtn.addClass('btn--loading');

                $.post(
                    action,
                    formData,
                    function (data) {
                        $sendMsgCont.html(data);
                        if ($sendMsgCont.find('#send-message__form').length) {
                            _bind();
                        } else {
                            _afterSend(data);
                        }
                    }
                );
            })

        //bind cancel
            .find('#send-message__cancel-btn').click(function(e) {
                e.preventDefault();

                modal.close();
            });


        //bind file drop
        $fileForm
        .find('#send-message__file-dropzone').filedrop({
            fallback_id: 'send-message__file-input',
            url: $fileForm.attr('action'),
            paramname: 'message-file',
            data: {
                target_user_id: userId,
            },
            error: function (err, file) {
                switch (err) {
                    case 'BrowserNotSupported':
                        alert('browser does not support HTML5 drag and drop');
                        break;
                    case 'TooManyFiles':
                        break;
                    case 'FileTooLarge':
                        alert('Sorry, that file is too large. 20mb is the largest file you can send.');
                        break;
                    case 'FileTypeNotAllowed':
                        alert('Sorry, you cant send that kind of file. We only accept .jpg, .gif, .png, .doc, .docx, .xlss and .pdf');
                    default:
                        break;
                }
            },
            allowedfiletypes: config.fileTypesMsg,
            maxfiles: 1,
            maxfilesize: 20,
            dragOver: function() {
                $(this).addClass('over');
            },
            dragLeave: function() {
                $(this).removeClass('over');
            },
            drop: function() {
                $(this).removeClass('over');
            },
            uploadStarted: function(i, file, len){
                $fileMsg[0].innerHTML = loadingAttachmentText;
            },
            uploadFinished: function(i, file, response, time) {
                $fileMsg[0].innerHTML = finishedAttachmentText;
                
                setTimeout(function() {
                    $fileMsg[0].innerHTML = defaultAttachmentText;
                }, 500);
            },
            afterAll: function() {
                // runs after all files have been uploaded or otherwise dealt with
                _fetchMsgAttachment();
            }
        });

    }

};

var _bindOpen = function() {

    $sendBtns.click(function(e) {
        e.preventDefault();

        var userId = $(this).attr('data-user-id');

        open(userId);

    });

};

var setup = function() {
    
    $sendBtns = $('.send-message');

    if ($sendBtns.length) {

        _bindOpen();

    }

};


module.exports = {
    setup: setup,
    open: open
};
