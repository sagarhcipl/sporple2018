'use strict';
 
var gulp 	= require('gulp');
var config 	= require('../config');
var sass 	= require('gulp-sass');
var browserSync  = require('browser-sync');
var autoprefixer = require('gulp-autoprefixer');
var cmq          = require('gulp-combine-media-queries');
var minifycss    = require('gulp-minify-css');
var gutil        = require('gulp-util');
 

gulp.task('styles', function () {
  
     gulp.src(config.styles.src)
  	//compile sass
    .pipe(sass().on('error', sass.logError))

    //add vendor prefixes
    .pipe(autoprefixer({
            browsers: ['ie 8', 'ie 9', 'last 5 versions']
        })
    )

    //combine media queries
    .pipe(cmq({log: true }))

    //minify
    .pipe(minifycss())

    //add to destination folder
    .pipe(gulp.dest( config.styles.dest ))

    //reload site
    .pipe(browserSync.reload({stream:true}));

});
 
