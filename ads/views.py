from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone

from reviews.forms import ReviewForm
from .models import Ad
from .forms import AdForm
from reviews.models import Review
from rentals.models import Rental


def ad_list(request):
    ads = Ad.objects.all()

    for ad in ads:
        active_rental = Rental.objects.filter(
            ad=ad,
            status=Rental.Status.APPROVED,
            start_date__lte=timezone.now().date(),
            end_date__gte=timezone.now().date(),
        ).first()

        ad.is_booked = active_rental is not None
        ad.booked_from = active_rental.start_date if active_rental else None
        ad.booked_to = active_rental.end_date if active_rental else None

    return render(request, "ads/ad_list.html", {"ads": ads})


def home(request):
    ads = Ad.objects.filter(status=Ad.Status.PUBLISHED)

    q = request.GET.get("q", "").strip()
    location = request.GET.get("location", "").strip()
    price_from = request.GET.get("price_from", "").strip()
    price_to = request.GET.get("price_to", "").strip()

    if q:
        ads = ads.filter(
            Q(title__icontains=q) | Q(description__icontains=q)
        )

    if location:
        ads = ads.filter(location__icontains=location)

    if price_from:
        ads = ads.filter(price__gte=price_from)

    if price_to:
        ads = ads.filter(price__lte=price_to)

    return render(
        request,
        "ads/home.html",
        {
            "ads": ads,
            "q": q,
            "location": location,
            "price_from": price_from,
            "price_to": price_to,
        },
    )


def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    can_review = False

    if request.user.is_authenticated:
        can_review = Rental.objects.filter(
            ad=ad,
            user=request.user,
            status=Rental.Status.COMPLETED,
        ).exists()

    reviews = ad.reviews.select_related("author").all()

    return render(
        request,
        "ads/ad_detail.html",
        {
            "ad": ad,
            "reviews": reviews,
            "form": ReviewForm(),
            "can_review": can_review,
        },
    )


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = "ads/ad_form.html"
    success_url = reverse_lazy("home")
    login_url = "users:login"
    redirect_field_name = "next"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class AdDetailView(DetailView):
    model = Ad
    template_name = "ads/ad_detail.html"
    context_object_name = "ad"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = Review.objects.filter(ad=self.object).select_related("author")
        return context

class AdUpdateView(LoginRequiredMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = "ads/ad_form.html"
    success_url = reverse_lazy("home")
    login_url = "users:login"
    redirect_field_name = "next"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        self.object = self.get_object()

        if self.object.author != request.user:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)


class AdListView(ListView):
    model = Ad
    template_name = "ads/ad_list.html"
    context_object_name = "ads"


class AdMyAdsView(LoginRequiredMixin, ListView):
    model = Ad
    template_name = "ads/my_ads.html"
    context_object_name = "ads"

    def get_queryset(self):
        return Ad.objects.filter(author=self.request.user)


@login_required
def my_ads(request):
    ads = Ad.objects.filter(author=request.user)

    status_filter = request.GET.get("status", "").strip()
    if status_filter:
        ads = ads.filter(status=status_filter)

    q = request.GET.get("q", "").strip()
    location = request.GET.get("location", "").strip()
    price_from = request.GET.get("price_from", "").strip()
    price_to = request.GET.get("price_to", "").strip()

    if q:
        ads = ads.filter(
            Q(title__icontains=q) | Q(description__icontains=q)
        )

    if location:
        ads = ads.filter(location__icontains=location)

    if price_from:
        ads = ads.filter(price__gte=price_from)

    if price_to:
        ads = ads.filter(price__lte=price_to)

    return render(
        request,
        "ads/my_ads.html",
        {
            "ads": ads,
            "q": q,
            "location": location,
            "price_from": price_from,
            "price_to": price_to,
            "status_filter": status_filter,
        },
    )


@login_required
def archive_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)

    # запрет на архивацию чужих объявлений
    if ad.author != request.user:
        return HttpResponseForbidden("Недостаточно прав для архивации этого объявления")

    # если ещё не архивировано — архивируем
    if ad.status != Ad.Status.ARCHIVED:
        ad.status = Ad.Status.ARCHIVED
        ad.save()

    # после архивации/повторной попытки — всегда редирект в "Мои объявления"
    return redirect("ads:my_ads")


@login_required
def ad_edit(request, pk):
    ad = get_object_or_404(Ad, pk=pk)

    if ad.author != request.user:
        return render(request, "ads/error.html", {
            "message": "Вы не можете редактировать чужие объявления."
        })

    if request.method == "POST":
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            ad = form.save()
            return redirect("ads:detail", pk=ad.pk)
    else:
        form = AdForm(instance=ad)

    return render(request, "ads/ad_edit.html", {"form": form, "ad": ad})


@login_required
def ad_create(request):
    if request.method == "POST":
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.status = Ad.Status.PENDING
            ad.save()
            return redirect("home")
    else:
        form = AdForm()

    return render(request, "ads/ad_create.html", {"form": form})
