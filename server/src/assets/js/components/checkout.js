/*
 * Functions related to the checkout module
 *
 */
module.exports = function() {
    'use strict';

    $(function(){
        var $monthly_option = $('#checkout-monthly'),
            $annual_option = $('#checkout-annual'),
            $card_monthly = $('#card-monthly'),
            $card_annual = $('#card-annual'),
            $plan_input = $('#plan_length'),
            $plan_due = $('#plan-due');
        $monthly_option.click(function() {
            $plan_input.val('monthly');
            $card_monthly.addClass('active');
            $card_annual.removeClass('active');
            $monthly_option.addClass('btn--blue');
            $monthly_option.removeClass('btn--secondary');
            $annual_option.removeClass('btn--blue');
            $annual_option.addClass('btn--secondary');
            $monthly_option.text('Selected');
            $annual_option.text('Choose Option');
            $plan_due.text($card_monthly.find('.price span').text());
        });

        $annual_option.click(function() {
            $plan_input.val('annual');
            $card_monthly.removeClass('active');
            $card_annual.addClass('active');
            $monthly_option.removeClass('btn--blue');
            $monthly_option.addClass('btn--secondary');
            $annual_option.removeClass('btn--secondary');
            $annual_option.addClass('btn--blue');
            $annual_option.text('Selected');
            $monthly_option.text('Choose Option');
            $plan_due.text($card_annual.find('.price span').text());
        });
        $plan_due.text($('.subscription .active .price span').text());
    });
};
