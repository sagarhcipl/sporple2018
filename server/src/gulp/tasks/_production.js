'use strict';

var gulp        = require('gulp');
var runSequence = require('run-sequence');


gulp.task('production', function(cb) {

  cb = cb || function() {};

  global.isProd = false;

  runSequence('styles', 'browserify', 'svg', cb);

});

// Assign a shortcut task to development
gulp.task('prod', ['production']);
