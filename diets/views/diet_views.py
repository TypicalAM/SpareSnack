"""Views concerning diet creation & browsing"""
from http import HTTPStatus
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404, JsonResponse
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.base import View
from django.views.generic.edit import DeleteView

from ..forms import DietCreateForm, DietImportForm
from ..models import Diet

BAD = {
    "data": {"status": "operation unsuccessfull"},
    "status": HTTPStatus.BAD_REQUEST,
}
SAVED = {"data": {"status": "data saved"}, "status": HTTPStatus.CREATED}


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


class DietCreate(LoginRequiredMixin, FormView):
    """FormView for creating a diet using the DietCreateForm"""

    form_class = DietCreateForm
    success_url = reverse_lazy("day-create")
    template_name = "diet/create.html"

    def form_valid(self, form):
        """Save the form if the request was valid"""
        form.save(self.request.user)
        return super().form_valid(form)


class DietImport(LoginRequiredMixin, View):
    """A view for importing the diet, usually from a redirect with a slug"""

    template_name = "diet/import.html"

    def get(self, *_):
        """Get the slug from the url"""
        diet = Diet.objects.filter(slug=self.request.GET.get("diet")).first()

        if not diet:
            raise Http404()
        context = {}
        context["diet"] = diet
        context["form"] = DietImportForm()
        return render(self.request, self.template_name, context)

    def post(self, *_):
        """Fill the form and save it"""
        form = DietImportForm(self.request.POST)
        if not form.is_valid():
            return JsonResponse(**BAD)

        form.save(self.request.user)
        return JsonResponse(**SAVED)


class DietDelete(LoginRequiredMixin, DeleteView):
    """A view for deleting a diet, usually from a redirect with a slug"""

    model = Diet
    context_object_name = "diet"
    template_name = "diet/delete.html"
    success_url = reverse_lazy("diet-browse")

    def get_context_data(self, **kwargs):
        """If the person here isn't the author, it's fishy"""

        context = super().get_context_data(**kwargs)
        diet = context.get("diet")

        if not diet or self.request.user != diet.author:
            raise Http404()
        return context
