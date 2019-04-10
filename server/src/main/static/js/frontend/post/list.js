var Comment = {

    hideLink: function (e) {
        e.preventDefault();
        var class_name = this.className.replace('hide_show_comment_link ', ''),
            hide = true,
            post_id;

        if (class_name.search('comment_hide_link_') == -1) {
            hide = false;
        }

        if (hide) {
            post_id = class_name.replace('comment_hide_link_', '');
            Comment.hide(post_id);
        } else {
            post_id = class_name.replace('comment_show_link_', '');
            Comment.show(post_id);
        }
    },

    hide: function (post_id) {
        $('#show_comment_text_' + post_id).toggleClass('hidden visible');
        $('#hide_comment_text_' + post_id).toggleClass('visible hidden');
        $('.comment_' + post_id).toggleClass('visible hidden');
    },

    show: function (post_id) {
        $('#hide_comment_text_' + post_id).toggleClass('hidden visible');
        $('#show_comment_text_' + post_id).toggleClass('visible hidden');
        $('.comment_' + post_id).toggleClass('hidden visible');
    },

    adjustTextarea: function (e) {
        e = e || window.event;

        var elem = e.currentTarget,
            span = elem.parentNode.parentNode.parentNode.parentNode.children[2];

        span.style.width = elem.clientWidth + 'px';
        span.innerHTML = elem.value.replace(/\n/ig, '<br/>') + 'space';

        elem.style.height = (span.clientHeight) + 'px';
    },

    // check if an element is visible on the viewport
    isScrolledIntoView: function (e) {
        var docViewTop = $(window).scrollTop(),
            docViewBottom = docViewTop + $(window).height(),
            elemTop = $(e).offset().top,
            elemBottom = elemTop + $(e).height();

        return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
    },

    goToNew: function (e) {
        e.preventDefault();
        var comment_form = $(e.target).closest('article').find('.new_comment_container'),
            post_id = this.className.replace('new_comment_link_', ''),
            container = $('html,body');

        post_id = post_id.replace('new_comment_link ', '');

        comment_form.find('textarea').focus(); // focus on comment form
    },

    init: function () {
        window.oldBrowserMode = false;

        if (!window.FileList) {
            window.oldBrowserMode = true;
        }
        Comment.bindEvents();
        Comment.makeExternalLinksTargetBlank();
        Comment.embedYoutubeVideos();
        Comment.embedSoundcloudLinks();
    },

    makeExternalLinksTargetBlank: function () {
        $('a[href^="http://"]').not('a[href*=sporple]').attr('target','_blank');
        $('a[href^="https://"]').not('a[href*=sporple]').attr('target','_blank');
    },

    embedYoutubeVideos: function () {
        $('div.youtube-embed').each(function() {
            var $width, $height;

            if ($(this).parents('.SharedPost').length) {
                $width = 470;
                $height = 264;
            } else {
                $width = 550;
                $height = 309;
            }

            var ytID = $(this).data('youtube-id');

            $(this).replaceWith('<iframe width="' + $width + '" height="' + $height + '" src="//www.youtube.com/embed/' + ytID + '" frameborder="0" allowfullscreen></iframe>');
        });
    },

    embedSoundcloudLinks: function () {
        $('div.soundcloud-embed').each(function () {
            var scID = $(this).data('soundcloud-id');

            $(this).replaceWith('<iframe width="100%" height="450" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/' + scID + '&amp;auto_play=false&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false&amp;visual=true"></iframe>');
        });
    },

    bindEvents: function () {
        $('.hide_show_comment_link').unbind();
        $('.new_comment_link').unbind();
        $('textarea.comment_textarea').unbind();
        $('button.comment_button').unbind();
        $('.hide_show_comment_link').click(Comment.hideLink);
        $('.new_comment_link').click(Comment.goToNew);
        $('textarea.comment_textarea').on('keyup', function (e) {
            e = e || window.event;
            if (e.keyCode === 13 && !e.shiftKey) {
                var $form = $(this).closest("form");

                // start your submit function
                if ($.trim($(this).val()) != '') {
                    $form.find('button.comment_button').addClass('btn--loading');
                    $form.find('#sf_comment_referer').val(window.location.pathname);
                    $form.submit();
                }
            }

            Comment.adjustTextarea(e);
        });
        $('button.comment_button').click(function(e) {
            var $form = $(this).closest("form");
            var comment_text = $form.find('textarea.comment_textarea').val();
            $(this).addClass('btn--loading');
            if ($.trim(comment_text) != '') {
                $form.find('#sf_comment_referer').val(window.location.pathname);
                $form.submit();
            }
            return false;
        });

        var options_comment = {
            success: Comment.pageReload,
            clearForm: true,
            resetForm: true
        };
        $('.sf_comment_form').submit(function() {
            $(this).ajaxSubmit(options_comment);
            return false;
        });

        $('.activity_container').off().on('click', 'article ul.ooip_attachment_list a', function (e) {
            e.preventDefault();
            Comment.imagePopup(
                $(e.currentTarget.parentNode.parentNode.parentNode).attr('id'),
                $(e.currentTarget).attr('href'),
                e.currentTarget
            );
        });
    },

    pageReload: function() {
        window.location.reload();
    },

    imagePopup: function (post, image, elem) {
        var item = '#' + post + '_popup',
            loader = '<span class="loading-floater" style="position: relative; height: 0; float: left;"><div style="padding: 0; background-color: #000; opacity: 0.6;"><img style="position: relative; width: 16px;" src="/images/icons/ajax-loader.gif"></div></span>',
            imageObj = new Image(),
            img, loaderLeftMargin, loaderTopMargin;

        if ($(elem).find('span.loading-floater').length == 0) {
            img = $(elem).find('img');
            loaderLeftMargin = (img.width() - 16) / 2;
            loaderTopMargin = (img.height() - 16) / 2;

            $(loader).insertBefore($(elem).find('img'));
            $(elem).find('span.loading-floater img').css('left', loaderLeftMargin).css('top', loaderTopMargin);
            $(elem).find('span.loading-floater div').css('width', img.width()).css('height', img.height());
        }

        // preload image data - for processing image dimenstions
        // prevents miss fire of the resizePopup() function
        imageObj.src = image;

        $(imageObj).load(function () {
            Comment.resizePopup(item);
            Comment.showImagePopup(item, imageObj);
            $(elem).find('span.loading-floater').remove();
        });
        $(imageObj).error(function () {
            $(elem).find('span.loading-floater').remove();
            alert('Error encounterd, image cannot be loaded.');
        });
    },

    // open the image popup using an image object - new Image()
    showImagePopup: function (item, imageObj) {
        $(item).bPopup({
            modalColor: '#000000',
            position: ['auto', 50],
            opacity: 0.8,
            onOpen: function () {
                $(item).css({'display': 'block'});

                $(item + ' a.btn_prev').addClass('disabled');
                $(item + ' a.btn_next').addClass('disabled');

                $(item + ' figure').html('<img src="' + imageObj.src + '" />');

                Comment.resizePopup(item);
            }
        });
    },

    resizePopup: function (item) {
        $(item + ' figure img').css({
            width: 'auto',
            height: 'auto'
        });

        var maxHeight = ($(window).height() * 0.8) - 55,
            maxWidth = ($(window).width() * 0.8),
            ratioX = $(item + ' figure img').width() > maxWidth ? maxWidth / $(item + ' figure img').width() : 1,
            ratioY = $(item + ' figure img').height() > maxHeight ? maxHeight / $(item + ' figure img').height() : 1,
            ratio = ratioX < ratioY ? ratioX : ratioY;

        $(item + ' figure img').css({
            width: ratio * $(item + ' figure img').width(),
            height: ratio * $(item + ' figure img').height()
        });
    },

    // ======== sharing ===========

    shareClick: function (post_id) {
        Comment.shareLoadPopup(post_id);
    },

    shareLoadPopup: function (post_id) {
        mainController.resetPopupDiv();

        $('#popup').bPopup({
            contentContainer: '#popupcontent',
            loadUrl: post_popup_form_url + '?post_id=' + post_id,
            loadCallback: function () {
                Comment.sharePopupLoaded();
            },
            onClose: function () {
            }
        });
    },

    sharePopupLoaded: function () {
        var post_id = $('#post_shared_post_id_popup').attr('value');

        $('#post_new_popup_form').submit(function (e) {
            if ($.trim($('#post_body_popup').val()) == '') {
                return false;
            }
            $('#post_popup_submit_button').attr('disabled', true);
            return true;
        });

        $.get(post_preview_url + '?post_id=' + post_id, function (data) {
            $('#post_new_popup_share_preview').html(data);

            //$('#popup').css({'height': 'auto'});
            setTimeout(function () {
                $('#popup').css({'height': 'auto'});
            }, 200);
        });
    }

}


