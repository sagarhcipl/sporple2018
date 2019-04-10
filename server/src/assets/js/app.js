'use strict';

var global = require('./base/global');
var home = require('./pages/page--home/page--home');
var profile = require('./pages/page--profile/page--profile');
var messages = require('./pages/page--messages');
var searchResults = require('./pages/page--search');
var loginMod = require('./components/header/login-mod');
var sendMessage = require('./components/send-message');
var settings = require('./pages/page--settings');
var signUp = require('./pages/page--sign-up/page--sign-up');
var autoRegister = require('./pages/page--autoregister');
var invite = require('./pages/page--invite');

global();
loginMod();
settings();
signUp();

$(function(){

	home.setup();
	profile.setup();
	messages.setup();
	searchResults.setup();

	sendMessage.setup();
    autoRegister.setup();
    invite.setup();
});

