'use strict';

global.jQuery = window.$ = require('jquery');
global.config = require('./config');
var forms = require('./forms');
var dropdownMenu = require('../components/dropdown-menu');
var search = require('../components/header/search');
var notifications = require('../components/header/notifications');
var alerts = require('../components/alerts');
var scroll = require('../components/scroll');
var checkout = require('../components/checkout');
var more = require('../components/more');
var relate = require('../components/relate');
require('../components/floating-labels');

if( Modernizr && Modernizr.svg){
	var svg4everybody = require('svg4everybody');
}


module.exports = function() {

	if (Modernizr && Modernizr.svg) {
		svg4everybody();
	}

	//check if is modern browser and set in client cache
	config.isModern();
	//get user data
	config.getUserData();

	//doc ready functions
	$(function() {

		//set commen jQ elements to cache
		global.config.setjQEles();
		forms.setup();
		dropdownMenu.setup();
		search.setup();
		alerts.setup();
        scroll.setup();
        relate.setup();
        checkout();
        more();

		//wait a little to help bring attention to the notifs
		setTimeout(function(){
			notifications.setup();
		},3000);

	});
};
