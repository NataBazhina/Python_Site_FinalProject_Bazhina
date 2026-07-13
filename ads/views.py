from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.core.exceptions import PermissionDenied

from .models import Ad
from .forms import AdForm


def ad_list(request):
    ads = Ad.objects.all()
    return render(request, "ads/ad_list.html", {"ads": ads})


def home(request):
    ads = Ad.objects.all()
    return render(request, "ads/home.html", {"ads": ads})


def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    return render(request, "ads/ad_detail.html", {"ad": ad})


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
