from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Budget
from .serializers import BudgetSerializer, LogInSerializer, UserSerializer


class SignUpView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class LogInView(TokenObtainPairView):
    serializer_class = LogInSerializer


class BudgetViewSet(ModelViewSet):
    serializer_class = BudgetSerializer
    queryset = Budget.objects.all()
