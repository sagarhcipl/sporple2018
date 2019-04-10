var profileFieldClearController = new function() {

  var self;

  this.user_id = false;
  this.jquery_content_field_query = false;

  this.init = function() {
    self = this;

    this.bindEvents();
  }

  this.bindEvents = function () {

    $('.profile_clear_field_button').click(function(e) {

      e.preventDefault();

      self.jquery_content_field_query = $(this).attr('data-jquery-content-field-query');

      $.post($(this).attr('href'), function(data) {

        var jquerystring = self.jquery_content_field_query;
//        alert('debug ' + jquerystring);

        $(jquerystring).html('');

      });


    });

  }


}





$(function() {

  profileFieldClearController.init();

  //
  // @TODO: after ajax update when editing a field:
  //    profileFieldClearController.bindEvents()
  //

});