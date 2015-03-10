'use strict';

var TOGGLE_CLASS = 'is_active';

var toggle = {
  init: function($el, $onLink, $offLink) {
    $onLink.on('click', function(ev) {
      ev.preventDefault();
      $el.toggleClass(TOGGLE_CLASS, true);
    });
    $offLink.on('click', function(ev) {
      ev.preventDefault();
      $el.toggleClass(TOGGLE_CLASS, false);
    });
  }
};

module.exports = toggle;
