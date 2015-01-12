/*
 * To accommodate non-JS users, certain elements are only shown (or are only
 * hidden) if JS is present.
 */
'use strict';

var progEnhcJSUsers = function($root) {
  $root.find('.js-showForJSUsers').attr('aria-hidden', false);
  $root.find('.js-hideForJSUsers').attr('aria-hidden', true);
};

module.exports = {
  progEnhcJSUsers: progEnhcJSUsers
};
