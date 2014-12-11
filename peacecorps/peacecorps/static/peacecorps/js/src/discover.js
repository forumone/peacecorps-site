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
  this.ccFilteredItem = '.js-filterable';
  this.init.apply(this, arguments);
};

Discover.ccFilteredItem = '.js-filterable';

Discover.prototype.init = function(root, $navLinks, opts) {
  var self = this,
      lopts = opts || {};

  this.$navLinks = $navLinks;
  this.filters = [];
  $navLinks.each(function() {
    self.filters.push($(this).data('filter-type'));
    $(this).on('click', function() {
      self.select($(this));
    });
  });
  this.selected = lopts.selected || this.filters[0];
};

Discover.prototype.render = function() {
  var $filtereds = this.$(
    this.ccFilteredItem + this.dataSelector('filter-type', this.selected));
  this.$(this.ccFilteredItem)
      .attr('aria-hidden', true)
      .toggleClass('u-hide', true);

  $filtereds.each(function() {
    $(this)
        .attr('aria-hidden', false)
        .toggleClass('u-hide', false);
  });
};

Discover.prototype.select = function($link) {
  var filter = $link.attr('data-filter-type');
  this.selected = filter;
  this.render();
};

Discover.prototype.dataSelector = function(dataAttr, dataVal) {
  return '[data-'+ dataAttr + '="' + dataVal + '"]';
};


module.exports = Discover;

