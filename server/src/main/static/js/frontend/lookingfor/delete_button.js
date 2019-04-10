var lookingforDeleteButtonController = new function() {

  var self;

  this.user_id = false;
  this.jquery_query = false;

  this.init = function() {
    self = this;

    this.bindEvents();
  }

  this.bindEvents = function () {

    $('.lookingfor_delete_button').click(function(e) {

      e.preventDefault();

      self.jquery_query = $(this).attr('data-jquery-query');

      $.post($(this).attr('href'), function(data) {

        var jquerystring = self.jquery_query;
//        alert('debug ' + jquerystring);

        $(jquerystring).remove();

        // MUST RELOAD !!!!!!!!!!!!
        location.reload();

      });


    });

  }


}





$(function() {

  lookingforDeleteButtonController.init();

  //
  // @TODO: after ajax update when editing a field:
  //    clientDeleteButtonController.bindEvents()
  //

});