var $postListUrl = '/post/list',
    $alreadyloading = false,
    $nextpage = 2,
    $listContainer, $ownPosts, $cond, $scrollTarget, $profileId;

function loadPosts () {
    if ($cond()) {
        if ($alreadyloading == false) {
            $alreadyloading = true;
            $listContainer.children().last().after('<div style="text-align: center; margin: 10px">Loading ...</div>');
            $.ajax({
                type: 'POST',
                url: $postListUrl,
                data: {page: $nextpage, own: $ownPosts, user_id: $profileId, referer: window.location.pathname},
                success: function (data) {
                    if (data.length > 10) {
                        $listContainer.children().last().remove();
                        $listContainer.children().last().after(data);
                        $alreadyloading = false;
                        $nextpage++;

                        Comment.bindEvents();
                        Comment.embedYoutubeVideos();
                        Comment.embedSoundcloudLinks();
                    } else {
                        $listContainer.children().last().html('No more posts !')
                            .delay('2000')
                            .queue(function () {
                                $(this).remove();
                            });

                        $scrollTarget.unbind('scroll');
                    }
                }
            });
        }
    }
};


$(window).load(function () {
    Comment.init();

    if (($listContainer = $('#homepage_activity_container')) && $listContainer.length > 0) {
        $ownPosts = null;
        $scrollTarget = $(window);
        $cond = function () {
            return ($(window).height() + $(window).scrollTop()) >= ($(document).height() - $('#footer').height());
        };
    } else if (($listContainer = $('#activity_container'))&& $listContainer.length > 0) {
        $ownPosts = true;
        $scrollTarget = $listContainer;
        $cond = function () {
            return ($listContainer.scrollTop() + $listContainer.innerHeight()) >= ($listContainer[0].scrollHeight);
        };
    }

    if ($listContainer.length > 0) {
        $profileId = $listContainer.data('id');

        $scrollTarget.on('scroll', _.debounce(loadPosts, 100));
    }
});
