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
    // Constants
    pkgFullName: '<%= pkg.name %>-donation',
    jsBuildDir: './js/compiled/',
    jsSrcDir: './js/src/',
    // Task configuration.
    clean: ['<%= jsBuildDir %>'],
    uglify: {
      options: {
        report: 'gzip',
        sourceMap: true,
        sourceMapIn: '<%= browserify.donation.dest %>.map',
        sourceMapIncludeSources : true
      },
      dist: {
        src: '<%= browserify.donation.dest %>',
        dest: '<%= jsBuildDir %><%= pkgFullName %>.min.js'
      }
    },
    jshint: {
      all: ['<%= jsSrcDir %>**/*.js'],
      options: {
        jshintrc: './.jshintrc'
      }
    },
    browserify: {
      donation: {
        options: {
          browserifyOptions: {
             debug: true
          }
        },
        dest: '<%= jsBuildDir %><%= pkgFullName %>.js',
        src: '<%= jsSrcDir %>donation.js'
      },
      withWatch: {
        options: {
          browserifyOptions: {
             debug: true
          },
          watch: true
        },
        dest: '<%= jsBuildDir %><%= pkgFullName %>.js',
        src: '<%= jsSrcDir %>donation.js'
      }
    },
    exorcise: {
      donation: {
        options: {},
        files: {
          '<%= browserify.donation.dest %>.map': [
            '<%= browserify.donation.dest %>'],
        }
      }
    },
    watch: {
      jshint: {
        files: '<%= jsSrcDir %>**/*.js',
        tasks: ['jshint']
      }
    },
  });

  // These plugins provide necessary tasks.
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-watch');

  grunt.loadNpmTasks('grunt-browserify');
  grunt.loadNpmTasks('grunt-exorcise');

  // Default task.
  grunt.registerTask('default', ['build']);
  grunt.registerTask('build', [
      'jshint',
      'clean',
      'browserify:donation',
      'exorcise',
      'uglify']);
  grunt.registerTask('buildWatch', ['browserify:withWatch', 'watch']);
};
