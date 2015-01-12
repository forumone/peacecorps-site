/*
 * Show parts of a page which would otherwise be hidden if JS is present
 */
'use strict';

var $ = require('jquery');

var showHideForJSUsers = function() {
  $('.js-showForJSUsers').attr('aria-hidden', false);
  $('.js-hideForJSUsers').attr('aria-hidden', true);
};

module.exports = {
  showHideForJSUsers: showHideForJSUsers
};
