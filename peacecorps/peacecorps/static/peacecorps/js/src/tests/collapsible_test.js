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
  t.test('should set the hideControls to option passed in', function(t) {
    var $testEl,
        actual,
        testCollapsible;

    $testEl = $('<div></div>');
    testCollapsible = new Collapsible($testEl, $('<div>'), {
      hideControls: true
    });

    actual = testCollapsible.hideControls;

    t.equals(actual, true, 'Sets the hideControls attr to true');

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
  t.test('should hide the element unless told not to', function(t) {
    var $testEl,
        actual,
        testCollapsible;

    $testEl = $('<div class="callapseMe"></div>');

    testCollapsible = new Collapsible($testEl);
    testCollapsible.render();
    actual = testCollapsible.$el.attr('aria-hidden');
    t.equals(actual, 'true', 'Element has the hidden class');

    testCollapsible = new Collapsible($testEl, null, {startOpen: false});
    testCollapsible.render();
    actual = testCollapsible.$el.attr('aria-hidden');
    t.equals(actual, 'true', 'Element has the hidden class');

    testCollapsible = new Collapsible($testEl, null, {startOpen: true});
    testCollapsible.render();
    actual = testCollapsible.$el.attr('aria-hidden');
    t.equals(actual, 'false', 'Element does not have the hidden class');

    t.end();
  });
  t.test('should hide controls if option set', function(t) {
    var $testEl,
        actual,
        testCollapsible;

    $testEl = $('<div></div>');
    testCollapsible = new Collapsible($('<div></div>'), $testEl, {
      startOpen: true,
      hideControls: true
    });
    testCollapsible.render();

    actual = testCollapsible.$control.attr('aria-hidden');

    t.equals(actual, 'true', 'Element is hidden');

    t.end();
  });
  t.end();
});
