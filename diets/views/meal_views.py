"""Views for creating/browsisng meals and managing the day"""
from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.http.response import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView
from django.views.generic.edit import DeleteView

from diets.forms import MealCreateForm, validate_day_post_save
from diets.models import Day, Ingredient, Meal, ThroughDayMeal


class MealCreate(LoginRequiredMixin, View):
    """View for creating meals"""

    template_name = "meal/create.html"

    def get_ingredient_data(self) -> JsonResponse:
        """Get the ingredient data from the server by a query"""
        data_dict = {}
        query = self.request.GET.get("q")
        if not query:
            return JsonResponse({}, status=HTTPStatus.BAD_REQUEST)

        ingredients = Ingredient.objects.filter(name__icontains=query)
        data_dict["results"] = serializers.serialize("json", ingredients)

        return JsonResponse(data_dict)

    def get(self, *_):
        """If the request is ajax, get ingredients else generate the form"""
        if not self.request.accepts("text/html"):
            return self.get_ingredient_data()

        context = {}
        context["form"] = MealCreateForm()
        return render(self.request, self.template_name, context)

    def post(self, *_):
        """Validate the form and create a meal"""
        form = MealCreateForm(self.request.POST, self.request.FILES)
        if not form.is_valid():
            return JsonResponse({}, status=HTTPStatus.BAD_REQUEST)

        form.save(self.request.user)
        return redirect(reverse_lazy("day-create"))


@method_decorator(csrf_exempt, name="dispatch")
class DayCreate(LoginRequiredMixin, View):
    """View for creating days"""

    template_name = "day/create.html"

    def get_data(self) -> JsonResponse:
        """Get the searched meal or the selected day data"""
        data_dict = {}
        search_query = self.request.GET.get("q")
        day_query = self.request.GET.get("d")

        if not search_query and not day_query:
            return JsonResponse({}, status=HTTPStatus.BAD_REQUEST)
        if search_query:
            recipes = Meal.objects.filter(name__icontains=search_query)[:5]
            data_dict["search_results"] = serializers.serialize("json", recipes)
        if day_query:
            day, _ = Day.objects.get_or_create(
                date=day_query, author=self.request.user, backup=False
            )
            inter = ThroughDayMeal.objects.filter(day=day)
            meals = [obj.meal for obj in inter]
            meal_nums = [obj.meal_num for obj in inter]
            data_dict["meals"] = serializers.serialize("json", meals)
            data_dict["meal_nums"] = str(meal_nums)
        return JsonResponse(data_dict)

    def get(self, *_):
        """If the request is ajax get data, else return the template"""
        if not self.request.accepts("text/html"):
            return self.get_data()
        return render(self.request, self.template_name)

    def post(self, *_):
        """Receive a day update"""
        check = validate_day_post_save(self.request)
        if not check:
            return JsonResponse({}, status=HTTPStatus.BAD_REQUEST)

        meals, meal_nums, date = check

        day = Day.objects.get(date=date, author=self.request.user, backup=False)
        for rel in ThroughDayMeal.objects.filter(day=day):
            rel.delete()
        for meal, meal_num in zip(meals, meal_nums):
            ThroughDayMeal.objects.create(
                day=day, meal=meal, meal_num=meal_num
            ).save()
        return JsonResponse({}, status=HTTPStatus.CREATED)


class MealBrowse(ListView):
    """Browse different meals"""

    model = Meal
    context_object_name = "meals"
    template_name = "meal/browse.html"
    paginate_by = 5


class MealDetail(DetailView):
    """Details page for a meal"""

    model = Meal
    context_object_name = "meal"
    template_name = "meal/view.html"


class MealDelete(LoginRequiredMixin, DeleteView):
    """Delete a meal that you have created"""

    model = Meal
    context_object_name = "meal"
    template_name = "meal/delete.html"
    success_url = reverse_lazy("day-create")

    def get_context_data(self, **kwargs):
        """If the person here isn't the author, it's fishy"""
        context = super().get_context_data(**kwargs)
        meal = context.get("meal")
        if not meal or self.request.user != meal.author:
            raise Http404
        return context


class UserMeals(ListView, LoginRequiredMixin):
    """ListView for showing the user his/her diets"""

    model = Meal
    context_object_name = "meals"
    template_name = "meals.html"
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        """Get only the meals which the user has authored"""
        queryset = super().get_queryset(*args, **kwargs)
        return queryset.filter(author=self.request.user)
