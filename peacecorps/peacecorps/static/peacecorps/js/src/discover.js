'use strict';

var $ = require('jquery');
var _ = require('underscore');

var Discover = function($root) {
  var self = this;
  // TODO move this all into shared code.
  if ($root.length < 1) {
    throw new Error('selector missing');
  }
  this.$el = $root;
  this.state = [];
  this.currentProject = false;
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
  
  window.onpopstate = function (event) {
    console.log('window.onpopstate', event);
  };
  
  // Parse that hash
  var config = this.parseHash();
  
  console.log('config', config);
  
  if ( config.section ) {
    this.state = [ config.section ];
  }
  if ( config.params['subSection'] ) {
    this.state.push( config.params['subSection'] );
  }
  if ( config.params['project'] ) {
    this.currentProject = config.params['project'];
  }
  console.log('  this.state', this.state);
  console.log('  _.last(this.state)', _.last(this.state));
  console.log('  this.currentProject', this.currentProject);
  this._filter( _.last(this.state) );
  this.highlightSelected();
  if ( this.currentProject ) {
    this.selectProject(this.currentProject);
  }
};

Discover.prototype.parseHash = function() {
  
  var hash, hashParts = [], section = '', rawParams= [], keyValue = [], params = {};
  
  hash = window.location.hash.substr(1);
  hashParts = hash.split('?');
  section = hashParts.shift();
  rawParams = hashParts.pop().split('&');
  for (var i = 0; i < rawParams.length; i++) {
    keyValue = rawParams[i].split('=');
    params[keyValue.shift()] = keyValue.shift();
  }
  
  return {section: section, params: params};
};

/* Store filter state in the URI's hash */
Discover.prototype.updateHash = function() {
  var appState = this.state.slice(),
      hash = '',
      params = [],
      section = false,
      subSection = false,
      project = false;
  
      console.log('updateHash', appState);
  
  section = appState.shift() || 'issue';
  subSection = appState.shift() || false;
  project = this.currentProject || false;
  
  if ( section ) {
    hash += section;
  }
  if ( subSection ) {
    params.push('subSection=' + subSection);
  }
  if ( project ) {
    params.push('project=' + project);
  }
  if ( params.length > 0) {
    hash += '?' + params.join('&');
  }
  
  window.location.hash = hash;
};

/* Select a filter. Reset will reset the filter history */
Discover.prototype.select = function(filter, reset) {
  
  console.log('select:'  + filter);
  
  if (reset) {
    this.state = [filter];
  } else {
    this.state.push(filter);
  }
  this.currentProject = false;
  this._filter(filter);
  this.highlightSelected();
  this.updateHash();
};

/* Go back in the trail of selected filters */
Discover.prototype.back = function() {
  this.state.pop();
  this._filter(this.state[this.state.length - 1]);
  this.highlightSelected();
  this.currentProject = false;
  this.updateHash();
};

/* Go back in the trail of selected filters */
Discover.prototype.selectProject = function(itemId) {
  this.currentProject = itemId;
  this.updateHash();
};

Discover.prototype.deselectProject = function() {
  this.currentProject = false;
  this.updateHash();
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
  console.log('_filter', escaped, regex);
  this.$filterables.each(function() {
    var $this = $(this);
    $this.attr('aria-hidden', !regex.test($this.attr('data-in-filter')));
  });
};

module.exports = Discover;

