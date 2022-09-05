"""Utilities for the SpareSnack project"""

import os
from uuid import uuid4

from django.contrib import messages
from django.shortcuts import render
from django.utils.deconstruct import deconstructible


@deconstructible
class UploadAndRename:
    """Made to help with making sensible filenames for images"""

    def __init__(self, path):
        """
        Determine the sub_path
        """
        self.sub_path = path

    def __call__(self, instance, filename):
        """Make and return the filenames"""
        ext = filename.split(".")[-1]
        model_name = instance.__class__.__name__.lower()
        filename = f"{model_name}_{uuid4().hex}.{ext}"
        return os.path.join(self.sub_path, filename)


def image_clean_up(instance, image_field_name="image"):
    """Clean up old photos after updating"""
    proxy = instance._meta.proxy_for_model  # pylint: disable=protected-access
    model = proxy if proxy else instance.__class__

    image_field = getattr(model, image_field_name, None)
    image_default = image_field.field.default if image_field else None

    try:
        image_old = getattr(
            model.objects.get(pk=instance.pk), image_field_name, None
        )
    except model.DoesNotExist:
        return

    image_new = getattr(instance, image_field_name, None)
    if image_old and image_new and image_old != image_new:
        if not image_default or image_default != image_old:
            image_old.delete(save=False)


class PassUserFormMixin:
    """A mixin made to pass the user as an additional kwargs to a form"""

    def get_form_kwargs(self):
        """Add the user as the author"""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Save the form and inform the user"""
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        """Inform the user that the form doesn't want his bad data"""
        for _, error in form.errors.items():
            messages.error(self.request, ", ".join(error))
            return render(self.request, self.template_name)
