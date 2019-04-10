/*
 * profile pic editor plugin
 *
 */

var modal = require('./modal');
var cropper = require('cropper');

var inputPrefix = 'profile';
var options = {
    inputPrefix: 'profile',
    modalClassName: 'photo-crop--profile-pic',
    aspectRatio: 1
};


var setup = function(file, args) {

    if (args.inputPrefix) options.inputPrefix = args.inputPrefix;
    if (args.modalClassName) options.modalClassName = args.modalClassName;
    if (args.aspectRatio) options.aspectRatio = args.aspectRatio;
    if (args.callback) options.callback = args.callback;
           
    drawImage(file);
}
 
/*
 * Read uploaded image into base64
 * 
 */

var drawImage = function(file, prefix) {

    var fileReader = new FileReader();

    //do we have an input prefix
    if (prefix) options.inputPrefix = prefix;

    //check if file is not too big
    if (file.size > 8250 * 1024) {
        alert('Sorry, this image is too big!');
        return false;
    }
       
    //read file    
    fileReader.readAsDataURL(file);
    
    fileReader.onload = function () {
        var imageData = this.result;
        
        crop(imageData);
    };
}


/*
 * image cropper
 * 
 */
var crop = function(img) {
    var $formX = $('#'+options.inputPrefix+'_image_x1');
    var $formY = $('#'+options.inputPrefix+'_image_y1');
    var $formW = $('#'+options.inputPrefix+'_image_w');
    var $formH = $('#'+options.inputPrefix+'_image_h');
    var $formR = $('#'+options.inputPrefix+'_rotation');
    var $cropperCont = undefined;
    var lastZoomVal = 0.3; //start 0.3 because the init autoCropArea is 0.7 (its been changed to 0.8 because the calculation is off by 0.1 somewhere)
    var zoomThrottle = undefined;
    var cropHtml = '<div id="cropper">'+
        '<div class="cropper__preview-cont">'+
            '<img id="cropper__img" src="" alt="">'+
        '</div>'+
        '<div class="cropper__controls-wrapper">'+
            '<svg class="icon sign-up-form__small-pic-icon" role="presentation" viewBox="0 0 14 14">'+
                '<use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/images/svg/foreground-svg.svg#picture"></use>'+
            '</svg>'+
            '<input type="range" id="cropper-cont__zoom" min="0" max="2" step="0.1" value="0.3" />'+
            '<svg class="icon sign-up-form__big-pic-icon" role="presentation" viewBox="0 0 14 14">'+
                '<use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/images/svg/foreground-svg.svg#picture"></use>'+
            '</svg>'+
            '<button id="cropper-cont__rotate">'+
                '<svg class="icon sign-up-form__rotate-icon" role="img" title="rotate 90 degrees" viewBox="0 0 28 25">'+
                    '<use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/images/svg/foreground-svg.svg#rotate"></use>'+
                '</svg>'+
            '</button>'+
        '</div>'+
    '</div>';


    modal.setup(
        cropHtml,
        {
            title: 'Crop photo',
            classes: options.modalClassName,
            success: function() {
                var data = $cropperImg.cropper('getData',true);

                //add values to form
                $formX.val( Math.round(data.x) );
                $formY.val( Math.round(data.y) );
                
                $formW.val( Math.round(data.width) );
                $formH.val( Math.round(data.height) );
                
                $formR.val(data.rotate);

                //close modal
                modal.close();

                if (options.callback && typeof options.callback === 'function') {
                    options.callback();
                }
            }
        }
     );

    $cropperImg = $('#cropper__img');

    if(img) {

        $cropperImg
            .attr('src',img)
            
            .cropper({
                dragCrop: false,
                cropBoxMovable: false,
                cropBoxResizable: false,
                aspectRatio: options.aspectRatio,
                autoCropArea: 0.8,
                guides: false,
                highlight: false,
                mouseWheelZoom: false,
                preview: '#'+options.inputPrefix+'-crop-preview'
            });

        modal.open();

    } else {

        //$cropperCont.cropit();
    }

    //bind custom rotate btn
    $('#cropper-cont__rotate').click(function(){

        $cropperImg.cropper("rotate", 90);

    });

    //custom zoom
    $('#cropper-cont__zoom')
    .on('change', function() {

        //cropper zoom only accepts in or out in the form of -0.1 or 1.0
        //so we convert the range to that
        var zoomInput = $(this).val();
        var zoomOutput = 0;

        clearTimeout(zoomThrottle);

        zoomThrottle = setTimeout(function(){

            if(zoomInput == lastZoomVal) {

                return false;

            } else if(zoomInput > lastZoomVal) {

                zoomOutput = parseFloat( (zoomInput - lastZoomVal).toFixed(2) );
                //must be positive
                if(zoomOutput < 0) zoomOutput = zoomOutput * -1;

            } else if(zoomInput < lastZoomVal) {

                zoomOutput = parseFloat( (lastZoomVal - zoomInput).toFixed(2) );
                //must be negative
                if(zoomOutput > 0) zoomOutput = zoomOutput * -1;
            }

            //update last zoom
            lastZoomVal = zoomInput;

            //zoom
            $cropperImg.cropper("zoom", zoomOutput);

        }, 50);

    });

}


module.exports = {
    setup: setup,
    drawImage: drawImage
};
