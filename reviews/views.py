from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden

from ads.models import Ad
from reviews.forms import ReviewForm
from reviews.models import Review
from rentals.models import Rental


@login_required
def add_review(request, pk):
    ad = get_object_or_404(Ad, pk=pk)

    allowed = Rental.objects.filter(
        ad=ad,
        user=request.user,
        status=Rental.Status.COMPLETED,
    ).exists()

    if not allowed:
        return HttpResponseForbidden("You can review only services you have used.")

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ad = ad
            review.author = request.user
            review.save()
            return redirect("ads:ad_detail", pk=ad.pk)
    else:
        form = ReviewForm()

    return render(request, "reviews/add_review.html", {"form": form, "ad": ad})
