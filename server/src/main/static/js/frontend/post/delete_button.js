var postDeleteButtonController = new function() {
  var self;

  this.user_id = false;
  this.jquery_query = false;

  this.init = function() {
    self = this;

    this.bindEvents();
  }

  this.bindEvents = function () {
    $('#main_container').on('click', '.post_delete_button', function(e) {
      e.preventDefault();
      self.jquery_query = $(this).attr('data-jquery-query');

      $.post($(this).attr('href'), function(data) {
        var jquerystring = self.jquery_query;
        $(jquerystring).remove();
      });
    });
  }

}

$(function() {
  postDeleteButtonController.init();
  //
  // @TODO: after ajax update when editing a field:
  //    postDeleteButtonController.bindEvents()
  //

});