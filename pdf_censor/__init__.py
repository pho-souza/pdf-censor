import os
import sys

# __DIR__ contains the actual directory that this file is in.
if hasattr(sys, '_MEIPASS'):
    __DIR__ = getattr(
        sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__))
    )
else:
    __DIR__ = os.path.abspath(os.path.dirname(__file__))

# Images
# pdf_censor/gui_assets/delete.png
__GUI_ASSETS__ = os.path.join(__DIR__, 'gui_assets')

__IMG_ADD__ = os.path.join(__GUI_ASSETS__, 'add.png')
__IMG_FILE__ = os.path.join(__GUI_ASSETS__, 'file.png')
__IMG_TRASH__ = os.path.join(__GUI_ASSETS__, 'trash.png')
__IMG_DELETE__ = os.path.join(__GUI_ASSETS__, 'delete.png')
__IMG_SAVE__ = os.path.join(__GUI_ASSETS__, 'save.png')
__IMG_LOGO__ = os.path.join(__GUI_ASSETS__, 'logo.png')
