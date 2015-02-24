'use strict';

var $ = require('jquery');

var Discover = function($root) {
  var self = this;
  // TODO move this all into shared code.
  if ($root.length < 1) {
    throw new Error('selector missing');
  }
  this.$el = $root;
  this.state = [];
  // create shortcut to finding things within root.
  this.$ =  function(selector) {
    return this.$el.find(selector);
  };
  this.$filterables = this.$('[data-in-filter]');
  this.$controls = this.$('[data-controls-filter]');

  this.$controls.click(function(ev) {
    var $this = $(this),
        filter = $this.attr('data-controls-filter');
    ev.preventDefault();
    self.select(filter, $this.data('filter-reset'));
  });
  this.$('.js-pageBack').click(function(ev) {
    ev.preventDefault();
    self.back();
  });
};

/* Select a filter. Reset will reset the filter history */
Discover.prototype.select = function(filter, reset) {
  if (reset) {
    this.state = [filter];
  } else {
    this.state.push(filter);
  }
  this._filter(filter);
  this.highlightSelected();
};

/* Go back in the trail of selected filters */
Discover.prototype.back = function() {
  this.state.pop();
  this._filter(this.state[this.state.length - 1]);
  this.highlightSelected();
};

/* Highlight the trail of filters */
Discover.prototype.highlightSelected = function() {
  this.$controls.attr('aria-selected', false);
  for (var i = 0; i < this.state.length; i++) {
    this.$controls.filter('[data-controls-filter=' + this.state[i] + ']').attr(
        'aria-selected', true);
  }
};

/**
 * Internal method; hides all filterable items unless their data-in-filter
 * includes the filterName
 **/
Discover.prototype._filter = function(filterName) {
  var escaped = filterName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'),
      regex = new RegExp('(,|^)' + escaped + '(,|$)');
  this.$filterables.each(function() {
    var $this = $(this);
    $this.attr('aria-hidden', !regex.test($this.attr('data-in-filter')));
  });
};

module.exports = Discover;

