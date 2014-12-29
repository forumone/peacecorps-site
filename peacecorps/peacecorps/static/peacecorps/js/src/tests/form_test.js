'use strict';

var setup = require('./setup');
setup = setup; // HACK not using module yet.

var test = require('tapes');

var form = require('../form');

test('initForm', function(t) {
  t.test('should exist', function(t) {
    t.ok(form.initForm, 'Function exists');
    t.end();
  });
  t.end();
});
