from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    def all_user_budgets(self):
        qs = self.owned_budgets.all() | self.user_budgets.all().order_by("-updated_at")
        return qs


class Budget(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(
        get_user_model(), related_name="owned_budgets", on_delete=models.CASCADE
    )
    members = models.ManyToManyField(
        get_user_model(), related_name="user_budgets", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def members_count(self):
        count = self.members.count() + 1
        return f"{count} member{'s' if count != 1 else ''}"


class Transaction(models.Model):
    CATEGORIES = (
        ("taxes", "Taxes"),
        ("eating out", "Eating Out"),
        ("rent", "Rent"),
        ("shopping", "Shopping"),
        ("travel", "Travel"),
        ("other income", "Other Income"),
        ("salary", "Salary"),
    )
    TYPES = (("expense", "Expense"), ("income", "Income"))
    budget = models.ForeignKey(
        Budget, related_name="transactions", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    category = models.CharField(max_length=32, choices=CATEGORIES)
    type = models.CharField(max_length=7, choices=TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE
    )

    def __str__(self):
        expense_type = "-" if self.type == "expense" else "+"
        return f"{self.name} ({expense_type}{(self.amount/100):.2f})"
