'use strict';

var setup = require('./setup');
setup = setup; // HACK not using module yet.

var $ = require('jquery');
var sinon = require('sinon');
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

test('submitForm', function(t) {
  t.test('calls ajax with serialized data', function(t) {
    var $form = $('<form data-ajax-url="some-url">' +
                  '<input type="hidden" name="some" value="value" />' +
                  '<input type="text" name="other" value="example" />' +
                  '</form>'),
        $submit = $('<button />'),
        server = sinon.fakeServer.create(),
        request;
    form.submitForm($form, $submit);
    request = server.requests[0];
    t.equal(request.method, 'POST', 'sends POST');
    t.equal(request.requestBody, 'some=value&other=example',
            'contains proper body');
    t.equal($submit.text(), 'Processing', 'submit text changed');
    t.equal($submit.attr('disabled'), 'disabled', 'submit becomes disabled');
    t.end();
  });
  t.test('submits to paygov on success', function(t) {
    var $form = $('<form data-ajax-url="some-url"></form>'),
        $submit = $('<button />'),
        server = sinon.fakeServer.create(),
        $div = $('<div />').append($form),
        submitted = false,
        request,
        $secondForm;
    form.submitForm($form, $submit);
    $div.on('submit', 'form', function(ev) {
      ev.preventDefault();
      submitted = true;
    });

    request = server.requests[0];
    request.respond(200, {'Content-Type': 'application/json'},
                    JSON.stringify({'oci_servlet_url': 'some-url',
                                    'another': 'some-val'}));
    t.equal(submitted, true, 'paygov form was submitted');
    t.equal($div.find('form').length, 2, 'second form was added');
    $secondForm = $div.find('form:last');
    t.equal($secondForm.attr('action'), 'some-url', 'paygov url is used');
    t.equal($secondForm.attr('method'), 'POST', 'form is posted');
    t.equal($secondForm.find('input[name=another]').attr('type'), 'hidden',
            'form fields are hidden');
    t.equal($secondForm.find('input[name=another]').val(), 'some-val',
            'form fields are present');
    t.end();
  });
  t.end();
});
