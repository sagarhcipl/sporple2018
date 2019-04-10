/*
 * Functions for sign up funnel
 *
 */

var modal = require('./../components/modal');

module.exports = function() {
    $(function() {
        'use strict';
        
        var confirmDeactivate = '<div class="form__row">' +
            '<p>Are you sure you want to cancel your membership? This cannot be undone.</p>' +
            '</div>';
        var $deactivateBtn = $('.deactivate-membership');
        $deactivateBtn.click(function(e) {
            modal.setup(
                confirmDeactivate,
                {
                    title: 'Confirm Membership Deactivation',
                    classses: 'confirm-email',
                    success: function() {
                        $deactivateBtn.addClass('btn--loading');
                        modal.close();
                        $.post(
                            '/payment/unsubscribe',
                            {},
                            function(data) {
                                if (data.success) {
                                    window.location.reload();
                                } else {
                                    $deactivateBtn.removeClass('btn--loading');
                                    window.alert(data.error);
                                }
                            },
                            'json'
                        );
                    },
                }
            );
            modal.open();
        });
    });

};
