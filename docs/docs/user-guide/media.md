<h1>Media</h1>
In this section:

[TOC]

<hr>

Media can refer to photography, video, or audio uploaded to the site to be provided to users. Media is primarily managed through fields inside other objects on the site (such as projects or campaigns), where it is identified normally with a dropdown menu or text field with a magnifiying glass or + sign next to it.

## Uploading Media
When you decide to upload a media asset (currently, this is limited to imagery), you'll be provided a pop-up similar to this after clicking the "add-media" button or a green + sign.

![Add Media Box](images/addmediabox.png)

Within this box, there are several options:

- **File**: Upload a file from your computer. Images should be properly cropped and compressed. We use [ImageOptim](https://imageoptim.com/) for this.
- **Title**: A title for the media. Will mostly be used for image identification for admin users.
- **Media Type**: Defaults to `image`
- **Country**: The country the media originated in
- **Caption**: A caption for the media, if desired
- **Description**: A description of the media, for 508 purposes
- **Transcript**: A transcript of the media, if it is video or audio.

## Rich Content Editing
Some items on the site, like `Project` and `Campaign` descriptions, have _Rich Content Editing_ enabled. Rich Content Editing enables you to use an easy interface to make text styles, embed images, or do other stylistic changes to content. 

Fields which have Rich Content Editing enabled feature an interactive editor, like this:

![Rich Content Editor](images/rich_content_editor.png)

The Rich Text Editor is built using vertical _blocks_. Each block is stacked, one on top of the other, to make a page. As of now, two block types exist: **text** and **image**. To add another block to the stack, click the `+` sign at the top or bottom of the editor.

### Text Styles and Linking
Within a text block, you can _style_ text (bold or italic) as well as _link_ text to another page. To apply these styles, highlight the text you wish to edit, then use the option menu that appears to select bold, italic, link, or un-link:

![Text Styling](images/edit_text_style.png)


### Adding Blocks
To add a block, click the `+` button above or below an existing block (to add it above or below said block). You'll see a prompt asking you to select `text` or `image`:

![Add Block](images/add_block.png)

Selecting `text` will create another text block:

![Add Block](images/new_text_block.png)

Selecting `image` will create a new image block, to support inline images in text:

![Add Block](images/new_image_block.png)

Provide a **title**, **description**, and select **choose a file** to upload an image file from your computer. Images should be properly cropped and compressed. We use [ImageOptim](https://imageoptim.com/) for this.

### Deleting and Moving Blocks
You can move a block up or down in order by selecting the move icon, or delete it by selecting the trash can icon. Mouse over the block to highlight and show this menu.

![Move Block](images/move_block.png)