'use strict';

var config       = require('../config');
var gulp         = require('gulp');
var svgstore     = require('gulp-svgstore');
var svgmin       = require('gulp-svgmin');
var svg2png      = require('gulp-svg2png');
var browserSync  = require('browser-sync');

// Create SVG sprite
gulp.task('svg', ['svg-sprite-foreground']);

gulp.task('svg-sprite-foreground', function() {

    var singleSvgBasePath = config.svg.src.replace('/*.svg','');

    // Remove fill attribute
    function transformSvg ($svg, done) {
        $svg.find('[fill]').removeAttr('fill').css('fill','');
        done(null, $svg);
    }

    //single svgs
    gulp.src(config.svg.src, { base: singleSvgBasePath })
        .pipe(svgmin())
        .pipe(gulp.dest(config.svg.dest));


    //generate fallback pngs
    gulp.src(config.svg.spriteSrc)
        .pipe(svg2png())
        .pipe(gulp.dest(config.svg.dest));

    //sprite sheet
    return gulp
        
        .src(config.svg.spriteSrc)
        
        .pipe(svgmin())
        
        .pipe(svgstore({
            transformSvg: transformSvg
        }))
        
        .pipe(gulp.dest(config.svg.dest))

        .on('end', function () {
            browserSync.reload();
        });

});
