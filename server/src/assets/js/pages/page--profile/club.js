/*
 * New style listings
 */

 'strict mode';

var forms = require('./../../base/forms');
var autosearch = require('./../../components/autosearch');
var modal = require('./../../components/modal');
var $pageContainer = undefined;


var _bindDeleteForm = function() {
    var $secondaryBtn = config.jQEles.$modal.find('.btn--secondary'),
        $primaryBtn = config.jQEles.$modal.find('#btn--submit');
    $secondaryBtn.click(function() {
        modal.close();
        return false;
    });
    var $form = config.jQEles.$modal.find('#delete-listing-form');
    if($form.length) {
        forms.wrapSelects();
        forms.bind();
        // form validation
        $form.parsley(config.parsleyDefaultConfig);
        $form.submit(function() {
            var $this = $(this);
            $primaryBtn.addClass('btn--loading');
            mixpanel.track('delete-listing');
            $this.ajaxSubmit({
                success: function(response) {
                    if(response === 'success') {
                        window.location.reload();
                    } else {
                        modal.refresh(response);
                        _bindDeleteForm();
                    }
                },
                error: function(xhr, textStatus, error) {
                    alert(error);
                }
            });
            return false;
        });
        $form.find('input[name=close_reason]').click(function() {
            var $this = $(this);
            if ($this.val() == 'found_on_sporple') {
                $form.find('.delete-listing-quick-search').removeClass('hidden');
                $form.find('.delete-listing-outside').addClass('hidden');
            } else if($this.val() == 'found_elsewhere')  {
                $form.find('.delete-listing-outside').removeClass('hidden');
                $form.find('.delete-listing-quick-search').addClass('hidden');
            } else {
                $form.find('.delete-listing-quick-search').addClass('hidden');
                $form.find('.delete-listing-outside').addClass('hidden');
            }
        });
        $('#delete-listing-results-container').on('click', 'li', function() {
            var $this = $(this);
            var user_id = $this.attr('data-user-id'),
                img_src = $this.find('img').attr('src'),
                name = $this.find('a.search-results__profile-name').text();
            $form.find('input[type=text]').addClass('hidden');
            $form.find('#delete-listing-results-container').addClass('hidden');
            $result = $('.delete-listing-picked-user');
            $result.find('img').attr('src', img_src);
            $result.find('span.name').text(name);
            $form.find('#delete-listing-user-id').val(user_id);
            $result.removeClass('hidden');
        });
        autosearch.setup('delete-listing-form', 'delete-listing-results-container');
    }
};


var _bindDeleteListing = function () {
    $pageContainer.find('.delete-listing').click(function() {
        var $this = $(this);
        var url = $this.attr('data-url');
        // close any previous modal
        modal.close();
        modal.setup(undefined, {
                title: 'Close Listing',
                contentUrl: url,
                noBtns: true,
                callback: function() {
                    _bindDeleteForm();
                }
        });

        setTimeout(function() {
            modal.open();
        }, 300);
    });
};

var setup = function() {
    $pageContainer = $('.profile-page.club');
    if ($pageContainer.length) {
        _bindDeleteListing();
    }
};

module.exports = {
    setup: setup
};
