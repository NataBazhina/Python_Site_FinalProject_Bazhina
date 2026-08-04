from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from ads.models import Ad


def is_moderator(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(is_moderator)
def pending_ads(request):
    ads = Ad.objects.filter(status=Ad.Status.PENDING).order_by("-created_at")
    return render(request, "moderation/pending_ads.html", {"ads": ads})


@login_required
@user_passes_test(is_moderator)
def approve_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    ad.publish()
    return redirect("moderation:pending_ads")


@login_required
@user_passes_test(is_moderator)
def reject_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    ad.reject()
    return redirect("moderation:pending_ads")
