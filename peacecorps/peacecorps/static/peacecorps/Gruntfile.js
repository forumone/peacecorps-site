/*global module:false*/
'use strict';
module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    // Metadata.
    pkg: grunt.file.readJSON('package.json'),
    banner: '/*! <%= pkg.title || pkg.name %> - v<%= pkg.version %> - ' +
      '<%= grunt.template.today("yyyy-mm-dd") %>\n' +
      '<%= pkg.homepage ? "* " + pkg.homepage + "\\n" : "" %>' +
      '* Copyright (c) <%= grunt.template.today("yyyy") %> <%= pkg.author.name %>;' +
      ' Licensed <%= _.pluck(pkg.licenses, "type").join(", ") %> */\n',
    // Task configuration.
    uglify: {
      options: {
        banner: '<%= banner %>',
        sourceMap: true
      },
      dist: {
        src: '<%= browserify.donation.dest %>',
        dest: './js/compiled/<%= pkg.name %>-donation.min.js'
      }
    },
    jshint: {
      all: ['./js/src/**/*.js'],
      options: {
        jshintrc: './.jshintrc'
      }
    },
    browserify: {
      donation: {
        options: {
          browserifyOptions: {
             debug: true
          },
          banner: '<%= banner %>',
        },
        dest: './js/compiled/<%= pkg.name %>-donation.js',
        src: './js/src/**/*.js'
      },
      withWatch: {
        options: {
          browserifyOptions: {
             debug: true
          },
          watch: true
        },
        dest: './js/compiled/<%= pkg.name %>-donation.js',
        src: './js/src/**/*.js'
      }
    },
    watch: {
      jshint: {
        files: '<%= jshint.all =>',
        tasks: ['jshint']
      }
    }
  });

  // These plugins provide necessary tasks.
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-watch');

  grunt.loadNpmTasks('grunt-browserify');

  // Default task.
  grunt.registerTask('default', ['build']);
  grunt.registerTask('build', ['jshint', 'browserify:donation', 'uglify']);
  grunt.registerTask('buildWatch', ['browserify:withWatch', 'watch']);
};
