'use strict';

var setup = require('./setup');
setup = setup; // HACK not using module yet.

var $ = require('jquery');
var sinon = require('sinon');
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
  t.test('should set all the filters and selected to first', function(t) {
    var testDiscover,
        $testEls,
        expected,
        expected1 = 'test1',
        expected2 = 'test2';

    $testEls = [
      $('<div>').data('filter-type', expected1),
      $('<div>').data('filter-type', expected2)];

    testDiscover = new Discover($('<div></div>'), $($testEls));
    expected = [expected1, expected2];

    t.deepEquals(testDiscover.filters, expected, 'Filters set to the data of ' +
      'elements passed in');
    t.equal(testDiscover.selected, expected1, 'Sets the selected to the first ' +
      'filter if no option passed in');

    t.end();
  });
  t.test('should set the selected filter', function(t) {
    var testDiscover,
        expected = 'afilterable';

    testDiscover = new Discover($('<div></div>'), $('<a>'), {
      selected: expected
    });

    t.equals(testDiscover.selected, expected, 'Expected is the passed in opt');
    t.end();
  });
  t.end();
});

test('render', function(t) {
  t.test('should hide all the items not matching selected', function(t) {
    var testDiscover,
        testF = 'tester',
        $testEl,
        $testEls;

    $testEls = [
      $('<div>').addClass('js-filteredItem').attr('data-filter-type', 'dud'),
      $('<div>').addClass('js-filteredItem').attr('data-filter-type', testF),
      $('<div>').addClass('js-filteredItem').attr('data-filter-type', 'dud')];
    $testEl = $('<div>');
    $testEl.append($testEls);

    testDiscover = new Discover($testEl, $($testEls), {
      selected: testF
    });

    testDiscover.render();

    t.equal(testDiscover.$('.js-filteredItem').length, 3, 'All elements there');
    t.equal(testDiscover.$('.js-filteredItem:not(.u-hide)').length, 1, 'One is ' +
      'visible');
    t.equal(testDiscover.$('.js-filteredItem.u-hide').length, 2, 'Two are ' +
      'not visible');

    t.end();
  });
  t.end();
});

test('select', function(t) {
  t.test('should select selected to the new filter', function(t) {
    var $testLink,
        testDiscover,
        expected = 'test',
        actual;

    $testLink = $('<div data-filter-type="' + expected + '"]></div>');
    testDiscover = new Discover($('<div>'), $([$testLink]), {
      selected: 'dud'
    });

    testDiscover.select($testLink);
    actual = testDiscover.selected;

    t.equals(actual, expected, 'It sets the selected class to the filter');
    t.end();
  });
  t.test('should call render', function(t) {
    var spy,
        testDiscover;

    testDiscover = new Discover($('<div>'), $('<div>'));
    spy = sinon.spy(testDiscover, 'render');
    testDiscover.select($('<div>'));

    t.ok(spy.calledOnce, 'Render was called once');

    t.end();
  });
  t.end();
});
