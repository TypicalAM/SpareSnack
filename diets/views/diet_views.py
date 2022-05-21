from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse_lazy
from django.views.generic import DetailView, FormView, ListView

from ..forms import DietForm
from ..models import Diet

class DietBrowse(ListView):

    model               = Diet
    context_object_name = 'diets'
    template_name       = 'diet/browse.html'
    paginate_by         = 1

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

    form_class          = DietForm
    success_url         = reverse_lazy('day-create')
    template_name       = 'diet/create.html'

    def form_valid(self, form):
        form.save(self.request.user)
        return super(DietCreate, self).form_valid(form)
