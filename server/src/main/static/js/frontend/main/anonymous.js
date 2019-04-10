var mainAnonController = new function () {

    var self;

    //this.timer_interval_id = false;

    this.init = function () {
        self = this;

        // specific for message popup (but using general popup div)
//        this.bindJoinButtons();

        // specific for message popup (but using general popup div)
        this.bindExpandablesButtons();


    }


//    this.bindJoinButtons = function () {
//
//        $('.btn_join').click(function (e) {
//
//            e.preventDefault();
//
//            // use "landing_head" for the top of the landing page
//            $('html, body').animate({
//                scrollTop: 0
//            }, 300);
//        });
//    }

    this.bindExpandablesButtons = function () {

        $('.ha-clickable').click(function (e) {

            e.preventDefault();

            var the_id = $(this).attr('id');
            var the_expandable_id = the_id + '-expand';
//      alert(the_expandable_id);
            $('.ha-expandable').hide();
            $('.ha-clickable').removeClass('selected');

            $('#' + the_id).addClass('selected');
            $('#' + the_expandable_id).fadeIn();

        });

    }


}


// =============================== BOOTUP =================================

$(function () {

    mainAnonController.init();
    $('#ha-athlete').click();

});


