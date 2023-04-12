from bpy.utils import previews
import os


# global list for storing icon collection
_CUSTOM_ICONS = None


def register_icons():
    """Load icon from the add-on folder"""
    global _CUSTOM_ICONS
    if _CUSTOM_ICONS:
        # the collection list is already  loaded
        return

    collection = previews.new()
    img_extensions = ('.png', '.jpg')
    
    module_path = os.path.dirname(__file__)
    picture_path = os.path.join(module_path, 'pictures')
    for img_file in os.listdir(picture_path):
        img_name, ext = os.path.splitext(img_file)
        
        if ext.lower() not in img_extensions:
            continue

        disk_path = os.path.join(picture_path, img_file)
        collection.load(img_name, disk_path, 'IMAGE')

    _CUSTOM_ICONS = collection


def unregister_icons():
    """Removes all loaded icons"""
    global _CUSTOM_ICONS
    if _CUSTOM_ICONS:
        previews.remove(_CUSTOM_ICONS)
    
    _CUSTOM_ICONS = None


def get_icons_collection():
    # load icons from disk
    register_icons()

    # at this point, we should have icons. A None _CUSTOM_ICONS would cause an error
    assert _CUSTOM_ICONS
    return _CUSTOM_ICONS
