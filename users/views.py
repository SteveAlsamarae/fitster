from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages

from .forms import (
    UserUpdateForm,
    UserProfileUpdateForm,
    DeliveryAddressForm,
)
from .models import DeliveryAddress

# TODO:
# 1. Update rendering template for all views
# 2. Update redirect links


@login_required
def profile_update_view(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("users:update_profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=request.user.profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    return render(request, "account/update_profile.html", context)


@login_required
def add_delivery_address(request):
    if request.method == "POST":
        form = DeliveryAddressForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.customer = request.user.profile
            form.save()
            return redirect("users:customer_address")
        else:
            return HttpResponse("Invalid form input", status=400)
    else:
        form = DeliveryAddressForm()
    return render(request, "account/add_delivery_address.html", {"form": form})


@login_required
def edit_delivery_address(request, id):
    if request.method == "POST":
        customer_address = DeliveryAddress.objects.get(
            pk=id, customer=request.user.profile
        )
        address_form = DeliveryAddressForm(request.POST, instance=customer_address)
        if address_form.is_valid():
            address_form.save()
            return redirect("users:addresses")
    else:
        customer_address = DeliveryAddress.objects.get(
            pk=id, customer=request.user.profile
        )
        address_form = DeliveryAddressForm(instance=customer_address)
    return render(
        request,
        "account/dashboard/update_delivery_address.html",
        {"form": address_form},
    )


@login_required
def delete_delivery_address(request, id):
    delivery_address = DeliveryAddress.objects.filter(pk=id, customer=request.user)
    if delivery_address.exists():
        delivery_address.delete()
        return redirect("users:profile")
    return HttpResponse("Address not found", status=404)
