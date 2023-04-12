
bl_info = {
    "name": "A Structured Add-on",
    "author": "John Doe",
    "version": (1, 0),
    "blender": (3, 2, 0),
    "description": "Add-on consisting of multiple files",
    "category": "Learning",
}


from . import operators
from . import img_loader
from . import panel
from . import preferences
from . import _refresh_
_refresh_.reload_modules()


def register():
    preferences.register_classes()
    operators.register_classes()
    img_loader.register_icons()
    panel.register_classes()


def unregister():
    panel.unregister_classes()
    img_loader.unregister_icons()
    operators.unregister_classes()
    preferences.unregister_classes()
