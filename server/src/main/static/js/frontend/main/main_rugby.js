$(document).ready(function () {
    'use strict';
    
    //  Accordion Panels
    var $whoAccordian = $('#landing-page__accordian');

    $whoAccordian.on('click', '.toggle-pane', function () {

        var $accordianItm = $(this).parent('div.col-1-3');
        var $pane = $accordianItm.children('div.pane');
        var transDurantion = 300;

        if(!$accordianItm.hasClass('open')){

            var h = $pane.children('ul').outerHeight(true);

            $pane.height(h);
            $accordianItm.addClass('open');

        }else{

            $pane.height(0);
            $accordianItm.removeClass('open');

        }

    });

    //open athlete to start
    $whoAccordian.find('div.athlete h3.toggle-pane').click();


    $('a.site-header__login-toggle').on('click', function () {
        var $loginCont = $(this).siblings('div.site-header__login-cont');
        var transDuration = 300;

        if(!$loginCont.hasClass('open')){

            var h = $loginCont.children('div.login-mod').outerHeight(true);

            $loginCont
                .height(h);

            setTimeout(function(){

                $loginCont.addClass('open');

            }, transDuration-100);    

        }else{

            $loginCont
                .removeClass('open')
                .height(0);
                
        }

    });

    $("div.landing-page__slider").owlCarousel({
        slideSpeed: 300,
        paginationSpeed: 400,
        singleItem: true
    });
});
