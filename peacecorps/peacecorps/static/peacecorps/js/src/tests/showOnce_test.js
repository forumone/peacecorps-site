'use strict';

var setup = require('./setup');
setup = setup; // HACK not using module yet.

var $ = require('jquery');
var test = require('tapes');

var showOnce = require('../showOnce');

test('showOnce', function(t) {
  var mockStorage = function() {
    var db = {};
    return {
      getItem: function(key) { return db[key] || null; },
      setItem: function(key, value) { db[key] = value; }
    };
  };
  t.test('should default if no localstorage is present', function(t) {
    var $root = $('<div />'),
        $el1 = $('<span data-show-once="firstId" />'),
        $el2 = $('<span data-show-once="secondId" />');
    $root.append($el1, $el2);
    showOnce.showOnce($root, false);
    console.log($el1);
    t.equals($el1.attr('aria-hidden'), 'false');
    t.equals($el2.attr('aria-hidden'), 'false');
    t.end();
  });
  t.test('should be shown if keys not present', function(t) {
    var $root = $('<div />'),
        $el1 = $('<span data-show-once="firstId" />'),
        $el2 = $('<span data-show-once="secondId" />'),
        storage = mockStorage();
    $root.append($el1, $el2);
    showOnce.showOnce($root, storage);
    console.log($el1);
    t.equals($el1.attr('aria-hidden'), 'false');
    t.equals($el2.attr('aria-hidden'), 'false');
    t.equals(storage.getItem('show-once:firstId'), true);
    t.equals(storage.getItem('show-once:secondId'), true);
    t.end();
  });
  t.test('should not be shown if key is present', function(t) {
    var $root = $('<div />'),
        $el1 = $('<span data-show-once="firstId" />'),
        $el2 = $('<span data-show-once="secondId" />'),
        storage = mockStorage();
    storage.setItem('show-once:secondId', true);
    $root.append($el1, $el2);
    showOnce.showOnce($root, storage);
    console.log($el1);
    t.equals($el1.attr('aria-hidden'), 'false');
    t.equals($el2.attr('aria-hidden'), 'true');
    t.equals(storage.getItem('show-once:firstId'), true);
    t.equals(storage.getItem('show-once:secondId'), true);
    t.end();
  });
  t.end();
});

