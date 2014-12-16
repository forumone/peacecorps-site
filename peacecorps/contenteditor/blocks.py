from sirtrevor.blocks import BaseBlock


class ButtonBlock(BaseBlock):
    name = "Button"

    class Media:
        js = ['contenteditor/js/buttonblock.js']


class Image508Block(BaseBlock):
    name = 'Image508'

    class Media:
        js = ['contenteditor/js/image508block.js']