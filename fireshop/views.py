from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Event, ShopItem, ShopItemRedeem
from .forms import EventForm

# Create your views here.
class EventListView(LoginRequiredMixin, ListView):
    model = Event
    context_object_name = "events"
    ordering = ['date']

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    success_url = reverse_lazy('event_list')

class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    success_url = reverse_lazy('event_list')

# Create your views here.
class ShopListView(LoginRequiredMixin, ListView):
    model = ShopItem
    context_object_name = "shop_items"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'shop_points'):
            context['points'] = self.request.user.shop_points.amount
        else:
            context['points'] = 0

        return context

class ShopItemCreateView(LoginRequiredMixin, CreateView):
    model = ShopItem
    fields = '__all__'
    success_url = reverse_lazy('shop_item_list')

class ShopItemUpdateView(LoginRequiredMixin, UpdateView):
    model = ShopItem
    fields = '__all__'
    success_url = reverse_lazy('shop_item_list')

class ShopItemRedeemView(LoginRequiredMixin, CreateView):
    model = ShopItemRedeem
    success_url = reverse_lazy('shop_item_list')

class PartyPlanningView(LoginRequiredMixin, TemplateView):
    template_name = 'fireshop/party_planning.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context
