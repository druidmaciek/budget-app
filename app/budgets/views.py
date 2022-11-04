from rest_framework.viewsets import ModelViewSet

from .models import Budget
from .serializers import BudgetSerializer


class BudgetViewSet(ModelViewSet):
    serializer_class = BudgetSerializer
    queryset = Budget.objects.all()
