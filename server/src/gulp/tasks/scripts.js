'use strict';
 
var gulp 	= require('gulp');
var config 	= require('../config');
var browserify = require('gulp-browserify');
var uglify = require('gulp-uglify');
var browserSync  = require('browser-sync');


gulp.task('scripts', ['vendors', 'browserify']);

gulp.task('vendors', function() {
  
    gulp.src(config.scripts.vendor, { base: config.src + '/js/vendor' })

    	.pipe(gulp.dest(config.scripts.dest + '/vendor'));

});

gulp.task('browserify', function() {
  
    gulp.src(config.browserify.src)
    .pipe(browserify({
         insertGlobals : true
    }))
     .pipe(uglify())

    .pipe(gulp.dest(config.scripts.dest))

    .on('end', function () {
        browserSync.reload();
    });

});
