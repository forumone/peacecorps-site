/*
 * Functionality related to forms
 */
'use strict';

var $ = require('jquery');

var ccCollapsibleToggle = '.js-collapsibleToggle';

var collapsibleToggles = function($el, $form) {
  var id = $(this).attr('id'),
      $control = $form.find('[aria-controls="'+ id +'"] input');

  $control.change(function(ev) {
    ev.preventDefault();
    $el.attr('aria-hidden', !$control.is(':checked'));
  }).change();
};

var initForm = function($form) {
  $form.find(ccCollapsibleToggle).each(function() {
    collapsibleToggles($(this), $form);
  });
};

module.exports = {
  initForm: initForm,
  collapsibleToggles: collapsibleToggles
};
