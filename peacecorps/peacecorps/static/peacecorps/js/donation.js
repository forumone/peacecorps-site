'use strict';

//  Namespace
var Init = {
  //  State/Zip are only marked "required" if country == USA
  countryRequirements: function() {
    var country = $('#id_country'),
        countryReqLabels = $('label[for=id_state], label[for=id_zip_code]');

    country.change(function() {
      countryReqLabels.toggleClass('required', country.val() === 'USA');
    });
  },

  //  Donations in dedication to someone have additional fields
  dedicationFields: function() {
    var dedication = $('#id_dedication'),
        dedicationDiv = $('#dedication_details');

    dedication.change(function() {
      dedicationDiv.toggle(dedication.is(':checked'));
    });
  },

  //  In-memory donations have a separate field + wording
  inMemoryChanges: function() {
    var selectors = $('input[name=dedication_type'),
        honoreeSwap = $('.honoree_swap');

    $('input[name=dedication_type]').change(function() {
      //  "this" refers to the *selected* radio button
      var inMemory = $(this).val() === 'in-memory';

      $('#dedication_contact_wrapper').toggle(inMemory);
      honoreeSwap.each(function(idx, el) {
        var $el = $(el);
        if (inMemory) {
          $el.html($el.html().replace('honoree', 'family'));
        } else {
          $el.html($el.html().replace('family', 'honoree'));
        }
      });
    });
  }
};

$(document).ready(function() {
  Init.countryRequirements();
  Init.dedicationFields();
  Init.inMemoryChanges();
});
