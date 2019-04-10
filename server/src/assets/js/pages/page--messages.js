/*
 * Functionality for the Messages page
 *
 */

var modal = require('./../components/modal');

var $pageCont = undefined;

var _openMessageImg = function(imgUrl) {

    var modalHtml = '<div class="image-viewer__img-cont">' +
            '<img src="' + imgUrl + '" alt="">' +
        '</div>';

    //set up modal
    modal.setup(
        modalHtml,
        {
            classes: 'modal--image-viewer',
            noBtns: true,
            callback: function() {

                modal.open(); 
            }
        }
    );

};


var _bind = function() {
    var $msgThreadCont = $pageCont.find('#message-current-thread');
    $msgThreadCont
        .on('click', 'img.upload_image', function() {
            var imgUrl = $(this).attr('src');
            _openMessageImg(imgUrl);
        });

    
};


var setup = function() {
    
    $pageCont = $('section.page--messages');

    if ($pageCont.length) {

        _bind();

    }

};


module.exports = {
    setup: setup
};
