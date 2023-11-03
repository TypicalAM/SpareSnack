"""Views for creating/browsisng meals and managing the day"""
from http import HTTPStatus
import json
from typing import Any

from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core import serializers
from django.forms.models import ModelForm
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView
from django.views.generic.edit import DeleteView

from core.utils import PassUserFormView
from foods.forms import DayCreateForm, MealCreateForm
from foods.models import Day, Ingredient, Meal, ThroughDayMeal, ThroughMealIngr


def homepage_view(request: HttpRequest) -> HttpResponse:
    """A basic view of the index page"""
    return render(request, "general/index.html")


class MealCreate(SuccessMessageMixin, PassUserFormView):
    """View for creating meals"""

    form_class = MealCreateForm
    template_name = "meal/create.html"
    success_url = reverse_lazy("foods_day_create")
    success_message = "The meal has been created"

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        """If the request is ajax, get ingredients else generate the form"""
        if self.request.accepts("text/html"):
            return super().get(request, *args, **kwargs)

        # Get ingredients
        query = self.request.GET.get("q")
        if not query:
            return JsonResponse({}, status=HTTPStatus.UNPROCESSABLE_ENTITY)

        ingredients = Ingredient.objects.filter(name__icontains=query)[:5]
        data = {"results": serializers.serialize("json", ingredients)}
        return JsonResponse(data)


create = login_required(MealCreate.as_view())


@method_decorator(csrf_exempt, "dispatch")
class DayCreate(PassUserFormView):
    """View for creating days"""

    form_class = DayCreateForm
    template_name = "day/create.html"
    success_url = reverse_lazy("foods_day_create")

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        """If the request is ajax get data"""
        if not request.accepts("text/html"):
            return self.get_search_data()

        return super().get(request, *args, **kwargs)

    def form_valid(self, form: ModelForm) -> HttpResponse:
        """Save the form and inform the user"""
        form.save()
        return JsonResponse({"Status": "Saved"}, status=HTTPStatus.OK)

    def form_invalid(self, form: ModelForm) -> HttpResponse:
        """Inform the user that the form doesn't want his bad data"""
        return JsonResponse(
            {"Status": "Saved"}, status=HTTPStatus.UNPROCESSABLE_ENTITY
        )

    def get_form_kwargs(self) -> dict[str, Any]:
        """Make sure that request data is getting processed correctly"""
        kwargs = super().get_form_kwargs()
        if self.request.method == "POST":
            kwargs.update({"data": json.loads(self.request.body)})
        return kwargs

    def get_search_data(self) -> JsonResponse:
        """Get the searched meal or the selected day data"""
        data_dict = {}
        search_query = self.request.GET.get("q")
        day_query = self.request.GET.get("d")

        if not search_query and not day_query:
            return JsonResponse({}, status=HTTPStatus.UNPROCESSABLE_ENTITY)

        if search_query:
            recipes = Meal.objects.filter(name__icontains=search_query)[:5]
            data_dict["search_results"] = serializers.serialize("json", recipes)

        if day_query:
            day, _ = Day.objects.get_or_create(
                date=day_query, author=self.request.user, backup=False
            )
            from django.db import reset_queries
            from django.db import connection
            inter = ThroughDayMeal.objects.filter(day=day)
            print(connection.queries)
            meals = [obj.meal for obj in inter]
            meal_nums = [obj.meal_num for obj in inter]
            data_dict["meals"] = serializers.serialize("json", meals)
            data_dict["meal_nums"] = str(meal_nums)

        return JsonResponse(data_dict)


day_create = login_required(DayCreate.as_view())


class MealBrowse(ListView):
    """Browse different meals"""

    model = Meal
    context_object_name = "meals"
    template_name = "meal/browse.html"
    paginate_by = 10


browse = MealBrowse.as_view()


class MealDetail(DetailView):
    """Details page for a meal"""

    model = Meal
    context_object_name = "meal"
    template_name = "meal/view.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Get the ingredient amount data in addition to the meal"""
        context = super().get_context_data(**kwargs)
        meal = context.get("meal")
        context["ingredients"] = (
            ThroughMealIngr.objects.filter(meal=meal) if meal else None
        )
        return context


detail = MealDetail.as_view()


class MealDelete(SuccessMessageMixin, DeleteView):
    """Delete a meal that you have created"""

    model = Meal
    context_object_name = "meal"
    template_name = "meal/delete.html"
    success_url = reverse_lazy("foods_day_create")
    success_message = "The meal has been deleted"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """If the person here isn't the author, it's fishy"""
        context = super().get_context_data(**kwargs)
        meal = context.get("meal")
        if not meal or self.request.user != meal.author:
            raise Http404
        context["ingredients"] = ThroughMealIngr.objects.filter(meal=meal)
        return context


delete = login_required(MealDelete.as_view())
