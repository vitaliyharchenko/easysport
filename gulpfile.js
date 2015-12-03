'use strict';

var gulp = require('gulp'),
    jade = require('gulp-jade'),
    rigger = require('gulp-rigger'),
    sourcemaps = require('gulp-sourcemaps'),
    sass = require('gulp-sass'),
    prefixer = require('gulp-autoprefixer'),
    cssmin = require('gulp-minify-css'),
    watch = require('gulp-watch'),
    rimraf = require('rimraf'),
    uglify = require('gulp-uglify'),
    imagemin = require('gulp-imagemin'),
    pngquant = require('imagemin-pngquant');

var path = {
    build: {
        templates: 'templates/',
        js: 'static/js/',
        style: 'static/css/',
        fonts: 'static/fonts/',
        img: 'static/images/'
    },
    src: {
        jade: 'src/jade/**/*.jade',
        js: 'src/js/**/*.js',
        style: 'src/style/**/*.scss',
        bootstrapfonts: 'bower_components/bootstrap-sass/assets/fonts/**/*.*',
        img: 'src/images/**/*.*'
    },
    watch: {
        jade: 'src/jade/**/*.jade',
        js: 'src/js/**/*.js',
        style: 'src/style/**/*.scss',
        img: 'src/images/**/*.*'
    },
    clean: {
        templates: 'templates/'
    }
};

gulp.task('templates:clean', function (cb) {
    rimraf(path.clean.templates, cb);
});

gulp.task('jade:build' , function () {
    gulp.src(path.src.jade)
        .pipe(jade({
            pretty: true
        }))
        .on('error', console.log)
        .pipe(rigger())
        .pipe(gulp.dest(path.build.templates));
});

gulp.task('js:build', function () {
    gulp.src(path.src.js)
        .pipe(rigger())
        .pipe(sourcemaps.init())
        .pipe(uglify())
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(path.build.js));
});

gulp.task('style:build', function () {
    gulp.src(path.src.style)
        .pipe(sourcemaps.init())
        .pipe(sass({
            sourceMap: true,
            errLogToConsole: true
        }))
        .pipe(prefixer())
        .pipe(cssmin())
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(path.build.style));
});

gulp.task('fonts:build', function() {
    gulp.src(path.src.bootstrapfonts)
        .pipe(gulp.dest(path.build.fonts))
});

gulp.task('image:build', function () {
    gulp.src(path.src.img)
        .pipe(imagemin({
            progressive: true,
            svgoPlugins: [{removeViewBox: false}],
            use: [pngquant()],
            interlaced: true
        }))
        .pipe(gulp.dest(path.build.img));
});

gulp.task('clean', [
    'templates:clean',
]);

gulp.task('build', [
    'jade:build',
    'js:build',
    'style:build',
    'fonts:build',
    'image:build',
]);

gulp.task('watch', function(){
    watch([path.watch.jade], function(event, cb) {
        gulp.start('jade:build');
    });
    watch([path.watch.js], function(event, cb) {
        gulp.start('js:build');
        gulp.start('jade:build');
    });
    watch([path.watch.style], function(event, cb) {
        gulp.start('style:build');
        gulp.start('jade:build');
    });
    watch([path.watch.img], function(event, cb) {
        gulp.start('image:build');
    });
});

gulp.task('default', ['build', 'watch']);