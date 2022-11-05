from itertools import chain

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    def all_user_budgets(self):
        return list(chain(self.owned_budgets.all(), self.user_budgets.all()))


class Budget(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(
        get_user_model(), related_name="owned_budgets", on_delete=models.CASCADE
    )
    members = models.ManyToManyField(get_user_model(), related_name="user_budgets")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def members_count(self):
        return self.members.count() + 1


class TransactionBaseModel(models.Model):
    CATEGORIES = (
        ("taxes", "Taxes"),
        ("eating out", "Eating Out"),
        ("rent", "Rent"),
        ("shopping", "Shopping"),
        ("travel", "Travel"),
        ("other income", "Other Income"),
        ("salary", "Salary"),
    )
    budget = models.ForeignKey(Budget, related_name="inc/exp", on_delete=models.CASCADE)
    amount = models.IntegerField()
    category = models.CharField(max_length=32, choices=CATEGORIES)

    class Meta:
        abstract = True


class Income(models.Model):
    @staticmethod
    def get_budget_related_name():
        return "incomes"


class Expense(models.Model):
    @staticmethod
    def get_budget_related_name():
        return "expenses"
