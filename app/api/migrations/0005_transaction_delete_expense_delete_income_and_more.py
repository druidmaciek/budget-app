# Generated by Django 4.1.3 on 2022-11-05 19:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_budget_members_alter_budget_owner_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("amount", models.IntegerField()),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("taxes", "Taxes"),
                            ("eating out", "Eating Out"),
                            ("rent", "Rent"),
                            ("shopping", "Shopping"),
                            ("travel", "Travel"),
                            ("other income", "Other Income"),
                            ("salary", "Salary"),
                        ],
                        max_length=32,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("expense", "Expense"), ("income", "Income")],
                        max_length=7,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.DeleteModel(
            name="Expense",
        ),
        migrations.DeleteModel(
            name="Income",
        ),
        migrations.AlterField(
            model_name="budget",
            name="members",
            field=models.ManyToManyField(
                blank=True, related_name="user_budgets", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="transaction",
            name="budget",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="transactions",
                to="api.budget",
            ),
        ),
    ]
