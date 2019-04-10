'use strict';

module.exports = {

	isModern: function() { 

		if (!config.isModernCached) {

			var h = document.getElementsByTagName('html')[0];
			var isModClass = 'not-modern';

			config.isModernCached = ('querySelector' in document && 'addEventListener' in window && 'localStorage' in window && 'sessionStorage' in window);

			if (config.isModernCached) {

				isModClass = 'is-modern';
			}

			if (navigator.userAgent.indexOf('Safari') > -1 && navigator.userAgent.indexOf('Chrome') === -1) {
				isModClass = isModClass + ' is-safari';	
			}

			h.className = h.className + ' ' + isModClass;
		}

	    return config.isModernCached;
	},
	isModernCached: undefined,
	breakpoints: {
		mobile: 320,
		tablet: 568,
    	desktop: 1024,
    	largedesktop: 1280
	},
	getBreakpoint:  function(){

		var w = $(window).outerWidth();

		if(w < config.breakpoints.tablet){

			return "mobile";

		}else if(w >= config.breakpoints.tablet && w < config.breakpoints.desktop){

			return "tablet";

		}else{

			return "desktop";
		}
	},
	headerHeights: {
		mobile: 60,
		tablet: 60,
    	desktop: 68
	},
	footerHeights: {
		mobile: 154,
		tablet: 125,
    	desktop: 125
	},
	forms: {
		selectWrapperHtml: '<div class="select-wrapper"><span class="select-wrapper__label"></span></div>'
	},
	parsleyDefaultConfig: {
	    errorsContainer: function(pEle) {
	    	var $ele = pEle.$element;
	    	var $errCont = $ele.parent();

	    	if($ele.parent('div.select-wrapper').length) {

	    		$errCont = $ele.parent('div.select-wrapper').parent()
	    	}

	        return $errCont;
	    }
	},
	getUserData: function(cb) {
		var self = this;

	    $.getJSON(main_update_url, function (data) {
	        self.userData = data;

	        if (!!cb && typeof cb === 'function'){
	        	cb();
	        }
	    });
	},
	userData: undefined,
	jQEles: {
		$win: undefined,
		$bod: undefined,
		$modal: undefined
	},
	setjQEles: function(){

		this.jQEles.$win = $(window);
		this.jQEles.$bod = $('body');
		this.jQEles.$modal = $('#modal-bg > #modal');
	},

	fileTypesMsg: [
		'image/jpeg',
		'image/png',
		'image/gif',
		'application/msword',
		'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
		'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
		'application/pdf'
	]

}
