SirTrevor.Blocks.Button = SirTrevor.Block.extend({
  type: 'button',
  title: 'Button',
  formattable: false,
  editorHTML: function() {
    return [
      '<div class="st-required st-text-block" contenteditable="true"></div>',
      '<label class="st-input-label">URL</label>',
      '<input name="url" class="st-input-string st-required js-url-input"',
      ' type="text" />'
    ].join("\n");
  },
  loadData: function(data) {
    this.getTextBlock().html(SirTrevor.toHTML(data.text, this.type));
    this.$('.js-url-input').val(data.url);
  },
});

(function() {
  var checkForImageButton = function() {
    for (var i = 0; i < SirTrevor.instances.length; i++) {
      var instance = SirTrevor.instances[i];
      for (var j = 0; j < instance.blocks.length - 1; j++) {
        var lhs = instance.blocks[j],
            rhs = instance.blocks[j+1];
        if (j === 0 && lhs.type === 'button') {
          lhs.setData({float_above: false});
        }
        if (rhs.type === 'button') {
          rhs.setData({float_above: lhs.type === 'image'});
        }
      }
    }
  };
  SirTrevor.EventBus.on('block:create:new', checkForImageButton);
  SirTrevor.EventBus.on('block:reorder:dropped', checkForImageButton);
})();
