'use strict';

//HEPER FUNCTIONS

module.exports = {

    setCookie: function(name, value, days) {
        var expires;

        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toGMTString();
        }
        else {
            expires = "";
        }

        document.cookie = name + "=" + value + expires + "; path=/";

    },

    getCookie: function(name) {
        var c_start = undefined;
        var c_end = undefined;

        if (document.cookie.length > 0) {

            c_start = document.cookie.indexOf(name + "=");

            if (c_start != -1) {
                c_start = c_start + name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) {
                    c_end = document.cookie.length;
                }

                return unescape(document.cookie.substring(c_start, c_end));
            }
        }

        return false;
    },

    deleteCookie: function (sKey, sPath, sDomain) {
        
        this.setCookie(sKey, "", -1);
        return true;
    },

    getQueryStr: function(key) {  
        return unescape(window.location.search.replace(new RegExp("^(?:.*[&\\?]" + escape(key).replace(/[\.\+\*]/g, "\\$&") + "(?:\\=([^&]*))?)?.*$", "i"), "$1"));  
    } 

};
