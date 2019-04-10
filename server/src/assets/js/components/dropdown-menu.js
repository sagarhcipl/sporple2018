/*
 * dropdown menu functions
 *
 */


var $dropdowns = undefined;
var transitionDuration = 300;

var _bind = function() {

    $dropdowns.each(function() {
        var $this = $(this);
        $this.find('.dropdown-menu__toggle').click(function(e){
            e.preventDefault();
            toggle($this);
        });
    })
    .children('a').click(function(e){
        if (Modernizr.touchevents) {
            e.preventDefault();
        } else {
            e.stopPropagation();
        }
    });

};

var toggle = function($dd) {
    var $listCont = $dd.children('.dropdown-menu__list-cont');

    if(!$dd.hasClass('open')) {

        var h = $listCont.children('ul').outerHeight(true);

        $listCont.height(h);

        setTimeout(function(){

            $dd.addClass('open');

            //bind close to anywhere but the menu
            config.jQEles.$bod.click(function(){
                toggle($dd);
            });

            $listCont.click(function(e){
                e.stopPropagation(); 
            });

        }, transitionDuration);

    } else {

        $listCont.height(0);

        //remove global binds
        config.jQEles.$bod.off('click');
        $listCont.off('click');

        setTimeout(function(){

            $dd.removeClass('open');

        }, transitionDuration);

    }

};

var setup = function() {
    
    $dropdowns = $('section.dropdown-menu-header, div.dropdown-btn-group');

    if($dropdowns.length) {

        _bind();

    }

};

module.exports = {
    setup: setup,
    toggle: toggle,
};
