'use strict';

var $ = require('jquery');

var Collapsible = require('./collapsible');
var Discover = require('./discover');
var UpdatePercent = require('./update_donatepercent');
var Landing = require('./landing');
var form = require('./form');
var jsusers = require('./jsusers');
var showOnce = require('./showOnce');
var toggle = require('./toggle');

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
      $form = $('.js-form'),
      $share = $('.share'),
      $doc = $(document);

  // TODO I want to rebuild the Init class to remove this check at some point.
  if ($('.landing').length < 1) {
    Init.countryRequirements();
    Init.inMemoryChanges();
  }

  Landing.createExpanders();
  Landing.createDataFilter();

  new UpdatePercent($('.js-fundingBar'));

  var discover = null,
      //hash = window.location.hash.substr(1) || 'issue',
      project = false,
      discoverHashObj = {},
      discoverSelectedCollapsible = false;
  //console.log('hash: ' + hash);

  if ($discoverApp.length > 0) {
    discover = new Discover($discoverApp);
    discoverHashObj = discover.parseHash();
    project = discoverHashObj.params['project'];
  }
  $('.js-collapsibleItem').each(function() {
    var collapsible,
        $this = $(this),
        id = $this.attr('id'),
        $control = $('[aria-controls="'+ id +'"]');

    collapsible = new Collapsible($this, $control, {
      hideControls: !($(this).hasClass('js-collapsibleNoHide')),
      startOpen: (!!discover && discover.currentProject === id)
    });
    if (!!discover && discover.currentProject === id) {
      discoverSelectedCollapsible = collapsible;
    }

    if (discover) {
      $this.on('collapsible:open', function(event){
        //console.log('collapsible:open', event);
        discover.selectProject(event.item.id, true);
      });
      $this.on('collapsible:close', function(event){
        //console.log('collapsible:close', event);
        discover.deselectProject(event.item.id, true);
      });
    }

    collapsible.render();
  });
  if (discoverSelectedCollapsible) {
    discoverSelectedCollapsible.hidden = false;
    discoverSelectedCollapsible.render();
  }

  if ($form) {
    form.initForm($form);
  }

  if ($share) {
    toggle.init($share, $share.find('.js-shareOn'), $share.find('.js-shareOff'));
  }

  jsusers.progEnhcJSUsers($doc);
  showOnce.showOnce($doc, 'localStorage' in window && window.localStorage);
});
