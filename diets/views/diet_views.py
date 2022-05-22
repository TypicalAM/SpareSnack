from http import HTTPStatus
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.base import View

from ..forms import DietCreateForm, DietImportForm
from ..models import Diet

BAD = {'data' : {'status' : 'operation unsuccessfull'},'status' : HTTPStatus.BAD_REQUEST}
SAVED = {'data' : {'status' : 'data saved'}, 'status' : HTTPStatus.CREATED}

class DietBrowse(ListView):

    model               = Diet
    context_object_name = 'diets'
    template_name       = 'diet/browse.html'
    paginate_by         = 10

    def get_queryset(self, *_):
        return Diet.objects.filter(public=True)

class DietDetail(DetailView):

    model               = Diet
    context_object_name = 'diet'
    template_name       = 'diet/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class DietCreate(FormView, LoginRequiredMixin):

    form_class          = DietCreateForm
    success_url         = reverse_lazy('day-create')
    template_name       = 'diet/create.html'

    def form_valid(self, form):
        form.save(self.request.user)
        return super(DietCreate, self).form_valid(form)


class DietImport(View, LoginRequiredMixin):

    template_name = 'diet/import.html'

    def get(self, *_):
        diet = Diet.objects.filter(slug=self.request.GET.get('diet')).first()
        if not diet:
            return JsonResponse(**BAD)
        context = {}
        context['diet'] = diet
        context['form'] = DietImportForm()
        return render(self.request, self.template_name, context)

    def post(self, *_):
        form = DietImportForm(self.request.POST)
        if not form.is_valid():
            print('Errors')
            print(form.errors)
            return JsonResponse(**BAD)

        form.save(self.request.user)
        return JsonResponse(**SAVED)
