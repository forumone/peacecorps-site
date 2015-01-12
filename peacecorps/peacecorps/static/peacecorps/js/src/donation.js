'use strict';

var $ = require('jquery');

var Collapsible = require('./collapsible');
var Discover = require('./discover');
var UpdatePercent = require('./update_donatepercent');
var Landing = require('./landing');
var form = require('./form');
var jsusers = require('./jsusers');

//  Note that we set up an event listener and call it immediately to check the
//  initial state
//  TODO move Init to own module
var Init = {
  //  State/Zip are only marked "required" if country == USA
  countryRequirements: function() {
    var country = $('#id_country'),
        countryReqLabels = $('label[for=id_billing_state], ' +
            'label[for=id_billing_zip]');

    country.change(function() {
      countryReqLabels.toggleClass('required', country.val() === 'USA');
    }).change();
  },

  //  In-memory donations have a separate field + wording
  inMemoryChanges: function() {
    var honoreeSwap = $('.honoree_swap');

    $('input[name=dedication_type]').change(function() {
      //  "this" refers to the *selected* radio button
      var inMemory = (
        $('input[name=dedication_type]:checked').val() === 'in-memory');

      $('#dedication_contact_wrapper').toggle(inMemory);
      honoreeSwap.each(function(idx, el) {
        var $el = $(el);
        if (inMemory) {
          $el.html($el.html().replace('honoree', 'family'));
        } else {
          $el.html($el.html().replace('family', 'honoree'));
        }
      });
    }).change();
  }
};

$().ready(function() {
  var $discoverApp = $('.js-discoverApp'),
      $form = $('.js-form');

  // TODO I want to rebuild the Init class to remove this check at some point.
  if ($('.landing').length < 1) {
    Init.countryRequirements();
    Init.inMemoryChanges();
  }

  Landing.createExpanders();
  Landing.createDataFilter();

  new UpdatePercent($('.js-fundingBar'));

  if ($discoverApp.length > 0) {
    var discover = new Discover($discoverApp, $('.js-discoverNav a'), {
      selected: window.location.hash.substr(1)
    });
    discover.render();
  }
  $('.js-collapsibleItem').each(function() {
    var collapsible,
        id = $(this).attr('id'),
        $control = $('[aria-controls="'+ id +'"]');

    collapsible = new Collapsible($(this), $control, {
      hideControls: !($(this).hasClass('js-collapsibleNoHide')),
      startOpen: id === window.location.hash.substr(1)
    });
    collapsible.render();
  });

  if ($form) {
    form.initForm($form);
  }

  jsusers.showHideForJSUsers();
});
