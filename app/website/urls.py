from django.urls import include, path

from .views import add_budget, budget_detail, dashboard, register

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("", dashboard, name="dashboard"),
    path("register/", register, name="register"),
    path("budget/add/", add_budget, name="add_budget"),
    path("budget/<int:pk>/", budget_detail, name="budget_detail"),
]
