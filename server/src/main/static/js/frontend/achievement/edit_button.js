var achievementEditButtonController = new function () {

    this.init = function () {
        this.bindEdit();
    };

    this.bindEdit = function () {

        //$('#profile_achievements').on('click', '#profile_add_achievement', function () {
            //$.get($(this).attr('href'), function( data ) {
                //$('#profile_achievements > form').remove();
                //$('#profile_achievements > header').after(data);
                //achievementEditButtonController.bindAchievementSubmit();
            //});
            //return false;
        //});

        // $('#profile_achievements').on('click', 'a[name="profile_edit_achievement"]', function () {
        //     $.get($(this).attr('href'), function (data) {
        //         $('#profile_achievements > form').remove();
        //         $('#profile_achievements > header').after(data);
        //         achievementEditButtonController.bindAchievementSubmit();
        //     });
        //     return false;
        // });
    };

    this.bindAchievementSubmit = function () {
        $("#profile_achievement_form").submit(function (event) {
            event.preventDefault();

            /* get some values from elements on the page: */
            var posting = $.post($(this).attr('action'), $(this).serialize());
            posting.done(function (data) {
                $("#profile_achievements").html(data);
                achievementEditButtonController.bindAchievementSubmit();//if wrong submit this is user

                $('#profile_achievements .foldable').click(function () {
                    mainController.foldableHandler($(this))
                });
            });
        });
        $('#profile_achievements').on('click', '#profile_achievement_cancel', function () {
            $(this).closest('form').remove();
            return false;
        });
        $("#icons_dropdown_container").show();
        $("#achievement_icon").hide();

        $('.icons_dropdown').delegate('a', 'click', function () {
            $('#achievement_icon').val(($(this).attr('id').substr(5)));
            $(".icons_dropdown").hide();
            $("#icon_select").find('img').attr('src', '/images/icons/icon' + ( parseInt($('#achievement_icon').val())) + '.png')
            return false;
        });

        $("#icon_select").on('click', function () {
            $(".icons_dropdown").show();
            return false;
        });
    }
};

$(function () {
    achievementEditButtonController.init();
});
