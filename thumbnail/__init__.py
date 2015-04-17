from copy import copy

from sorl.thumbnail import get_thumbnail as original_get_thumbnail

from .conf import settings


def get_thumbnail(file_, name):
    """
    get_thumbnail version that uses aliasses defined in THUMBNAIL_OPTIONS_DICT
    """
    options_dict = getattr(file_.instance, 'THUMBNAIL_OPTIONS_DICT', settings.OPTIONS_DICT)
    options = options_dict[name]
    opt = copy(options)
    geometry = opt.pop('geometry')

    return original_get_thumbnail(file_, geometry, **opt)
