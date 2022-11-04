from django.urls import include, path
from rest_framework import routers

from .views import BudgetViewSet

router = routers.DefaultRouter()
router.register(r'api/budgets', BudgetViewSet)
urlpatterns = [
     path('', include(router.urls)),
]