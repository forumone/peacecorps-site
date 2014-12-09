'use strict';

var setup = require('./setup');
setup = setup; // HACK not using module yet.

var $ = require('jquery');
var sinon = require('sinon');
var test = require('tapes');

var Collapsible = require('../collapsible');

test('init', function(t) {
  t.test('should set the id to the id of the element', function(t) {
    var $testEl,
        actual,
        expected = 'test-1',
        testCollapsible;

    $testEl = $('<div id="'+ expected +'"></div>');
    testCollapsible = new Collapsible($testEl);

    actual = testCollapsible.id;

    t.equals(actual, expected, 'The id attribute is set to the html id');

    t.end();
  });
  t.test('should set the id to blank string if not there', function(t) {
    var $testEl,
        actual,
        testCollapsible;

    $testEl = $('<div></div>');
    testCollapsible = new Collapsible($testEl);

    actual = testCollapsible.id;

    t.equals(actual, '', 'The id attribute is set to blank string');

    t.end();
  });
  t.test('should set the $controls to the one passed in', function(t) {
    var $testEl,
        $expected,
        $actual,
        testCollapsible;

    $expected = $('<a aria-controls="test"></a>');
    $testEl = $('<div id="test"></div>');
    testCollapsible = new Collapsible($testEl, $expected);

    $actual = testCollapsible.$control;

    t.equals($actual[0], $expected[0], 'The $controls set to its link');

    t.end();
  });
  t.test('should bind click even to $control', function(t) {
    var $testEl,
        mock,
        testCollapsible;

    mock = sinon.mock($.prototype);
    $testEl = $('<div id="test"></div>');
    mock.expects('on').once();
    testCollapsible = new Collapsible($testEl, mock.object);

    t.ok(mock.verify());

    t.end();
  });
  t.end();
});

test('render', function(t) {
  //t.test('should hide all other collapsible elements', function(t) {

  //  t.end();
  //});
  t.test('should hide the element', function(t) {
    var $testEl,
        actual,
        testCollapsible;

    $testEl = $('<div class="callapseMe"></div>');
    testCollapsible = new Collapsible($testEl);
    testCollapsible.render();

    actual = testCollapsible.$el.attr('aria-hidden');

    t.equals(actual, 'true', 'Element has the hidden class');

    t.end();
  });
  t.end();
});
