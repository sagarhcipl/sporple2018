/*
 * Functions related to the login module
 *
 */

var parsley = require('parsleyjs');

module.exports = function() {
    'use strict';

    var $register_form;
    var $forgot_password_form;

    function tryLogin($form, url, data){
        var $submitBtn = $form.find('#login_form__submit');

        //notify user that we are working
        $submitBtn.addClass('btn--loading');

        $.ajax({
            type: 'POST',
            url: url,
            data: data,
            dataType: 'json',
            success: function (data) {
                if (data.loggedIn) {
                    mixpanel.track('login_success');
                    window.location.href = data.redirectUrl || '/';
                } else {
                    var $emailField = $form.find('input[name="signin[username]"]');
                    var pwdField = $form.find('input[name="signin[password]"]').parsley();

                    //reset submit val
                    $submitBtn.removeClass('btn--loading');

                    //login form html is returned but we dont want to use that
                    //just set error
                    $emailField.addClass('error');
                    window.ParsleyUI.addError(pwdField, 'loginError', 'Your email or password is incorrect');

                    //remove errors when user edits the form
                    $form.on('focus','input', function(){
                        $emailField.removeClass('error');
                        window.ParsleyUI.removeError(pwdField, 'loginError');

                        //unbind
                        $form.off('focus','input');
                    });
                }
            }
        });
    }

    function facebookSignup(url, data) {
        var $fbBtn = $register_form.find('.btn--fb');
        $fbBtn.addClass('btn--loading');

        $.ajax({
            type: 'POST',
            url: url,
            data: data,
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                    alert(data.redirectUrl);
                    window.location.href = data.redirectUrl;
                } else {
                    $fbBtn.removeClass('btn--loading');
                    alert("There was some error processing your request, please try again");
                }
            },
            error: function() {
                $fbBtn.removeClass('btn--loading');
                alert("There was some error processing your request, please try again");
            }
        });
    }

    function tryRegister(url, data){
        var $submitBtn = $register_form.find('button[type="submit"]');

        //notify user that we are working
        $submitBtn.addClass('btn--loading');
        $.ajax({
            type: 'POST',
            url: url,
            data: data,
            dataType: 'json',
            success: function (data) {
                if (data.registerSuccess) {
                    mixpanel.track('register_success');
                    window.location.href = data.redirectUrl || '/';
                } else {
                    //reset submit val
                    $submitBtn.removeClass('btn--loading');
                    var $error_field = $register_form.find('.alert-error');
                    $error_field.text('Your email is already registered');
                    $error_field.removeClass('hidden');

                    //remove errors when user edits the form
                    $register_form.on('focus','input', function(){
                        $error_field.text('');
                        $error_field.addClass('hidden');

                        //unbind
                        $register_form.off('focus', 'input');
                    });
                }
            }
        });
    }

    function tryForgotPassword(url, data){
        var $submitBtn = $forgot_password_form.find('button[type="submit"]');

        // notify users that we are working
        $submitBtn.addClass('btn--loading');
        $.ajax({
            type: 'POST',
            url: url,
            data: data,
            dataType: 'json',
            success: function(data) {
                alert();
                $submitBtn.removeClass('btn--loading');
                if (data.success) {
                    mixpanel.track('forgot_password_success');
                    $('.cd-form-message.success').removeClass('hidden');
                } else {
                    var $emailField = $forgot_password_form.find('input[type="email"]');
                    var emailParsley = $emailField.parsley();
                    $emailField.addClass('error');
                    window.ParsleyUI.addError(emailParsley, 'loginError', 'Could not find email');
                    $forgot_password_form.on('focus', 'input', function(){
                        $emailField.removeClass('error');
                        window.ParsleyUI.removeError(emailParsley, 'loginError');
                        $forgot_password_form.off('focus', 'input');
                    });
                }
            }
        });
    }

    $(function(){
        var $login_form = $('#login_form, .login-form-page-form');

        //add validation to form
        if( $login_form.length ){
            $login_form.parsley();
            $login_form.submit(function(e) {
                var url = $(this).attr('action');
                var data = $(this).serialize();

                tryLogin($(this), url, data);
                return false;
            });
        }

        $register_form = $('#signup-form');

        // add validation
        if ($register_form.length) {
            $register_form.parsley();
            $register_form.submit(function(e) {
                var url = $(this).attr('action');
                var data = $(this).serialize();
                tryRegister(url, data);
                return false;
            });
            $register_form.find('.btn--fb').click(function(e) {
                var url = $(this).attr('data-url');
                var data = $register_form.serialize();
                facebookSignup(url, data);
                return false;
            });
        }

        $forgot_password_form = $('#forgot_password_form');
        // add validation
        if ($forgot_password_form.length) {
            $forgot_password_form.parsley();
            $forgot_password_form.submit(function(e) {
                var url = $(this).attr('action');
                var data = $(this).serialize();
                tryForgotPassword(url, data);
                return false;
            });
        }

        var formModal = $('.cd-user-modal'),
        formLogin = formModal.find('#cd-login'),
        formSignup = formModal.find('#cd-signup'),
        formModalTab = $('.cd-switcher'),
        formForgotPassword = formModal.find('#cd-reset-password'),
        tabLogin = formModalTab.children('li').eq(0).children('a'),
        tabSignup = formModalTab.children('li').eq(1).children('a'),
        signupButton = $('.cd-signup'),
        mainNav = $('.main-nav');
        var backToLoginLink = formForgotPassword.find('.cd-form-bottom-message a'),
        forgotPasswordLink = formLogin.find('.cd-form-bottom-message a');

        // open modal
        mainNav.on('click', function(event){
            $(event.target).is(mainNav) && mainNav.children('ul').toggleClass('is-visible');
        });

        //open login-form form
        mainNav.on('click', '.cd-signin', login_selected);
        $('.open-signin').click(login_selected);
        backToLoginLink.on('click', function(event){
            login_selected();
            return false;
        });
        forgotPasswordLink.on('click', function(event){
            forgot_password_selected();
            return false;
        });
        $('.forgot-password-link').click(function() {
            forgot_password_selected();
            return false;
        });

        //close modal
        formModal.on('click', function(event){
        if( $(event.target).is(formModal) || $(event.target).is('.cd-close-form') ) {
            formModal.removeClass('is-visible');
        }
        });
        //close modal when clicking the esc keyboard button
        $(document).keyup(function(event){
            if(event.which=='27'){
                formModal.removeClass('is-visible');
            }
        });

        //switch from a tab to another
        tabLogin.on('click', function(event){
            event.preventDefault();
            login_selected();
        });

        function login_selected(){
            mixpanel.track('login_selected');
            mainNav.children('ul').removeClass('is-visible');
            formModal.addClass('is-visible');
            formLogin.addClass('is-selected');
            formForgotPassword.removeClass('is-selected');
            tabLogin.addClass('selected');
        }

        function forgot_password_selected(){
            mixpanel.track('forgot_password');
            formModal.addClass('is-visible');
            formLogin.removeClass('is-selected');
            formForgotPassword.addClass('is-selected');
            tabLogin.addClass('selected');
        }


        // Signup Page
        var triggerBttn = $('.open-sign-up'),
        transEndEventNames = {
          'WebkitTransition': 'webkitTransitionEnd',
          'MozTransition': 'transitionend',
          'OTransition': 'oTransitionEnd',
          'msTransition': 'MSTransitionEnd',
          'transition': 'transitionend'
        },
        transEndEventName = transEndEventNames[Modernizr.prefixed('transition')],
        support = {
          transitions: Modernizr.csstransitions
        };
        triggerBttn.click(function(e) {
            window.location.href = '/register';
        });

        // Signup Flow
        // Binding next button on first step
        $(".open1").click(function() {
            $(".frm").hide("fast");
            $("#sf2").show("slow");
            var role_id = $('#role-signup').val();
            if (role_id == '3') {
                $('#club-form-group').removeClass('hidden');
            } else {
                $('#club-form-group').addClass('hidden');
            }
        });
 
        // Binding next button on second step
        $(".open2").click(function() {
            $(".frm").hide("fast");
            $("#sf3").show("slow");
        });
    });
};
