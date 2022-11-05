from django.urls import include, path

from .views import dashboard, register, add_budget

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("", dashboard, name="dashboard"),
    path("register/", register, name="register"),
    path("budget/add/", add_budget, name="add_budget"),
]
