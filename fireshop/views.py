from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Event, ShopItem, ShopItemRedeem

# Create your views here.
class EventListView(LoginRequiredMixin, ListView):
	model = Event
	context_object_name = "events"

class EventCreateView(LoginRequiredMixin, CreateView):
	model = Event

class EventUpdateView(LoginRequiredMixin, UpdateView):
	model = Event

# Create your views here.
class ShopListView(LoginRequiredMixin, ListView):
	model = ShopItem
	context_object_name = "shop_items"

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