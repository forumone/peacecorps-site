/* Update donations percentages on project pages. */

var PC = PC || {};

(function($) {
  'use strict';

  PC.UpdatePercent = function(root){
    this.root = root;
  };
  PC.UpdatePercent.prototype.getTotal = function(){
    $.ajax({
        url: '/api/accountpercent?code=' + this.code,
        method: 'GET'
    }).done(this.updateHTML.bind(this));
  };
  PC.UpdatePercent.prototype.getCode = function(){
    this.code = this.root.data("project-code");
  };
  PC.UpdatePercent.prototype.updateHTML = function(oData){
    var bar = this.root.find(".funded-amount-bar");
    var text = this.root.find(".funded-amount-text");
    bar.css('max-width', oData.percent+'%');
    text.text(parseInt(
              Math.round(oData.percent), 10) + '% funded');
  };

  PC.UpdatePercent.prototype.init = function(){
    this.getCode();
    var seconds = 60;
    this.interval = setInterval(this.getTotal.bind(this), seconds * 1000);
  };

  var updatePercent = new PC.UpdatePercent($('#fundingbar'));
  updatePercent.init();

})(jQuery);