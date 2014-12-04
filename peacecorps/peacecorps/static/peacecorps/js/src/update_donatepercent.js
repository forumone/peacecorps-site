/* Update donations percentages on project pages. */
'use strict';

var $ = require('jquery');

// TODO doesn't require a class.
var UpdatePercent = function($root){
  if ($root.length < 1) {
    return null;
  }
  this.$root = $root;
  this.init.apply(this, arguments);
};

UpdatePercent.prototype.getTotal = function(){
  $.ajax({
      url: '/api/account/' + this.code,
      method: 'GET'
  }).done(this.updateHTML.bind(this));
};

UpdatePercent.prototype.getCode = function(){
  var code = this.$root.data('project-code');
  return code;
};

UpdatePercent.prototype.updateHTML = function(oData){
  var bar = this.$root.find('.funded-amount-bar');
  var text = this.$root.find('.funded-amount-text');
  bar.css('max-width', oData.percent+'%');
  text.text(parseInt(
            Math.round(oData.percent), 10) + '% funded');
};

UpdatePercent.prototype.init = function(){
  this.code = this.getCode();
  this.getTotal();  //  rendered data may be out of date
  var seconds = 60;
  this.interval = setInterval(this.getTotal.bind(this), seconds * 1000);
};

module.exports = UpdatePercent;
