from http import HTTPStatus as Status
import json
from json.decoder import JSONDecodeError

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView

from ..forms import MealForm
from ..models import Day, Ingredient, IntermediaryDayMeal, Meal

OK  = {'data' : {'status' : 'operation successfull'},'status' : Status.OK}
BAD = {'data' : {'status' : 'operation unsuccessfull'},'status' : Status.BAD_REQUEST}
SAVED = {'data' : {'status' : 'data saved'}, 'status' : Status.CREATED}

class MealCreate(View, LoginRequiredMixin):
    """View for creating meals"""
    template_name = 'meal/create.html'

    def get_ingredient_data(self) -> JsonResponse:
        data_dict = {}
        query = self.request.GET.get('q')
        if not query:
            return JsonResponse(**BAD)

        ingredients = Ingredient.objects.filter(name__icontains=query)
        data_dict['results'] = serializers.serialize('json', ingredients)

        return JsonResponse(data_dict)

    def get(self, *_):
        if not self.request.accepts('text/html'):
            return self.get_ingredient_data()

        context = {}
        context['form'] = MealForm(self.request.user)
        return render(self.request, self.template_name, context)

    def post(self, *_):
        form = MealForm(self.request.user, self.request.POST, self.request.FILES)
        if not form.is_valid():
            return JsonResponse(**BAD)

        form.save()
        return redirect(reverse_lazy('day-create'))



@method_decorator(csrf_exempt, name='dispatch')
class DayCreate(View, LoginRequiredMixin):
    """View for creating days"""
    template_name = 'day/create.html'

    def get_data(self) -> JsonResponse:
        data_dict = {}
        search_query= self.request.GET.get('q')
        day_query   = self.request.GET.get('d')

        if not search_query and not day_query:
            return JsonResponse(**BAD)
        if search_query:
            recipes     = Meal.objects.filter(name__icontains=search_query)[:5]
            data_dict['search_results'] = serializers.serialize('json', recipes)
        if day_query:
            day , _     = Day.objects.get_or_create(date=day_query, author=self.request.user, backup=False)
            inter       = IntermediaryDayMeal.objects.filter(day=day)
            meals       = [obj.meal for obj in inter]
            meal_nums   = [obj.meal_num for obj in inter]
            data_dict['meals']      = serializers.serialize('json', meals)
            data_dict['meal_nums']  = str(meal_nums)
        return JsonResponse(data_dict)

    def get(self, *_):
        if not self.request.accepts('text/html'):
            return self.get_data()
        return render(self.request, self.template_name)

    def validate_save_data(self) -> bool:
        try:
            json_object= json.loads(self.request.body)
            meals      = [Meal.objects.get(name=obj.object.name, pk=obj.object.pk) for obj in serializers.deserialize("json",json_object['meals'])]
            meal_nums  = [int(x) for x in (json_object['meal_nums'][1:-1].split(','))]
            date       = json_object['date']
        except (JSONDecodeError, KeyError, ValueError):
            return False
        if len(meals) != len(meal_nums) or not (meals and meal_nums and date):
            return False
        self.meals      = meals
        self.meal_nums  = meal_nums
        self.date       = date
        return True

    def post(self, *_):
        check = self.validate_save_data()
        if not check:
            return JsonResponse(**BAD)
        day = Day.objects.get(date=self.date, author=self.request.user, backup=False)
        for rel in IntermediaryDayMeal.objects.filter(day=day):
            rel.delete()
        for i in range(len(self.meals)):
            IntermediaryDayMeal.objects.create(
                day         = day,
                meal        = self.meals[i],
                meal_num    = self.meal_nums[i]
            ).save()
        return JsonResponse(**SAVED)

class MealBrowse(ListView):

    model               = Meal
    context_object_name = 'meals'
    template_name       = 'meal/browse.html'
    paginate_by         = 5

class MealDetail(DetailView):

    model               = Meal
    context_object_name = 'meal'
    template_name       = 'meal/view.html'
