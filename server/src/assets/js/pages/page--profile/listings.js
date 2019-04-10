/*
 * Club listings on the profile page functions
 *
 */

'strict mode';

var helpers = require('./../../base/helpers');
var forms = require('./../../base/forms');
var modal = require('./../../components/modal');
var profilePicEditor = require('./../../components/profile-pic-editor');
var sendMessage = require('./../../components/send-message');
var incompleteProfile = require('./../../components/apply-check');
require('jquery-ui/datepicker');

var $applyBtns = undefined;

/*
 * send application to listing
 * 
 */
var _submitApplication = function($form) {

    var formUrl = $form.attr('action');
    var formData = $form.serialize();
    var clubName = $form.attr('data-club-name');
    var successHtml = '<div class="thank-you">Your application has been successfully submitted to ' + clubName + '</div>' +
                    '<p>Please be patient whilst the club gets back to you. We wish you all the best.<br/> &mdash; Team Sporple</p>';

    $form
        .find('#apply-form__submit').addClass('btn--loading');

    $.ajax({
        type: 'POST',
        url: formUrl,
        data: formData,
        success: function(response) {
            if (response === 'success') {
                modal.setup(
                    successHtml, {
                        title: 'Thanks for applying',
                        callback: function() {
                            // Do nothing
                        }
                    });
            } else {
                modal.setup(
                    response, {
                        title: 'New Application',
                        noBtns: true,
                        callback: function() {
                            _bindApplyForm();
                        }
                    });
            }
        }
    });

};


var _bind = function() {
    //bing any current & future send applicationj btns
    $applyBtns.click(function() {
        var $btn = $(this);
        $btn.addClass('btn--loading');
        var listingId = $btn.attr('data-id');
        var role = $btn.attr('data-role');
        var appUrl = $btn.attr('data-url');
        mixpanel.track('apply_clicked', {
            'listing-id': listingId,
            'role': role
        });

        // check if user can apply.
        $.ajax({
              url: '/can_apply/' + listingId + role,
              success: function(response) {
                if (response === 'success') {
                    mixpanel.track('can_apply', {
                        'listing-id': listingId,
                         'role': role
                    });

                    // close previous modals.
                    modal.close();
                    modal.setup(undefined, {
                        title: 'New Application',
                        contentUrl: appUrl,
                        noBtns: true,
                        callback: function() {
                            _bindApplyForm();
                        }
                    });
                    setTimeout(function() {
                        modal.open();
                        $btn.removeClass('btn--loading');
                    }, 300);

                } else {
                    incompleteProfile.open(response);
                    mixpanel.track('incomplete-profile', {
                        'listing-id': listingId
                    });
                }
            },
            error: function(xhr, textStatus, error) {
                alert('Sorry, there was an error trying to apply : ' + error);
            },
        });

        return false; 
    });
};


var _bindApplyForm = function() {
    var $form = config.jQEles.$modal.find('form');
    $form.submit(function() {
        _submitApplication($(this));
        return false;
    });
};


var setup = function() {
    $applyBtns = $('.listing-info .btn--apply');
    if ($applyBtns.length) {
        _bind();
    }
    $('.show-listing-details').click(function() {
        var $this = $(this);
        var details = $this.siblings('.listing-details');
        if (details.hasClass('hidden')) {
            $this.html('Hide Details');
        } else {
            $this.html('View Details');
        }
        details.toggleClass('hidden');
    });
};


module.exports = {
    setup: setup
};
