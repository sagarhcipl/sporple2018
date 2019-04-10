/*
 * Functions related to the generic and sports specific landing page
 *
 */

var $ = require('jquery');

module.exports = function() {

    $(function(){
        'use strict';

        var $learn_more = $(".landing.learn-more");
        var $tabs_box = $learn_more.find(".tabs");
        var $tabs = $tabs_box.find("div");

        $tabs.click(function() {
            $tabs.removeClass('active');
            $(this).addClass('active');
            var val = $(this).attr('data-info');
            var info = $learn_more.find('.info.' + val);
            $learn_more.find('.info').addClass('hidden');
            info.removeClass('hidden');
        });

        var $opportunities = $('.opportunities .tab'),
            $left = $('.opportunities .scroll-left'),
            $right = $('.opportunities .scroll-right');
        $left.click(function() {
            var current = $opportunities.scrollLeft();
            $opportunities.animate({scrollLeft: current-500}, 300);
        });
        $right.click(function() {
            var current = $opportunities.scrollLeft();
            $opportunities.animate({scrollLeft: current+500}, 300);
        });
    });

};
