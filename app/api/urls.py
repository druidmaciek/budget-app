from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import BudgetViewSet, LogInView, SignUpView, TransactionViewSet

router = routers.DefaultRouter()
router.register(r"api/budgets", BudgetViewSet, basename="budgets")
router.register(r"api/transactions", TransactionViewSet, basename="transactions")


urlpatterns = [
    path("", include(router.urls)),
    path("api/register/", SignUpView.as_view()),
    path("api/login/", LogInView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
]
