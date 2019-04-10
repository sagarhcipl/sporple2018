'use strict';

var global 			= require('./base/global');
var loginMod 		= require('./components/header/login-mod');
var landingPage 	= require('./pages/landing-page/landing-page');
var signUp 			= require('./pages/page--sign-up/page--sign-up');

global();
loginMod();
landingPage();
signUp();
