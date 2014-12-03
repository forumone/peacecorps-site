'use strict';

var $ = require('jquery');

var UpdatePercent = require('./update_donatepercent');
var Landing = require('./landing');

//  Note that we set up an event listener and call it immediately to check the
//  initial state
var Init = {
  //  Individual and Organization have different fields
  donorTypeFields: function() {
    var orgFields = $('.shown-with-organization'),
        indFields = $('.shown-with-individual');
    $('input[name=donor_type]').change(function() {
      var isOrg = $('input[name=donor_type]:checked').val() === 'Organization';

      orgFields.toggle(isOrg);
      indFields.toggle(!isOrg);
    }).change();
  },

  //  State/Zip are only marked "required" if country == USA
  countryRequirements: function() {
    var country = $('#id_country'),
        countryReqLabels = $('label[for=id_billing_state], label[for=id_billing_zip]');

    country.change(function() {
      countryReqLabels.toggleClass('required', country.val() === 'USA');
    }).change();
  },

  //  Donations in dedication to someone have additional fields
  dedicationFields: function() {
    var dedication = $('#id_dedication'),
        dedicationDiv = $('.dedication_details');

    dedication.change(function() {
      dedicationDiv.toggle(dedication.is(':checked'));
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
  Init.donorTypeFields();
  Init.countryRequirements();
  Init.dedicationFields();
  Init.inMemoryChanges();

  Landing.createExpanders();
  Landing.createDataFilter();

  var updatePercent = new UpdatePercent($('.js-fundingBar'));
  updatePercent.init();
});
