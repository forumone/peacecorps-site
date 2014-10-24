'use strict';

//  Namespace
var Init = {
  //  Each project can be clicked to reveal/hide extra project information
  createExpanders: function() {
    var $expands = $('.project-row .project-expanded');
    $('.project-row').click(function() {
      var $expand = $(this).find('.project-expanded');
      $expands.not($expand).slideUp();
      $expand.slideToggle();
    });
  },

  //  Initialize all data needed for the filter box; returns a mapping between
  //  PCPP id and the words contained in its description, title, etc.
  initFilterData: function() {
    //  Helpful functions
    var wordMapping = [],   // PCPP id to word array
        stopWords = ['A', 'AN', 'THE', 'AND', 'FOR', 'OF', 'IN'],
        wordRe = /\b(\w+)\b/g,
        toUpper = function(string) { return string.toUpperCase(); },
        parse = function(string) {
          var words = string.match(wordRe),
              upper = _.map(words, toUpper),
              withoutStopwords = _.difference(upper, stopWords);
          return withoutStopwords;
        };
    //  Convert projects into words, give them a unique id (wordIdx)
    $('.project-row').each(function() {
      var $this = $(this),
          title = parse($this.find('.project-name').text()),
          country = $this.find('.project-country').text().toUpperCase(), 
          volunteer = parse($this.find('.volunteer').text()),
          desc = parse($this.find('.short-desc').text()),
          words = _.union(title, [country], volunteer, desc);
      $this.data('wordIdx', wordMapping.length);
      wordMapping.push(_.uniq(words));
    });
    return wordMapping;
  },

  //  Creates the search box for filtering PCPP data
  createDataFilter: function() {
    var wordMapping = Init.initFilterData(),
        searchBox = $('.search-space input');
    $('.search-space').show();
    searchBox.keyup(function() {
      var query = searchBox.val().toUpperCase(),
          queryMatch = function(word) {
            return word.substring(0, query.length) === query;
          };
      if (query === '') {
        //  Show everything
        $('.project-row').show();
      } else {
        $('.project-row').each(function() {
          var $this = $(this),
              words = wordMapping[$this.data('wordIdx')];
          $this.toggle(_.some(words, queryMatch));
        });
      }
    });
  }
};

$(document).ready(function() {
  Init.createExpanders();
  Init.createDataFilter();
});
