/**
 *
 Media (cover image / showreel & images) functionality for image gallery.
 */


var modal = require('./modal');
var slick = require('slick-carousel');

var $mediaContainer = undefined;
var slickInstance = undefined;


var _openImagePopup = function(clickedIndex) {
    var $allImages =$mediaContainer.find('.image');
    var modalHtmlArray = ['<div class="image-viewer-cont--multiple">'];
    var modalHtml = undefined;
    var _img = undefined;

    // kill previous carousels
    if (!! slickInstance) {
        $('div.image-viewer-cont--multiple').slick('unslick');
    }

    // -- build modal carousel -- //
    // add all images
    for (var i = 0; i < $allImages.length; i++) {
        var imgUrl = $($allImages[i]).children('a').attr('href');
        var html = '<div><img src="' + imgUrl + '" alt=""></div>';
        modalHtmlArray.push(html);

        // preload the selected image
        if (i === clickedIndex) {
            try {
                _img = new Image();
                _img.src = imgUrl;
            } catch (e) {
            }
        }
    }

    modalHtmlArray.push('</div>' + '<button class="image-viewer-cont__btn-prev" tabindex="3">Previous</button><button class="image-viewer-cont__btn-next" tabindex="2">Next</button>');
    modalHtml = modalHtmlArray.join('');

    // setup modal
    modal.setup(
        modalHtml,
        {
            classes: 'modal--image-viewer modal--image-viewer-multiple',
            noBtns: true,
            callback: function() {
                var $caro = $('div.image-viewer-cont--multiple');

                // init slick carousel
                slickInstance = $caro.slick({
                    speed: '400',
                    initialSlide: clickedIndex,
                    prevArrow: 'button.image-viewer-cont__btn-prev',
                    nextArrow: 'button.image-viewer-cont__btn-next',
                    cssEase: 'ease-out',
                });

                setTimeout(function() {
                    modal.open();
                    config.jQEles.$modal.focus();
                }, 50);
            }
        });
};


var _bind = function() {
    $mediaContainer.on('click', 'a.thumb', function(e) {
        var $this = $(this);
        var i = parseInt($this.attr('data-index'));
        _openImagePopup(i);
        return false;
    });
};

var setup = function() {
    $mediaContainer = $('.gallery .image-container');
    if ($mediaContainer.length) {
        _bind();
    }
};

module.exports = {
    setup: setup
};

