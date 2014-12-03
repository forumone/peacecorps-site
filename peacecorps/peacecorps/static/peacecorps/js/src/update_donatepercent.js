/* Update donations percentages on project pages. */
'use strict';

var $ = require('jquery');

var UpdatePercent = function(root){
  this.$root = root;
};

UpdatePercent.prototype.getTotal = function(){
  $.ajax({
      url: '/api/account/' + this.code,
      method: 'GET'
  }).done(this.updateHTML.bind(this));
};

UpdatePercent.prototype.getCode = function(){
  this.code = this.$root.data('project-code');
};

UpdatePercent.prototype.updateHTML = function(oData){
  var bar = this.$root.find('.funded-amount-bar');
  var text = this.$root.find('.funded-amount-text');
  bar.css('max-width', oData.percent+'%');
  text.text(parseInt(
            Math.round(oData.percent), 10) + '% funded');
};

UpdatePercent.prototype.init = function(){
  this.getCode();
  this.getTotal();  //  rendered data may be out of date
  var seconds = 60;
  this.interval = setInterval(this.getTotal.bind(this), seconds * 1000);
};

module.exports = UpdatePercent;
