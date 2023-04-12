import sys
from importlib import reload
import bpy

from . import *

def reload_modules():
    if not bpy.context.preferences.view.show_developer_ui:
        return
    reload(sys.modules[__name__])
    reload(img_loader)
    reload(preferences)
    reload(operators)
    reload(panel)
