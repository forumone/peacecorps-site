'use strict';

var $ = require('jquery');

var UpdatePercent = require('./update_donatepercent');


$().ready(function() {
  var updatePercent = new UpdatePercent($('.js-fundingBar'));
  updatePercent.init();
  console.log('asldfjalsdjfalsd;kjfa;sldkfjasl;dkaj;afklsdfjl;ksd');
});
