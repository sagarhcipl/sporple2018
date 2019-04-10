var tabsController = new function() {

  var self;

//  this.open_thread_id = false;

  this.init = function() {
    self = this;

    this.bindStuff();
  }

  // thread list ------------------------------------------------------------------------

  this.bindStuff = function() {
//    alert('here i am');

    $('.content_tab').click(function(e) {
      e.preventDefault();
//      alert('hi there');
      $('.content_tab').removeClass('active');
      $(this).addClass('active');
      $('.content_tab_content').hide();
      $('#' + $(this).attr('id') + '_content').fadeIn();

      var init_call = $(this).attr('data-init-call');
//      alert(init_call);
      eval(init_call);

    });

  }

}



$(function() {

  tabsController.init();

});