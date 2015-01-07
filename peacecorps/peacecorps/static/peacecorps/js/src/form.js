/*
 * Functionality related to forms
 */
'use strict';

var $ = require('jquery');

var ccCollapsibleToggle = '.js-collapsibleToggle';
var ccSwitchToggle = '.js-formSwitch';

var collapsibleToggles = function($el, $form) {
  var id = $el.attr('id'),
      $control = $form.find('[aria-controls="'+ id +'"] input');

  $control.change(function(ev) {
    ev.preventDefault();
    $el.attr('aria-hidden', !$control.is(':checked'));
  }).change();
};

var switchToggle = function($elOn, $elOff, id, $form) {
  var $control = $form.find('[aria-controls="' + id + '"] input');

  $control.change(function(ev) {
    ev.preventDefault();
    $elOn.attr('aria-hidden', !$control.is(':checked'));
    $elOff.attr('aria-hidden', $control.is(':checked'));
  }).change();
};

var initForm = function($form) {
  var $switchGroup,
      switchGroupIds = [],
      i,
      ilen;

  $form.find(ccCollapsibleToggle).each(function() {
    collapsibleToggles($(this), $form);
  });

  $form.find(ccSwitchToggle).each(function() {
    var id = $(this).attr('data-switch-id');
    switchGroupIds.push(id);
  });
  $.unique(switchGroupIds);

  for (i = 0, ilen = switchGroupIds.length; i < ilen; i++) {
    $switchGroup = $form.find(ccSwitchToggle + '[data-switch-id="' +
        switchGroupIds[i] + '"]');

    switchToggle(
        $($switchGroup.filter(function() {
          return $(this).attr('data-switch-on') === 'true'; })),
        $($switchGroup.filter(function() {
          return $(this).attr('data-switch-on') === 'false'; })),
        switchGroupIds[i],
        $form);
  }

  $form.find('button[type="submit"]').text('Continue to Pay.gov');
};

module.exports = {
  initForm: initForm,
  collapsibleToggles: collapsibleToggles
};
