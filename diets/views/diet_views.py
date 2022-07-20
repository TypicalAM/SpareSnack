"""Views concerning diet creation & browsing"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import Http404
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.edit import DeleteView

from diets.forms import DietCreateForm, DietImportForm
from diets.models import Diet


class DietBrowse(ListView):
    """ListView for browsing different diets"""

    model = Diet
    context_object_name = "diets"
    template_name = "diet/browse.html"
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        """Get only the public diets"""
        queryset = super().get_queryset(*args, **kwargs)
        return queryset.filter(public=True)


class DietDetail(DetailView):
    """DetailView for viewing a certain diet"""

    model = Diet
    context_object_name = "diet"
    template_name = "diet/view.html"


class DietCreate(LoginRequiredMixin, SuccessMessageMixin, FormView):
    """FormView for creating a diet using the DietCreateForm"""

    form_class = DietCreateForm
    template_name = "diet/create.html"
    success_url = reverse_lazy("day-create")
    success_message = "The diet has been created"

    def form_valid(self, form):
        """Save the form if the request was valid"""
        form.save(self.request.user)
        return super().form_valid(form)


class DietImport(LoginRequiredMixin, SuccessMessageMixin, FormView):
    """A view for importing the diet, usually from a redirect with a slug"""

    form_class = DietImportForm
    template_name = "diet/import.html"
    success_url = reverse_lazy("diet-browse")
    success_message = "Successfully imported the diet!"

    def get(self, request, *, slug):
        """Get the slug from the url"""
        diet = Diet.objects.filter(slug=slug).first()
        if not diet:
            raise Http404

        context = self.get_context_data()
        context["diet"] = diet
        return render(request, self.template_name, context)

    def form_valid(self, form):
        """Save the form if the request was valid"""
        form.save(self.request.user)
        return super().form_valid(form)


class DietDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """A view for deleting a diet, usually from a redirect with a slug"""

    model = Diet
    context_object_name = "diet"
    template_name = "diet/delete.html"
    success_url = reverse_lazy("diet-browse")
    success_message = "The diet has been deleted"

    def get_context_data(self, **kwargs):
        """If the person here isn't the author, it's fishy"""
        context = super().get_context_data(**kwargs)
        diet = context.get("diet")
        if not diet or self.request.user != diet.author:
            raise Http404
        return context
