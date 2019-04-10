'use strict';

var dest    = './main/static/';
var src     = './assets/';
var proxy   = 'local.sporple.com';

module.exports = {

    src: src,
    dest: dest,

    browserSync: {
        proxy: proxy,
        //server: {
        //    baseDir: dest.root,
        //}//,
        //tunnel: "example"
    },

    styles: {
        src:    src + '/scss/**/*.scss',
        dest:   dest + '/css/frontend'
    },

    scripts: {
        vendor: src + '/js/vendor/**/*.js',
        src: src + '/js/**/*.js',
        dest: dest + '/js/frontend',

        lint: [
            src + '/assets/js/**/modules/*.js',
            src + '/modules/**/*.js'
        ]
    },

    browserify: {
        src: src + '/js/*.js'
    },

    svg: {
        spriteSrc:    src + '/img/svg/foreground-svg/*.svg',
        src:    src + '/img/svg/*.svg',
        dest:   dest + '/images/svg'
    }

};
