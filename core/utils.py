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

    image_field = getattr(model, image_field_name, None)
    if image_field:
        image_default = image_field.field.default

    try:
        image_old = getattr(
            model.objects.get(pk=instance.pk), image_field_name, None
        )
        image_new = getattr(instance, image_field_name, None)
        if image_old and image_new and image_old != image_new:
            if image_default and image_default == image_old:
                print("not deleting because it is the default image")
                # Not deleting the image (it is the default one) - don't save the model
                return False
            # Delete the old image, save the model
            image_old.delete(save=False)
            return True
    except model.DoesNotExist:
        pass
    return True
