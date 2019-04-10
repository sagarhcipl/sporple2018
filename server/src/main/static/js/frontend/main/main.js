var mainController = new function () {

    var self;

    this.target_user_id = false;
    this.timer_interval_id = false;
    this.previous_new_message_count = false;

    this.init = function () {
        self = this;

        // highlight menu item
        this.highlightNavigation();

        // specific for message popup (but using general popup div)
        this.bindButtonFollowUnfollow();

        // like buttons
        this.bindButtonFavouriteUnfavourite();

        //Foldable buttons
        this.hide();

        // bind account settings dropdown menu icon click
        //this.bindAccountsSettingsMenu();

        // loader while ajax perform
//        this.bindLoader();

    };

    // =================== general ===================

//    @TODO
//    TO BE MODIFIED TO BE EXECUTED ONLY WHEN UPLOADING A FILE

//    this.bindLoader = function () {
//        $(document).ajaxSend(function (event, jqxhr, settings) {
//            if (settings.url != "/main/update") {
//                if ($("#loadingbar").length === 0) {
//                    $("body").append("<div id='loadingbar'></div>");
//                    $("#loadingbar").addClass("waiting").append($("<dt/><dd/>"));
//                    $("#progress").width((50 + Math.random() * 30) + "%");
//                }
//            }
//        });
//
//        $(document).ajaxComplete(function () {
//            $("#loadingbar").width("101%").delay(200).fadeOut(400, function () {
//                $(this).remove();
//            });
//        });
//    }

    this.hide = function () {
        $('.foldable').click(function () {
            mainController.foldableHandler($(this))
        });
    };
    this.foldableHandler = function (el) {
        if (el.parent().siblings().is(':visible')) {
            el.addClass('open');
            el.parent().siblings().slideUp("fast").css('display', 'block');
        } else {
            el.removeClass('open');
            el.parent().siblings().slideDown("fast").css('display', 'block');
        }
    };

    this.resetPopupDiv = function () {
        $('#popup').remove();
        $('<div class="popup" id="popup"><div id="popupcontent"></div></div>').appendTo('body');
    };

    // ============ navigation ==========

    this.highlightNavigation = function () {
        if (main_current_module == 'message') {
            $('#nav_message').addClass('active');
        }
        else if (main_current_module == 'main') {
            $('#nav_home').addClass('active');
        }
        else if (main_current_module == 'profile') {
            $('#nav_profile').addClass('active');
        }
        else if (main_current_module == 'connection') {
            $('#nav_connection').addClass('active');
        }
    };

    // ========== liking/favouriting stuff =========

    this.bindButtonFavouriteUnfavourite = function () {
        $('.left_content').on('click', '.button-favourite, .button-unfavourite',function (e) {
            e.preventDefault();
            var $parent = $(this).parents('div').eq(0),
                $action = $(this).hasClass('button-favourite') ? 'favourite' : 'unfavourite',
                $postId = $(this).attr('data-post-id'),
                $url = ($action === 'favourite') ? favourite_post_url : unfavourite_post_url;

            if ($action === 'favourite') {
                $('.favourite-text-holder-post-id-' + $postId).show();
            } else {
                $('.favourite-text-holder-post-id-' + $postId).hide();
            }

            $.getJSON($url, { post_id: $postId }, function (data) {
                $parent.html(data.replacement_html);
            });
        });
    };

    // =========== connections / follow ==

    this.bindButtonFollowUnfollow = function () {
        $('.left_content').on('click', '.button-follow, .button-unfollow',function (e) {
            e.preventDefault();
            var $parent = $(this).parents('div').eq(0),
                $action = $(this).hasClass('button-follow') ? 'follow' : 'unfollow',
                $otherUserId = $(this).attr('data-user-id'),
                $url = ($action === 'follow') ? follow_user_url : unfollow_user_url;

            $.getJSON($url, { user_id: $otherUserId }, function (data) {
                $parent.html(data.replacement_html);
            });
        });
    };


}

// =============================== BOOTUP =================================

$(window).load(function() {
    mainController.init();

    var $container = $('div#body_main_container'),
        $minContainerSize = $(window).outerHeight() - 104;

    if ($container.height() < $minContainerSize) {
        $container.height($minContainerSize);
    }
});
