'use strict';

var gulp        = require('gulp');
var runSequence = require('run-sequence');

//gulp.task('development', ['clean'], function(cb) {

gulp.task('development', function(cb) {

  cb = cb || function() {};

  global.isProd = false;

  runSequence('styles', 'scripts', 'svg', 'watch',cb);

});

// Assign the default task to development
gulp.task('default', ['development']);

// Assign a shortcut task to development
gulp.task('dev', ['development']);


