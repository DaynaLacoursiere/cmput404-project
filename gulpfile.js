var gulp        = require('gulp');
var browserSync = require('browser-sync');
var reload      = browserSync.reload;

// Send html to build
gulp.task('html', function(){
  return gulp.src('./src/html/*.html')
          .pipe(gulp.dest('./build/html/'));
})

// Send css to build
gulp.task('css', function(){
  return gulp.src('./src/css/*.css')
          .pipe(gulp.dest('./build/css/'));
})

// Send js to build
gulp.task('js', function(){
  return gulp.src('./src/js/*.js')
          .pipe(gulp.dest('./build/js/'));
})

// Send img to build (general * in case of gif, svg, etc)
gulp.task('img', function(){
  return gulp.src('./src/img/*')
          .pipe(gulp.dest('./build/img/'));
})

// Send python to build
gulp.task('python', function(){
  return gulp.src('./src/python/*.py')
          .pipe(gulp.dest('./build/python/'));
})

// Send index to build
gulp.task('index', function(){
  return gulp.src('./src/index.html')
          .pipe(gulp.dest('./build/'));
})

// Serve and watch for changes
gulp.task('default', ['html', 'css', 'js', 'img', 'python', 'index'], function(){
  browserSync({server: './build'});

  gulp.watch('./src/html/*.html', ['html']);
  gulp.watch('./src/css/*.css', ['css']);
  gulp.watch('./src/js/*.js', ['js']);
  gulp.watch('./src/img/*', ['img']);
  gulp.watch('./src/python/*.py', ['python']);
  gulp.watch('./src/index.html', ['index']);
});