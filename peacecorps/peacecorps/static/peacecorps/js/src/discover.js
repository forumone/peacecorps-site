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

Discover.prototype.init = function(root, $navLinks) {
  var self = this,
      $selectedLink;

  this.$navLinks = $navLinks;
  this.filters = [];
  $navLinks.each(function() {
    self.filters.push($(this).data('filter-type'));
    $(this).on('click', function() {
      self.select($(this));
    });
  });
  $selectedLink = $(this.$navLinks[0]);
  this.selected = this.filters[0];
  this.select($selectedLink);
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

Discover.prototype.getOtherLinks = function($currentLink) {
  // TODO hacky, should use event binding
  return $currentLink.parent().siblings().find('a');
};

Discover.prototype.select = function($link) {
  var filter = $link.attr('data-filter-type') || $link.data('filter-type'),
      $otherLinks;

  this.selected = filter;
  this.render();
  $otherLinks = this.getOtherLinks($link);
  $otherLinks.attr('aria-selected', false);
  $link.attr('aria-selected', true);
};

Discover.prototype.dataSelector = function(dataAttr, dataVal) {
  return '[data-'+ dataAttr + '="' + dataVal + '"]';
};


module.exports = Discover;

