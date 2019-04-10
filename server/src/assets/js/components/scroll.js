/*
 * smooth scrolling to anchor tabs.
 *
 */

var setup = function() {
    $('a[href*="#"]:not([href="#"])').click(function() {
        if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
          var target = $(this.hash);
          target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
          if (target.length) {
            $('html, body').animate({
              scrollTop: (target.offset().top - 50)
            }, 1000);
            return false;
          } else {
              location.href = '/#' + this.hash.slice(1);
          }
        }
    });
};

module.exports = {
    setup: setup
};
