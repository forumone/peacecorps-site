'use strict';

var setup = require('./setup');
setup = setup; // HACK not using module yet.

var $ = require('jquery');
var test = require('tapes');

var Discover = require('../discover');

test('init', function(t) {
  t.test('should set $navLinks attr to navLinks passed in', function(t) {
    var testDiscover,
        expected;

    expected = $('<a></a>');
    testDiscover = new Discover($('<div></div>'), expected);

    t.equals(testDiscover.$navLinks, expected, 'The navLinks are whats passed ' +
        'in');

    t.end();
  });
  t.end();
});
