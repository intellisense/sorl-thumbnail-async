from copy import copy
from django.db.models import signals
from django.dispatch import receiver

from .conf import settings
from .tasks import create_thumbnail

class AsyncThumbnailMixin(object):
    """
    All model which have ImageField to be thumbnailed inheret from this class.
    """
    image_field_name = 'picture'

    def call_upload_task(self):
        options_dict = getattr(self, 'THUMBNAIL_OPTIONS_DICT', settings.OPTIONS_DICT)
        for name, options in options_dict.items():
            opt = copy(options)
            geometry = opt.pop('geometry')
            create_thumbnail.delay(self, getattr(self, self.image_field_name), geometry, **opt)

    def save(self, *args, **kwargs):
        thumbnail_task_completed = kwargs.pop('thumbnail_task_completed', False)
        super(AsyncThumbnailMixin, self).save(*args, **kwargs)
        if not thumbnail_task_completed:
            self.call_upload_task()
