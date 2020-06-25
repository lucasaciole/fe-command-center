from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, View, DetailView
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Event, ShopItem, ShopItemRedeem, EventAttendanceCategory, PlayerPoints
from .models import EventAttendance, EventAttendanceConfirmation, AttendanceTypes
from .forms import EventForm


# Create your views here.
class EventListView(LoginRequiredMixin, ListView):
    model = Event
    context_object_name = "events"
    ordering = ['date']

class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = context['event']
        context['going'] = event.attendances.filter(attendance_type='going').only('user').order_by('creation_date')
        context['maybe'] = event.attendances.filter(attendance_type='maybe').only('user').order_by('creation_date')
        context['notgoing'] = event.attendances.filter(attendance_type='notgoing').only('user').order_by('creation_date')
        context['unanswered'] = User.objects.exclude(user_attendances__event_id=event.id)
        return context

class EventPlannerView(LoginRequiredMixin, TemplateView):
    template_name = 'fireshop/party_planning.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context

class EventAttendanceConfirmationCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        new_attendance = EventAttendanceConfirmation()
        new_attendance.user = User.objects.get(pk=kwargs['user'])
        new_attendance.event = Event.objects.get(pk=kwargs['event'])
        new_attendance.attendance_category = EventAttendanceCategory.objects.get(pk=kwargs['ac'])
        new_attendance.save()

        return redirect('event_list')


class EventAttendanceListView(LoginRequiredMixin, TemplateView):
    template_name = 'fireshop/event_attendance_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = Event.objects.get(id=kwargs['pk'])
        context['event'] = event
        context['going'] = event.attendances.filter(attendance_type='going').only('user').order_by('creation_date')
        context['maybe'] = event.attendances.filter(attendance_type='maybe').only('user').order_by('creation_date')
        context['notgoing'] = event.attendances.filter(attendance_type='notgoing').only('user').order_by('creation_date')
        context['unanswered'] = User.objects.exclude(user_attendances__event_id=event.id)
        context['attendance_categories'] = event.attendance_categories.all()
        context['colspan'] = 2 + context['attendance_categories'].count()
        return context

class EventAttendanceCategoryCreateView(LoginRequiredMixin, CreateView):
    template_name = 'fireshop/event_attendance_category_form.html'
    model = EventAttendanceCategory
    fields = '__all__'

    def dispatch(self, request, *args, **kwargs):
        self.event = Event.objects.get(id=kwargs.get('eid'))
        return super(EventAttendanceCategoryCreateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('event_detail', kwargs={'pk' : self.object.event.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.event
        return context

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm

    def get_success_url(self):
        return reverse('event_detail', kwargs={'pk' : self.object.pk})

class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    success_url = reverse_lazy('event_list')

class EventAttendanceCreateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        new_attendance = EventAttendance(user=request.user)
        new_attendance.event = Event.objects.get(pk=kwargs['pk'])
        new_attendance.attendance_type = AttendanceTypes[kwargs['typ'].upper()]
        new_attendance.save()
        redirect
        return HttpResponse("DONE")

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

class PlayerPointsCreateView(LoginRequiredMixin, CreateView):
    model = PlayerPoints
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
