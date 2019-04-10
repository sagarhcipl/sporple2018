var profileClientsMediaController = new function()
{
  var self = this;

  this.page         = 0;
  this.image        = 0;
  this.imageLoaded  = false;

  /**
   * construct method
   */

  var construct = function()
  {
    self.updateNavigation();
  }

  /**
   * update navigation
   */

  this.updateNavigation = function()
  {
    if($('nav.media_thumb.clientslist').children().length == 0)
    {
      $('nav.media_thumb.clientslist').fadeOut(1000);
      $('nav.carousel_nav clientslist').fadeOut(1000);
    }
    else
    {
      $('nav.media_thumb.clientslist').fadeIn(1000);
      $('nav.carousel_nav clientslist').fadeIn(1000);

      $('nav.carousel_nav.clientslist div').html('');
      
      var images = $('nav.media_thumb.clientslist ul.ooip_attachment_list li').length;
      var pages = Math.ceil((($('nav.media_thumb.clientslist ul li').width()+3) * images) / $('nav.media_thumb.clientslist section').width());
      
      for(var a = 0; a < pages; a++)
      {
        $('nav.carousel_nav.clientslist div').append('<a href="#"></a>');
      }

      $('nav.media_thumb.clientslist a.attachment_link').unbind('click');
      $('nav.media_thumb.clientslist>a.btn_prev').unbind('click');
      $('nav.media_thumb.clientslist>a.btn_next').unbind('click');
      $('nav.carousel_nav.clientslist div a').unbind('click');

      $('nav.media_thumb.clientslist a.attachment_link').click(function(e) { e.preventDefault();self.imagePopup($(e.currentTarget.parentNode).index());  });
      $('nav.media_thumb.clientslist>a.btn_prev').click(function(e)       { e.preventDefault();self.navigationPage(self.page - 1);                      });
      $('nav.media_thumb.clientslist>a.btn_next').click(function(e)       { e.preventDefault();self.navigationPage(self.page + 1);                      });
      $('nav.carousel_nav.clientslist div a').click (function(e)          { e.preventDefault();self.navigationPage($(e.currentTarget).index());         });
      
      this.navigationPage(0);
    }
  };

  /**
   * set navigation page
   */

  this.navigationPage = function(page)
  {
    var images = $('nav.media_thumb.clientslist ul.ooip_attachment_list li').length;
    var pages = Math.ceil((($('nav.media_thumb.clientslist ul li').width()+3) * images) / $('nav.media_thumb.clientslist section').width());
    var containerWidth = $('.ooip_attachment_client_list_item').width() * images;
    
    $('.ooip_attachment_list.clientslist').width(containerWidth);
    
    this.page = page > 0 ? (page < pages ? page : pages - 1) : 0;
    
    (this.page == 0         ? $('nav.media_thumb.clientslist a.btn_prev').addClass('disabled') : $('nav.media_thumb.clientslist a.btn_prev').removeClass('disabled'));
    (this.page == pages - 1 ? $('nav.media_thumb.clientslist a.btn_next').addClass('disabled') : $('nav.media_thumb.clientslist a.btn_next').removeClass('disabled'));

    if(pages === 1) {
      $('nav.media_thumb.clientslist a.btn_prev').addClass('hide_carousel_nav');
      $('nav.media_thumb.clientslist a.btn_next').addClass('hide_carousel_nav');
      $('.carousel_nav.clientslist').addClass('hide_carousel_nav');
    }
    
    $('nav.media_thumb.clientslist ul.ooip_attachment_list').animate({ left: ((this.page * -($('nav.media_thumb.clientslist section').width()-4))) }, 1000);
    
    $('nav.carousel_nav.clientslist div').children().each(function()
    {
      if($(this).index() == self.page)
      {
        $(this).addClass('selected');
      }
      else
      {
        $(this).removeClass('selected');
      }
    });
  };

  $(function(){ construct(); });
}