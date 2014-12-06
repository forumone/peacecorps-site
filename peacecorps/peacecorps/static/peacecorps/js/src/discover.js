'use strict';

var $ = require('jquery');

var Discover = function($root) {
  // TODO move this all into shared code.
  if ($root.length < 1) {
    throw new Error('selector missing');
  }
  this.el = $root[0];
  this.$el = $root;
  // create shortcut to finding things within root.
  this.$ =  function(selector) {
    return this.$el.find(selector);
  };
  this.ccFilteredItem = '.js-filteredItem';
  this.init.apply(this, arguments);
};

Discover.prototype.init = function(root, $navLinks, opts) {
  var self = this,
      lopts = opts || {};

  this.$navLinks = $navLinks;
  this.filters = [];
  $navLinks.each(function() {
    self.filters.push($(this).data('filter-type'));
  });
  this.selected = lopts.selected || this.filters[0];
};

Discover.prototype.render = function() {
  console.log(this.selected);
  console.log(this.dataSelector('filter-type', this.selected));
  var $filtereds = this.$(
    this.ccFilteredItem + this.dataSelector('filter-type', this.selected));
  this.$(this.ccFilteredItem).hide()
      .toggleClass('u-hide', true);

  $filtereds.each(function() {
    $(this).show()
        .toggleClass('u-hide', false);
  });
};

Discover.prototype.dataSelector = function(dataAttr, dataVal) {
  return '[data-'+ dataAttr + '="' + dataVal + '"]';
};


module.exports = Discover;

