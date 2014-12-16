SirTrevor.Blocks.Image508 = SirTrevor.Block.extend({
  type: 'image508',
  title: 'Image508',
  droppable: true,
  uploadable: true,
  formattable: false,

  icon_name: 'image',

  editorHTML: function() {
    return [
      '<br  />',
      '<label class="st-input-label">Image Title</label>',
      '<input name="image_title" class="st-input-string st-required js-image_title-input"',
      ' type="text" /><br />',
      '<label class="st-input-label">Image Description</label>',
      '<input name = "image_description" size="81" class="st-input-string st-required js-image_description-input"',
      ' type="text" /><br />',
      /* '<div class="st-required st-text-block" contenteditable="true"></div>', */
      '<img width="95%" />',
    ].join("\n");
  },


  loadData: function(data){
    this.$('.js-image_description-input').val(data.image_description)
    this.$('.js-image_title-input').val(data.image_title);
    this.$('img').attr('src', data.file.url)

  },


  onBlockRender: function(){
    /* Setup the upload button */
    this.$inputs.find('button').bind('click', function(ev){ ev.preventDefault(); });
    this.$inputs.find('input').on('change', (function(ev) {
      this.onDrop(ev.currentTarget);
    }).bind(this));
  },

  onDrop: function(transferData){
    var file = transferData.files[0],
        urlAPI = (typeof URL !== "undefined") ? URL : (typeof webkitURL !== "undefined") ? webkitURL : null;

    // Handle one upload at a time
    if (/image/.test(file.type)) {
      this.loading();
      // Show this image on here
      this.$inputs.hide();
      this.$('img').attr('src', urlAPI.createObjectURL(file)).show();

      this.uploader(
        file,
        function(data) {
          this.setData(data);
          this.ready();
        },
        function(error) {
          this.addMessage(i18n.t('blocks:image:upload_error'));
          this.ready();
        }
      );
    }
  }
});