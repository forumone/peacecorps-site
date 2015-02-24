'use strict';

var setup = require('./setup');
setup = setup; // HACK not using module yet.

var $ = require('jquery');
var test = require('tapes');

var Discover = require('../discover');

test('init', function(t) {
  t.test('should populate filterables and controls', function(t) {
    var $root = $('<div />'),
        $control1 = $('<a id="c1" data-controls-filter="aaa"></a>'),
        $element1 = $('<div id="e1" data-in-filter="aaa"></a>'),
        $control2 = $('<a id="c2" data-controls-filter="bbb"></a>'),
        $element2 = $('<div id="e2" data-in-filter="bbb"></a>'),
        discover;
    $root.append($control1, $element2, $control2, $element1);
    discover = new Discover($root);
    t.equals(discover.$filterables[0].id, 'e2');
    t.equals(discover.$filterables[1].id, 'e1');
    t.equals(discover.$controls[0].id, 'c1');
    t.equals(discover.$controls[1].id, 'c2');
    t.end();
  });
  t.test('correctly associates resets', function(t) {
    var $root = $('<div />'),
        $c1 = $('<a data-controls-filter="c1"></a>').appendTo($root),
        $c2 = $('<a data-controls-filter="c2"></a>').appendTo($root),
        $c3 = $('<a data-filter-reset="true" data-controls-filter="c3"></a>'
                ).appendTo($root),
        $c4 = $('<a data-controls-filter="c4"></a>').appendTo($root);
    new Discover($root);
    $c1.click();
    t.equals($c1.attr('aria-selected'), 'true');
    t.equals($c2.attr('aria-selected'), 'false');
    t.equals($c3.attr('aria-selected'), 'false');
    t.equals($c4.attr('aria-selected'), 'false');
    $c2.click();
    t.equals($c1.attr('aria-selected'), 'true');
    t.equals($c2.attr('aria-selected'), 'true');
    t.equals($c3.attr('aria-selected'), 'false');
    t.equals($c4.attr('aria-selected'), 'false');
    $c3.click();
    t.equals($c1.attr('aria-selected'), 'false');
    t.equals($c2.attr('aria-selected'), 'false');
    t.equals($c3.attr('aria-selected'), 'true');
    t.equals($c4.attr('aria-selected'), 'false');
    $c4.click();
    t.equals($c1.attr('aria-selected'), 'false');
    t.equals($c2.attr('aria-selected'), 'false');
    t.equals($c3.attr('aria-selected'), 'true');
    t.equals($c4.attr('aria-selected'), 'true');
    t.end();
  });
  t.end();
});

test('state', function(t) {
  t.test('should filter and unfilter', function(t) {
    var $root = $('<div />'),
        $e1 = $('<div data-in-filter="c1"></div>').appendTo($root),
        $e2 = $('<div data-in-filter="c2"></div>').appendTo($root),
        discover = new Discover($root);

    discover.select('c1');
    t.equals($e1.attr('aria-hidden'), 'false');
    t.equals($e2.attr('aria-hidden'), 'true');
    discover.select('c2');
    t.equals($e1.attr('aria-hidden'), 'true');
    t.equals($e2.attr('aria-hidden'), 'false');
    discover.select('c3');
    t.equals($e1.attr('aria-hidden'), 'true');
    t.equals($e2.attr('aria-hidden'), 'true');
    discover.back();
    t.equals($e1.attr('aria-hidden'), 'true');
    t.equals($e2.attr('aria-hidden'), 'false');
    discover.back();
    t.equals($e1.attr('aria-hidden'), 'false');
    t.equals($e2.attr('aria-hidden'), 'true');
    t.end();
  });
  t.end();
});
