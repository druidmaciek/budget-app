from django.urls import include, path

from .views import (add_budget, add_transaction, budget_detail, budget_edit,
                    dashboard, register)

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("", dashboard, name="dashboard"),
    path("register/", register, name="register"),
    path("budget/add/", add_budget, name="add_budget"),
    path("budget/<int:pk>/", budget_detail, name="budget_detail"),
    path("budget/edit/<int:pk>/", budget_edit, name="budget_edit"),
    path(
        "budget/add/transaction/<int:budget_id>/",
        add_transaction,
        name="add_transaction",
    ),
]
