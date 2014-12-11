from sirtrevor.blocks import BaseBlock


class ButtonBlock(BaseBlock):
    name = "Button"

    class Media:
        js = ['contenteditor/js/buttonblock.js']
