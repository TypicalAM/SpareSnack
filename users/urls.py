"""
URL configuration for the users app
"""

from importlib import import_module

from allauth.account import views as auth_views
from allauth.socialaccount import providers
from django.conf import settings
from django.urls import include, path

from users import views

urlpatterns = [
    path("profile/", views.profile, name="account_profile"),
    path("signup/", auth_views.signup, name="account_signup"),
    path("login/", auth_views.login, name="account_login"),
    path("logout/", views.logout, name="account_logout"),
    path(
        "password/change/",
        auth_views.password_change,
        name="account_change_password",
    ),
    path(
        "profile/goals",
        views.change_goals,
        name="account_change_goals",
    ),
    path(
        "profile/avatar",
        views.change_avatar,
        name="account_change_avatar",
    ),
]

if "allauth.socialaccount" in settings.INSTALLED_APPS:
    urlpatterns += [path("social/", include("allauth.socialaccount.urls"))]

provider_urlpatterns = []
for provider in providers.registry.get_list():
    try:
        prov_mod = import_module(provider.get_package() + ".urls")
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, "urlpatterns", None)
    if prov_urlpatterns:
        provider_urlpatterns += prov_urlpatterns

urlpatterns += provider_urlpatterns
