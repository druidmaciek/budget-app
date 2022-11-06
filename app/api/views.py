from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import BudgetSerializer, LogInSerializer, UserSerializer, TransactionSerializer
from .models import Transaction, Budget


class SignUpView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class LogInView(TokenObtainPairView):
    serializer_class = LogInSerializer


class BudgetResultsSetPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = "page_size"
    max_page_size = 100


class BudgetViewSet(ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = BudgetResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["owner"]

    def get_queryset(self):
        return self.request.user.all_user_budgets()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TransactionsResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TransactionsResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["type", "category", "budget"]

    def get_queryset(self):
        return Transaction.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        budget = serializer.validated_data['budget']
        serializer.save(owner=budget.owner)