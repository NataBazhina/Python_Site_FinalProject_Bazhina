from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ads.models import Ad
from reviews.forms import ReviewForm
from .forms import RentalForm
from .models import Rental


@login_required
def create_rental(request, pk):
    ad = get_object_or_404(Ad, pk=pk)

    if request.method == "POST":
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.ad = ad
            rental.renter = request.user
            rental.status = Rental.Status.PENDING
            rental.save()
            return redirect("ads:detail", pk=ad.pk)
    else:
        form = RentalForm()

    return render(request, "rentals/create_rental.html", {"ad": ad, "form": form})


@login_required
def my_rentals(request):
    rentals = Rental.objects.filter(renter=request.user).select_related("ad").order_by("-id")
    return render(request, "rentals/my_rentals.html", {"rentals": rentals})


@login_required
def add_review(request, rental_id):
    rental = get_object_or_404(Rental, pk=rental_id, renter=request.user)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ad = rental.ad
            review.author = request.user
            review.save()
            return redirect("rentals:my_rentals")
    else:
        form = ReviewForm()

    return render(request, "reviews/add_review.html", {"form": form, "rental": rental})
