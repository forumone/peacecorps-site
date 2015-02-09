/**
 * Content that should only be shown once per user. A flag is set in
 * localstorage, and, if present, the content is hidden.
 **/
'use strict';

var $ = require('jquery');

var showOnce = function($root, storage) {
  $root.find('[data-show-once]').each(function() {
    var $el = $(this),
        key = 'show-once:' + $el.attr('data-show-once'),
        seen = !!(storage && storage.getItem(key));
    $el.attr('aria-hidden', seen);
    if (!seen && storage) {
      storage.setItem(key, true);
    }
  });
};

module.exports = {
  showOnce: showOnce
};
