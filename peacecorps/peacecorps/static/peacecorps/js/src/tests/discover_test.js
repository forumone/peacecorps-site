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

    sinon.stub(Discover.prototype, 'getOtherLinks').returns($('<a></a><a></a>'));
    expected = $('<a></a>');
    testDiscover = new Discover($('<div></div>'), expected);

    t.equals(testDiscover.$navLinks, expected, 'The navLinks are whats passed ' +
        'in');

    Discover.prototype.getOtherLinks.restore();
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
      'filter');

    t.end();
  });
  t.test('should set aria-selected to true on first link', function(t) {
    var testDiscover,
        $testNavs;

    $testNavs = [
      $('<a id="nav1"></a>'),
      $('<a id="nav2"></a>')];
    sinon.stub(Discover.prototype, 'getOtherLinks').returns($('<a></a><a></a>'));
    testDiscover = new Discover($('<div></div>'), $($testNavs));

    t.equals($testNavs[0].attr('aria-selected'), 'true', 'Sets the aria ' +
      'selected attribute of selected link to true');

    Discover.prototype.getOtherLinks.restore();
    t.end();
  });
  t.end();
});

test('render', function(t) {
  t.test('should hide all the items not matching selected', function(t) {
    var testDiscover,
        testF = 'tester',
        ccfilterable = Discover.ccFilteredItem.replace('.', ''),
        $testEl,
        $testEls;

    $testEls = [
      $('<div>').addClass(ccfilterable).attr('data-filter-type',
        testF),
      $('<div>').addClass(ccfilterable).attr('data-filter-type',
        'dud'),
      $('<div>').addClass(ccfilterable).attr('data-filter-type',
        'dud')];
    $testEl = $('<div>');
    $testEl.append($testEls);
    sinon.stub(Discover.prototype, 'getOtherLinks').returns($('<a></a><a></a>'));

    testDiscover = new Discover($testEl, $($testEls));

    testDiscover.render();

    t.equal(testDiscover.$(Discover.ccFilteredItem).length, 3,
        'All elements there');
    t.equal(testDiscover.$(Discover.ccFilteredItem + ':not(.u-hide)').length, 1,
        'One is visible');
    t.equal(testDiscover.$(Discover.ccFilteredItem + '.u-hide').length, 2,
        'Two are not visible');

    Discover.prototype.getOtherLinks.restore();
    t.end();
  });
  t.end();
});
