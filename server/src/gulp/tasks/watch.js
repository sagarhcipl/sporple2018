var gulp 		  = require('gulp');
var config 		  = require('../config');
var browserSync   = require('browser-sync');

// Define the watch task
gulp.task('watch', ['browserSync'], function() {

  gulp.watch(config.styles.src,  ['styles']);
  gulp.watch(config.scripts.src,  ['scripts']);
  gulp.watch(config.svg.src,  ['svg']);

});
