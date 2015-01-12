'use strict';

var setup = require('./setup');
setup = setup; // HACK not using module yet.

var $ = require('jquery');
var test = require('tapes');

var jsusers = require('../jsusers');

test('progEnhcJSUsers', function(t) {
  var $root = $('<div />'),
      $showPlain = $('<span class="js-showForJSUsers" />'),
      $showTrue = $('<span class="js-showForJSUsers" aria-hidden="true" />'),
      $showFalse = $('<span class="js-showForJSUsers" aria-hidden="false" />'),
      $hidePlain = $('<span class="js-hideForJSUsers" />'),
      $hideTrue = $('<span class="js-hideForJSUsers" aria-hidden="true" />'),
      $hideFalse = $('<span class="js-hideForJSUsers" aria-hidden="false" />');
  $root.append($showPlain, $hidePlain, $showTrue, $hideTrue, $showFalse,
               $hideFalse);
  jsusers.progEnhcJSUsers($root);
  
  t.equals($showPlain.attr('aria-hidden'), 'false');
  t.equals($showTrue.attr('aria-hidden'), 'false');
  t.equals($showFalse.attr('aria-hidden'), 'false');

  t.equals($hidePlain.attr('aria-hidden'), 'true');
  t.equals($hideTrue.attr('aria-hidden'), 'true');
  t.equals($hideFalse.attr('aria-hidden'), 'true');

  t.end();
});
