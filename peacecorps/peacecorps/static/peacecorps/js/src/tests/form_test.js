'use strict';

var setup = require('./setup');
setup = setup; // HACK not using module yet.

var $ = require('jquery');
var test = require('tapes');

var form = require('../form');

test('initForm', function(t) {
  t.test('should exist', function(t) {
    t.ok(form.initForm, 'Function exists');
    t.end();
  });
  t.end();
});

test('switchToggle', function(t) {
  t.test('allows anchors to set state', function(t) {
    var $form = $('<form />'),
        $el1 = $('<span data-switch-id="anId" data-switch-on="true" />'),
        $el2 = $('<span data-switch-id="anId" data-switch-on="false" />'),
        $a = $('<a aria-controls="anId">click</a>');
    $el1.addClass('js-formSwitch');
    $el2.addClass('js-formSwitch');
    $form.append($el1, $el2, $a);
    form.initForm($form);

    $a.click();
    t.equals($el1.attr('aria-hidden'), 'true', 'By default, elOn get hidden');
    t.equals($el2.attr('aria-hidden'), 'false', 'By default, elOff get shown');

    $a.data('set-state', false);
    $a.click();
    t.equals($el1.attr('aria-hidden'), 'true', 'false -> elOn get hidden');
    t.equals($el2.attr('aria-hidden'), 'false', 'false -> elOff get shown');

    $a.data('set-state', true);
    $a.click();
    t.equals($el1.attr('aria-hidden'), 'false', 'true -> elOn get shown');
    t.equals($el2.attr('aria-hidden'), 'true', 'true -> elOff get hidden');

    t.end();
  });
  t.end();
});
