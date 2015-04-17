import celery

from sorl.thumbnail import default

from .conf import settings


@celery.task
def create_thumbnail(model, image_file, geometry_string, **options):
    # Simply call get_thumbnail, if thumbnail does not exist sorl will create it
    default.backend.get_thumbnail(image_file, geometry_string, **options)
    if settings.SAVE_MODEL:
        model.save(thumbnail_task_completed=True)  # helful for signaling haystack to update index
