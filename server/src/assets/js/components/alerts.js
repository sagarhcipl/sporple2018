/*
 * Factory for alert message
 *
 */

var helpers = require('./../base/helpers');
var initialTO = 2000;
var $mainCont = undefined;
var $bannerAlert = undefined;
var $headerAlert = undefined;
var allowedPages = ['home','profile'];
var closeSvg = '<svg preserveAspectRatio="xMidYMid" width="17.156" height="17.156" viewBox="0 0 17.156 17.156" title="close">' +
  '<path d="M16.682,2.540 L10.690,8.532 L16.585,14.428 C17.166,15.009 17.166,15.949 16.585,16.530 C16.005,17.110 15.064,17.110 14.483,16.530 L8.587,10.634 L2.540,16.682 C1.954,17.268 1.004,17.268 0.419,16.682 C-0.167,16.096 -0.167,15.147 0.419,14.561 L6.466,8.513 L0.470,2.517 C-0.111,1.936 -0.110,0.995 0.470,0.415 C1.050,-0.166 1.992,-0.166 2.572,0.415 L8.568,6.411 L14.561,0.419 C15.146,-0.167 16.096,-0.167 16.682,0.419 C17.268,1.004 17.268,1.954 16.682,2.540 Z"/>' +
'</svg>';
var bannerCookieHTML = '<figure id="cookie-banner" class="cookie-banner new-school">' +
        '<div class="grid no-cols">'+
            '<a class="cookie-banner__close">{X}</a>' +
            '<figcaption><p>We are using cookies to improve your experience. To learn more please see our ' +
            '<a href="https://newsroom.sporple.com/privacy-cookies/" target="_blank">Privacy & Cookies Policy</a></p></figcaption>' +
        '</div>' +
    '</figure>';
var bannerHTML = '<figure id="" class="alert-banner new-school">' +
        '<a class="alert-banner__close">X</a>' +
        '<figcaption class="ttl3">{{title}}</figcaption>' +
        '<p>{{message}}</p>' +
        '<div>' +
            '<a href="" class="btn btn--cta">Resend Confirmation</a>' +
            '<a href="" class="btn btn--text">Update email address</a>' +
        '</div>' +
    '</figure>';


var _showBannerAlert = function(data) {

    $mainCont.prepend(bannerHTML);

};

var _showCookieBanner = function() {
    var banner = bannerCookieHTML.replace('{X}',closeSvg);
    var $banner = $(banner);

    config.jQEles.$bod.prepend($banner);

    $banner.find('a.cookie-banner__close').click(function(e) {
        e.preventDefault();

        _closeBanner($banner, false, function(){ 
            helpers.setCookie('acceptedCookies',1, 365);
        });
    });

    setTimeout(function() {
        $banner.addClass('active');
    }, 100);
    
};


var _prepNoPic = function() {

    _showBannerAlert();
};


var _closeBanner = function($banner, squash, cb) {

    $banner.removeClass('active');

    if (squash) {
        $banner.css('max-height', 0);
    }

    setTimeout(function() {

        $banner.remove();

        if (!!cb && typeof cb === 'function') {
            cb();
        }
    }, 400);

};


var _bind = function() {
    var $profilePicBanner = $('#alert-banner-profile-pic');
    var transitionDuration = 300;
    
    //generic close button bind
    $('a.alert-banner__close')
    .off('click')
    .click(function() {

        var $banner = $(this).parent('figure.alert-banner');

        _closeBanner($banner, true);
    });

    //specific profile pic
    if ($profilePicBanner.length) {

        $profilePicBanner.find('a.btn').click(function() {

            _closeBanner($profilePicBanner, true);
        });
    }
    
};


var _checkForAlerts = function() {

    if (!helpers.getCookie('acceptedCookies')) {
        _showCookieBanner();
    }

    // if (config.userData && config.userData.missing_profile_pic) {
    //     _prepNoPic();
    // }
};


var show = function(message) {
    if (!$headerAlert) {
        $headerAlert = $('.header-alert');
    }
    $headerAlert.find('.alert-message').html(message);
    $headerAlert.fadeIn('slow');
    setTimeout(function() {
        $headerAlert.fadeOut('fast');
    }, 3000);
}

var setup = function() {

    $mainCont = $('#main_container');
    $headerAlert = $('.header-alert');
    
    //check for any initial alerts to display
    setTimeout(function() {

        _checkForAlerts();

        _bind();

    }, initialTO);

};


module.exports = {
    setup: setup,
    show: show
};
