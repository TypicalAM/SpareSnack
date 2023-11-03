"""Views concerning diet creation & browsing"""
from typing import Any, cast
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import DeleteView

from core.utils import PassUserFormView
from foods.forms import DietCreateForm, DietImportForm
from foods.models import Diet


class DietBrowse(ListView):
    """ListView for browsing different diets"""

    model = Diet
    context_object_name = "diets"
    template_name = "diet/browse.html"
    paginate_by = 10

    def get_queryset(self, *args: Any, **kwargs: Any) -> QuerySet:
        """Get only the public diets"""
        queryset = cast(QuerySet, super().get_queryset(*args, **kwargs))
        print(queryset.filter(public=True).query)
        return queryset.filter(public=True)


browse = DietBrowse.as_view()


class DietDetail(DetailView):
    """DetailView for viewing a certain diet"""

    model = Diet
    context_object_name = "diet"
    template_name = "diet/view.html"


detail = DietDetail.as_view()


class DietCreate(SuccessMessageMixin, PassUserFormView):
    """FormView for creating a diet using the DietCreateForm"""

    form_class = DietCreateForm
    template_name = "diet/create.html"
    success_url = reverse_lazy("foods_day_create")
    success_message = "The diet has been created"


create = login_required(DietCreate.as_view())


class DietImport(SuccessMessageMixin, PassUserFormView):
    """A view for importing the diet, usually from a redirect with a slug"""

    form_class = DietImportForm
    template_name = "diet/import.html"
    success_url = reverse_lazy("foods_diet_browse")
    success_message = "Successfully imported the diet!"

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        """Get the slug from the url"""
        diet = Diet.objects.filter(slug=kwargs.pop("slug")).first()
        if not diet:
            raise Http404

        context = self.get_context_data()
        context["diet"] = diet
        return render(request, self.template_name, context)


imprt = login_required(DietImport.as_view())


class DietDelete(SuccessMessageMixin, DeleteView):
    """A view for deleting a diet, usually from a redirect with a slug"""

    model = Diet
    context_object_name = "diet"
    template_name = "diet/delete.html"
    success_url = reverse_lazy("foods_diet_browse")
    success_message = "The diet has been deleted"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """If the person here isn't the author, it's fishy"""
        context = super().get_context_data(**kwargs)
        diet = context.get("diet")
        if not diet or self.request.user != diet.author:
            raise Http404
        return context


delete = login_required(DietDelete.as_view())
