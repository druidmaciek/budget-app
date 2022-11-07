from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import UserRegistrationForm


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            return render(
                request, "registration/register_done.html", {"new_user": new_user}
            )
    else:
        user_form = UserRegistrationForm()
    return render(request, "registration/register.html", {"user_form": user_form})


@login_required
def dashboard(request):
    return render(request, "app/dashboard.html")


@login_required
def add_budget(request):
    return render(
        request, "app/budget/form.html", {"users": get_user_model().objects.all()}
    )


@login_required
def budget_detail(request, pk):
    return render(request, "app/budget/detail.html", {"id": pk})


@login_required
def budget_edit(request, pk):
    return render(
        request,
        "app/budget/edit_form.html",
        {"users": get_user_model().objects.all(), "id": pk},
    )


@login_required
def add_transaction(request, budget_id):
    return render(request, "app/transaction/form.html", {"budget_id": budget_id})
