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
  var $control = $form.find('[aria-controls="' + id + '"] input'),
      $anchorControls = $form.find('a[aria-controls="' + id + '"]');

  $control.change(function(ev) {
    ev.preventDefault();
    $elOn.attr('aria-hidden', !$control.is(':checked'));
    $elOff.attr('aria-hidden', $control.is(':checked'));
  }).change();
  $anchorControls.click(function(ev) {
    var state = $(ev.delegateTarget).data('set-state') || false;
    ev.preventDefault();

    $elOn.attr('aria-hidden', !state);
    $elOff.attr('aria-hidden', state);
  });

};

var submitForm = function($form, $submitButton) {
  var url = $form.data('ajax-url');
  $submitButton.text('Processing').attr('disabled', true);
  $.post(url, $form.serialize())
    .done(function(data) {
      //  Generate a form to submit to pay.gov
      var $payGovForm = $('<form>', {
        'method': 'POST',
        'action': data['oci_servlet_url']
      });
      $.each(data, function(key, value) {
        if (key !== 'oci_servlet_url') {
          $('<input>', {
            'type': 'hidden',
            'name': key,
            'value': value}).appendTo($payGovForm);
        }
      });
      $payGovForm.insertAfter($form).submit();
    })
    .fail(function() {
      //  Fall back to normal HTTP calls. Remove the submit handler to let our
      //  request through
      $form.off('submit');
      $form.submit();
    });
};

var initForm = function($form) {
  var $switchGroup,
      switchGroupIds = [],
      $submitButton = $form.find('.js-submit'),
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

  $form.submit(function(ev) {
    ev.preventDefault();
    submitForm($form, $submitButton);
  });
  $submitButton.text('Continue to Pay.gov');
};

module.exports = {
  initForm: initForm,
  submitForm: submitForm,
  collapsibleToggles: collapsibleToggles
};
