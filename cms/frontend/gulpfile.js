/**
    前端优化：代码合并、代码压缩(图片压缩)、缓存处理(添加版本号)、部署CDN
    开发流程优化：开启本地服务&热替换，本地环境和线上环境
*/
var gulp = require('gulp'),
	rev = require('gulp-rev'),
	revReplace = require('gulp-rev-replace'),
	connect = require('gulp-connect'),
	del = require('del'),
	override = require('gulp-rev-css-url'),
	cached = require('gulp-cached'),
	imagemin = require('gulp-imagemin'), //图片压缩
	cleanCSS = require('gulp-clean-css'), //css压缩
	// jshint = require('gulp-jshint'),           //js检查
	uglify = require('gulp-uglify'), //js压缩
	rename = require('gulp-rename'), //重命名
	concat = require('gulp-concat'), //合并文件
	clean = require('gulp-clean'); //清空文件夹

var config = {
	src: {
		path: './static/',
		static: {
			app: './templates/',
			css: './static/css/',
			js: './static/js/',
			img: './static/images/',
			font: './static/fonts/'
		}
	},
	dist: {
		path: './assets/',
		static: {
			app: './assets/templates/',
			css: './assets/static/css/',
			js: './assets/static/js/',
			img: './assets/static/images/',
			font: './assets/static/fonts/'
		}
	},
	rev: './rev/'
};

var manifest = {
	base: 'rev-manifest.json',
	css: 'rev-css-manifest.json',
	js: 'rev-js-manifest.json',
	img: 'rev-img-manifest.json'
};

gulp.task('rev_minify_css', ['clear'], function() {
	return gulp.src([config.src.static.css + '**/*'], {
			base: config.src.path
		})
		.pipe(cached('minify_css'))
		// .pipe(cleanCSS())
		.pipe(rev())
		.pipe(gulp.dest(config.dist.path + 'static/'))
		.pipe(rev.manifest(manifest.css))
		.pipe(gulp.dest(config.rev));
});

gulp.task('rev_minify_js', ['clear'], function() {
	return gulp.src([config.src.static.js + '**/*'], {
			base: config.src.path
		})
		// .pipe(uglify())
		.pipe(rev())
		.pipe(gulp.dest(config.dist.path + 'static/'))
		.pipe(rev.manifest(manifest.js))
		.pipe(gulp.dest(config.rev));
});

gulp.task('rev_minify_img', ['clear'], function() {
	return gulp.src([config.src.static.img + '**/*'], {
			base: config.src.path
		})
		// .pipe(imagemin())
		.pipe(rev())
		.pipe(gulp.dest(config.dist.path + 'static/'))
		.pipe(rev.manifest(manifest.img))
		.pipe(gulp.dest(config.rev));
});

gulp.task('rev_minify', ['rev_minify_css', 'rev_minify_js', 'rev_minify_img']);

gulp.task('cp-html', ['clear'], function() {
	return gulp.src(config.src.static.app + '**/*')
		.pipe(gulp.dest(config.dist.static.app));
});

gulp.task('cp-font', ['clear'], function() {
	return gulp.src(config.src.static.font + '**/*')
		.pipe(gulp.dest(config.dist.static.font));
});

gulp.task('cp', ['cp-html', 'cp-font']);

gulp.task('replace', ['rev_minify', 'cp'], function() {
	return gulp.src(config.dist.path + '**/*')
		.pipe(revReplace({
			manifest: gulp.src('./rev/rev-img-manifest.json')
		}))
		.pipe(revReplace({
			manifest: gulp.src('./rev/rev-css-manifest.json')
		}))
		.pipe(revReplace({
			manifest: gulp.src('./rev/rev-js-manifest.json')
		}))
		.pipe(gulp.dest(config.dist.path));
});

gulp.task('clear', function() {
	return del([config.dist.path, config.rev])
		.then(function(paths) {
			console.log('delete files and folders:\n', paths.join('\n'));
		})
});

gulp.task('default', ['replace']);