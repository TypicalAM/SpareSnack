"""Utilities for the SpareSnack project"""

import os
from uuid import uuid4

from django.utils.deconstruct import deconstructible


@deconstructible
class UploadAndRename:
    """Made to help with making sensible filenames for images"""

    def __init__(self, path):
        """Determine the sub_path"""
        self.sub_path = path

    def __call__(self, instance, filename):
        """Make and return the filenames"""
        ext = filename.split(".")[-1]
        model_name = instance.__class__.__name__.lower()
        filename = f"{model_name}_{uuid4().hex}.{ext}"
        return os.path.join(self.sub_path, filename)


def image_clean_up(instance, image_field_name="image"):
    """Cleans up the old images if there are any"""
    proxy = instance._meta.proxy_for_model  # pylint: disable=protected-access
    model = proxy if proxy else instance.__class__

    try:
        image_old = getattr(
            model.objects.get(pk=instance.pk), image_field_name, None
        )
        image_new = getattr(instance, image_field_name, None)
        if image_old and image_new and image_old != image_new:
            print("deleted an image")
            image_old.delete(save=False)
    except model.DoesNotExist:
        pass
