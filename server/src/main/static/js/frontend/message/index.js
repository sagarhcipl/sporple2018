var messageController = new function() {

  var self;

  this.open_thread_id = false;
  this.thread_update_timer = false;
  this.last_update_checksum = 'none';
  this.page = 0;
  this.scroll_target = undefined;
  this.cond = undefined;
  this.already_loading = false;

  this.init = function() {
    self = this;

    this.scroll_target = $('#message-user-threads-list');
    $('#message-user-threads-filter-form').submit(function(e) {
      e.preventDefault();
      self.page = 0;
      self.scroll_target.html('<div style="text-align: center; margin: 10px">Loading ...</div>');
      $.post($("#message-user-threads-filter-form").attr('action'), $("#message-user-threads-filter-form").serialize(), self.showUserThreads);
    });
  
    this.cond = function() {
      return (self.scroll_target.scrollTop() + self.scroll_target.innerHeight()) >= (self.scroll_target[0].scrollHeight);
    };
    if (self.scroll_target.length > 0) {
      self.scroll_target.on('scroll', _.debounce(this.loadUserThreads, 100));
    }
    this.loadUserThreads();
    $('.message-back').click(function(e) {
        $('#message-user-threads').removeClass('hidden-xs');
        $('#message-current').addClass('hidden-xs');
    });
  }


  // thread list ------------------------------------------------------------------------

  this.loadUserThreads = function() {
    if (self.cond()) {
      if (self.already_loading == false) {
        self.already_loading = true;
        self.scroll_target.append('<div style="text-align: center; margin: 10px">Loading ...</div>');

        $.get(message_retrieve_user_threads_url, {page: self.page}).done(self.showUserThreads);
      }
    }
  }

  this.showUserThreads = function(data) {
    if (data.length > 10) {
      self.scroll_target.children().last().remove();
      self.scroll_target.append(data);
      self.already_loading = false;
      self.page++;
      self.scroll_target.find('.message-open-thread-link').click(function(e) {
        e.preventDefault();
        self.clickThread(e);
      });

      // if no thread is opened, open the one on top:
      if(!this.open_thread_id) {
        // @TODO: check if any threads in list
        // @TODO: fake click on the first item
        var links = $('.message-open-thread-link');
        if(links !== 'undefined' && $(window).outerWidth() >= 568) {
          var firstlink = links.first();
          if(firstlink !== 'undefined') {
            firstlink.click();
          }
        }
      }
    } else {
      scroll_target.children().last().html('No more posts !')
        .delay('2000')
        .queue(function() {
            $(this).remove();
        });
        scroll_target.unbind('scroll');
    }
  }


  // current thread --------------------------------------------------------------------

  this.clickThread = function(e) {
    var url         = $(e.currentTarget).attr('href');
    var thread_id   = $(e.currentTarget).attr('data-thread-id');
    
    for(var a = 0; a < e.currentTarget.parentNode.children.length; a++)
    {
      var item = e.currentTarget.parentNode.children[a];

      item.className = item.className.replace(/ selected/ig, '') + ($(item).attr('data-thread-id') == thread_id ? ' selected' : '');
    }
    $('#message-user-threads').addClass('hidden-xs');
    $('#message-current').removeClass('hidden-xs');

    this.loadThread(thread_id);

    // CLEAR new message counter for thread (frontend only)
    $('#message_thread_list_thread_unread_count_' + thread_id).remove();
  }

  this.loadThread = function(thread_id) {

    this.open_thread_id   = thread_id;

    self.updateThreadInput();
    self.updateThreadHeader();
    self.updateThread();

    if(self.thread_update_timer != false) {
      clearInterval(self.thread_update_timer);
      self.thread_update_timer = false;
    }
    this.thread_update_timer = setInterval(function() {
      self.updateThread();
    }, 8400);
  }

  this.showThread = function(data) {
    if(self.last_update_checksum != data)
    {
      self.last_update_checksum = data;
      $('#message-current-thread').html(data);

      setTimeout(self.makeSureScrollyIsDown, 440);
    }
  }

  this.updateThread = function()  {
    var url = message_retrieve_thread_url + "?thread_id=" + self.open_thread_id;
    $.get(url, self.showThread);
  }

  this.updateThreadInput = function()  {
    var header_url = message_retrieve_thread_input_url + '?thread_id=' + self.open_thread_id;
    $.get(header_url, self.showThreadInput);
  }

  this.updateThreadHeader = function()  {
    var header_url = message_retrieve_thread_header_url + '?thread_id=' + self.open_thread_id;
    $.get(header_url, self.showThreadHeader);
  }

  this.showThreadInput = function(data) {
    $('#message-current-input').html(data);

    self.loadThreadHeaderImages();

    // bind some javascripts to the form
    $('#message-form').submit(function(e) {
      e.preventDefault();
      $("#message-input-error").addClass("hidden");
      $("#message-input-submit").addClass("btn--loading");
      // submit form -> redraw screens
      $.post($("#message-form").attr('action'),
            $("#message-form").serialize(),
            function(response) {
                if (response.success) {
                    self.updateThread();
                    self.updateThreadInput();
                } else {
                    $("#message-input-submit").removeClass("btn--loading");
                    $("#message-input-error").removeClass("hidden");
                    $("#message-input-error").text(response.error);
                }
            },
            "json");
    });

    $('#message-file-form-body-input').keypress(function(event) {
      // Check the keyCode and if the user pressed Enter (code = 13)
//      if (event.keyCode == 13) {
////        alert('you pressed enter ^_^');
//        $('#message-form').submit();
//      }
    });

    $('#message-file-form-body-input').focus();

    $('#message-file-form-file-dropzone').filedrop({
      fallback_id: 'message-file-form-file-input',   // an identifier of a standard file input element
      url: $("#message-file-form").attr('action'),              // upload handler, handles each file separately, can also be a function taking the file and returning a url
      paramname: $("#message-file-form-file-input").attr('name'),          // POST parameter name used on serverside to reference file
//      withCredentials: true,          // make a cross-origin request with cookies
      data: {
        thread_id: $("#message-file-form-threadid-input").attr('value'),           // send POST variables
//        param2: function(){
//          return calculated_data; // calculate data at time of upload
//        },
      },
//      headers: {          // Send additional request headers
//        'header': 'value'
//      },
      error: function(err, file) {
        switch(err) {
          case 'BrowserNotSupported':
            alert('browser does not support HTML5 drag and drop')
            break;
          case 'TooManyFiles':
            // user uploaded more than 'maxfiles'
            break;
          case 'FileTooLarge':
            // program encountered a file whose size is greater than 'maxfilesize'
            // FileTooLarge also has access to the file which was too large
            // use file.name to reference the filename of the culprit file
            break;
          case 'FileTypeNotAllowed':
          // The file type is not in the specified list 'allowedfiletypes'
          default:
            break;
        }
      },
      allowedfiletypes: [
        'image/jpeg',
        'image/png',
        'image/gif',
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      ],   // filetypes allowed by Content-Type.  Empty array means no restrictions
      maxfiles: 1,
      maxfilesize: 20,    // max file size in MBs
//      dragOver: function() {
//        // user dragging files over #dropzone
//      },
//      dragLeave: function() {
//        // user dragging files out of #dropzone
//      },
//      docOver: function() {
//        // user dragging files anywhere inside the browser document window
//      },
//      docLeave: function() {
//        // user dragging files out of the browser document window
//      },
//      drop: function() {
//        // user drops file
//      },
//      uploadStarted: function(i, file, len){
//        // a file began uploading
//        // i = index => 0, 1, 2, 3, 4 etc
//        // file is the actual file of the index
//        // len = total files user dropped
//      },
//      uploadFinished: function(i, file, response, time) {
//        // response is the data you got back from server in JSON format.
//      },
//      progressUpdated: function(i, file, progress) {
//        // this function is used for large files and updates intermittently
//        // progress is the integer value of file being uploaded percentage to completion
//      },
//      globalProgressUpdated: function(progress) {
//        // progress for all the files uploaded on the current instance (percentage)
//        // ex: $('#progress div').width(progress+"%");
//      },
//      speedUpdated: function(i, file, speed) {
//        // speed in kb/s
//      },
//      rename: function(name) {
//        // name in string format
//        // must return alternate name as string
//      },
//      beforeEach: function(file) {
//        // file is a file object
//        // return false to cancel upload
//      },
//      beforeSend: function(file, i, done) {
//        // file is a file object
//        // i is the file index
//        // call done() to start the upload
//      },
      afterAll: function() {
        // runs after all files have been uploaded or otherwise dealt with
        //alert('refresh the uploaded file thing');
        self.loadThreadHeaderImages();
      }
    });

  }

  this.showThreadHeader = function(data) {
    $('#message-current-header').html(data);
  }

  this.loadThreadHeaderImages = function()
  {
    var message_retrieve_thread_header_images = message_retrieve_thread_header_images_url + '?thread_id=' + self.open_thread_id;
    $.get(message_retrieve_thread_header_images, self.showThreadHeaderImages);
  }

  this.showThreadHeaderImages = function(data)
  {
    (data.replace(/\s/ig, '') == '' ? $('#message-form-files').hide() : $('#message-form-files').show());

    $('#message-form-files').html(data);
    $('.message_thread_delete_attachment').click(function() {
      //alert('remove image (messagecenter)');
      // call to url : message_delete_images_url
      // callback: self.loadThreadHeaderImages();
      $.post(message_delete_images_url, { thread_id: self.open_thread_id }, function() {
        self.loadThreadHeaderImages();
      });
    });
  }



  this.makeSureScrollyIsDown = function()
  {
    var action_needed = self.doMakeSureScrollyIsDown();
    if(action_needed)
    {
      setTimeout(self.makeSureScrollyIsDown, 440);
    }
  }

  this.doMakeSureScrollyIsDown = function()
  {
    $('#message-current-thread').scrollTop($('#message-current-thread')[0].scrollHeight);
    var changed = false;
    var scrolltop = $('#message-current-thread').scrollTop();
    var scrollheight = $('#message-current-thread')[0].scrollHeight;
    var windowheight = parseInt($('#message-current-thread').css('height'));
//    console.log('top: ' + scrolltop);
//    console.log('h:   ' + scrollheight);
//    console.log('win: ' + windowheight);
    var test1 = scrollheight - windowheight - 10;
    var test2 = scrolltop;
//    console.log('test1 ' + test1 + '    test2 ' + test2);
    if(test1 > test2)
    {
      changed = true;
    }
    $('#message-current-thread').scrollTop($('#message-current-thread')[0].scrollHeight);
    return changed;
  }

  this.imageLoaded = false;
  this.imagePopup  = function(post, image, elem)
  {
    var loader = '<span class="loading-floater" style="position: absolute; height: 1px; float: left;"><div style="padding: 0; background-color: #000; opacity: 0.6;"><img style="position: absolute; width: 16px; height: 16px; margin: 0; padding: 0; border: none;" src="/images/icons/ajax-loader.gif"></div></span>';
    if ($(elem).parent().find('span.loading-floater').length == 0) {
      var img = $(elem);
      var loaderLeftMargin = (img.width() - 16) / 2;
      var loaderTopMargin = (img.height() - 16) / 2;
      $(loader).insertBefore($(elem));
      $(elem).parent().find('span.loading-floater img').css('left', loaderLeftMargin).css('top', loaderTopMargin);
      $(elem).parent().find('span.loading-floater div').css('width', img.width()+2).css('height', img.height()+7);
    }
    var item = '#' + post.replace('_image', '_popup');
    
    self.imageLoaded = false;

      // preload image data - for processing image dimenstions
      // prevents miss fire of the resizePopup() function
      var imageObj = new Image();
      imageObj.src = image;
      $(imageObj).load(function(){
        $(item).bPopup
        ({
          modalColor: '#000000',
          position: ['auto',50],
          opacity: 0.8,
          onOpen: function()
          {
            $(item).css({'display':'block'});

            $(item + ' a.btn_prev').addClass('disabled');
            $(item + ' a.btn_next').addClass('disabled');

            $(item + ' figure').html('<img src="'+image+'" onload="messageController.resizePopup(\''+item+'\')"/>');

            self.resizePopup(item);
          }
        });
        $(elem).parent().find('span.loading-floater').remove();
      });
      $(imageObj).error(function(){
        $(elem).parent().find('span.loading-floater').remove();
        alert('Error encounterd, image cannot be loaded.');
      });
  };
    
  this.resizePopup = function(item)
  {
    if(!self.imageLoaded)
    {
      $(item + ' figure img').css
      ({
        width : 'auto',
        height: 'auto'
      });

      var maxHeight = ($(window).height() * 0.8) - 55;
      var maxWidth  = ($(window).width() * 0.8);

      var ratioX = $(item + ' figure img').width() > maxWidth   ? maxWidth / $(item + ' figure img').width() : 1;
      var ratioY = $(item + ' figure img').height() > maxHeight ? maxHeight / $(item + ' figure img').height() : 1;
      
      var ratio = ratioX < ratioY ? ratioX : ratioY;

      $(item + ' figure img').css
      ({
        width : ratio * $(item + ' figure img').width(),
        height: ratio * $(item + ' figure img').height()
      });

      if($(item + ' figure img').width() && $(item + ' figure img').height())
      {
        self.imageLoaded = true;
      }
    }
  };

}




$(function() {
  messageController.init();
});
