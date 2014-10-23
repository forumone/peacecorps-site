'use strict';

$(document).ready(function() {
  var $expands = $('.project-row .project-expanded');
  $('.project-row').click(function() {
    var $expand = $(this).find('.project-expanded');
    $expands.not($expand).slideUp();
    $expand.slideToggle();
  });
});
