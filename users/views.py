from diets.models import Diet, Meal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic import FormView, ListView
from django.views.generic.base import View

from .forms import UserCreationForm

class UserDiets(ListView, LoginRequiredMixin):

    model               = Diet
    context_object_name = 'diets'
    template_name       = 'users/diets.html'
    paginate_by         = 1

    def get_queryset(self, *_):
        return Diet.objects.filter(author=self.request.user)

class UserMeals(ListView, LoginRequiredMixin):

    model               = Meal
    context_object_name = 'meals'
    template_name       = 'users/meals.html'
    paginate_by         = 5

    def get_queryset(self, *_):
        return Meal.objects.filter(author=self.request.user)


class UserProfile(View, LoginRequiredMixin):

    template_name       = 'users/profile.html'

    def get(self, *_):
        context = {}
        context['user'] = self.request.user
        return render(self.request, self.template_name, context)

class UserRegisterView(FormView):

    form_class      = UserCreationForm
    success_url     = reverse_lazy('login')
    template_name   = 'users/register.html'
