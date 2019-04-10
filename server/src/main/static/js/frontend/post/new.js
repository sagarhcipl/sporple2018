var Post = {

    showResponse: function (responseText, statusText, xhr, $form) {
        $('.post_filename').html('');

        Comment.bindEvents();
        mainController.bindButtonFavouriteUnfavourite();
        $('.upload_footer').hide();
        Post.revealFileUpload(0);

        $(this).find('#post_new_submit').removeClass('btn--loading');

        var $container = $('#homepage_activity_container');

        // update the post list after a new post is added
        $container.load($container.data('url'), {user_id: $container.data('id')}, function () {
            Comment.embedYoutubeVideos();
            Comment.makeExternalLinksTargetBlank();
        });

        Post.bindInputEvents();

    },

    changeFilename: function (el) {
        if (!Post.checkImageUpload($(el))) {
            return false;
        } // check if the upload is really an image

        var file_number = el.className.replace('post_selectfile', ''),
            filename = $(el).val();

        file_number = $.trim(file_number.replace('select_file_', ''));
        filename = filename.split("\\");

        $('#filename_' + file_number).html(filename.pop());

        if (file_number < 9) {
            Post.revealFileUpload(parseInt(file_number) + 1);
        }
    },

    bindInputEvents: function () {
        var options = {
            target: '.activity_input div.content',   // target element(s) to be updated with server response
            replaceTarget: true,
            success: Post.showResponse,  // post-submit callback
            beforeSerialize: Post.beforeSerialize,

            // other available options:
            clearForm: true,        // clear all form fields after successful submit
            resetForm: true        // reset the form after successful submit
        };

        // bind form using 'ajaxForm'
        $('#post_new_form').submit(function() { 

            $(this).find('#post_new_submit').addClass('btn--loading');
            $(this).ajaxSubmit(options); 
     
            return false; 
        });

        $('.post_selectfile').bind('change', function () {
            Post.changeFilename(this); // adjust binding strategy
        });
    },

    revealFileUpload: function (number) {
        $('#upload_footer_' + number).fadeIn();
    },

    /**
     * Checks if the upload is an image
     *
     * @param object el
     * @returns {Boolean}
     */
    checkImageUpload: function (el) {
        // get selected file
        var oFile = el[0].files[0],
            file_id = el.attr('id').replace(/[^0-9]/g, ''),
            rFilter = /^(image\/jpeg|image\/jpg|image\/png|image\/gif)$/i;

        if (oFile.size > $('#post_new_form').data('max-size')) {
            alert('File is too large (maximum is ' + $('#post_new_form').data('max-size') + ' bytes).');
            $('#post_new_attachements_' + file_id + '_filename').val('');
            return false;
        }

        // check for image type (jpg and png are allowed)
        if (!rFilter.test(oFile.type)) {
            alert('Please select a valid image file (jpeg, jpg, png, and gif are allowed)');
            $('#post_new_attachements_' + file_id + '_filename').val('');
            return false;
        }

        // check for file size
        if (oFile.size > 8250 * 1024) {
            alert('You have selected too big file, please select a one smaller image file');
            return false;
        }

        return true;
    },

    init: function () {
        Post.bindInputEvents();
        Post.revealFileUpload($('.upload_footer:visible').length);
    }
};

$(window).load(Post.init);

