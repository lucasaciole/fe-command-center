from .models import EventAttendance, AttendanceTypes, EventAttendanceConfirmation, PlayerPointsHistory
from .models import Event, ShopItem, ShopItemRedeem, EventAttendanceCategory, PlayerPoints
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from .forms import EventForm
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)

# Create your views here.
class EventListView(LoginRequiredMixin, ListView):
    model = Event
    context_object_name = "events"
    ordering = ['date']

    def get_queryset(self, **kwargs):
        if not self.request.GET.get('show_all'):
            return Event.objects.filter(date__gte=datetime.now())
        else:
            return Event.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_going'] = Event.objects.filter(attendances__user_id=self.request.user.id, attendances__attendance_type='going')
        context['user_maybe'] = Event.objects.filter(attendances__user_id=self.request.user.id, attendances__attendance_type='maybe')
        context['user_not_going'] = Event.objects.filter(attendances__user_id=self.request.user.id, attendances__attendance_type='notgoing')
        return context

class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = context['event']
        context['going'] = event.attendances.filter(attendance_type='going').only('user').order_by('-creation_date')
        context['maybe'] = event.attendances.filter(attendance_type='maybe').only('user').order_by('-creation_date')
        context['notgoing'] = event.attendances.filter(attendance_type='notgoing').only('user').order_by('-creation_date')
        context['unanswered'] = User.objects.exclude(user_attendances__event_id=event.id)
        return context

class EventPlannerView(LoginRequiredMixin, TemplateView):
    template_name = 'fireshop/party_planning.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context

class EventAttendanceConfirmationView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        attendances = json.loads(request.POST['attendances'])
        event_id = kwargs['event']
        event = Event.objects.get(pk=event_id)
        for member, category in attendances.items():
            user = User.objects.get(pk=member)
            try:
                eac = EventAttendanceConfirmation.objects.get(user=user, event=event)
            except EventAttendanceConfirmation.DoesNotExist:
                eac = EventAttendanceConfirmation(user=user, event=event)
                eac.attendance_category = event.attendance_categories.get(id=category)
                eac.save()
            except Exception as error:
                raise error
        messages.info(request, "Presenças confirmadas com sucesso!")
        return redirect('event_attendance_list', pk=event.id)

class PlayerPointsHistoryListView(LoginRequiredMixin, ListView):
    model = PlayerPointsHistory
    template_name = 'fireshop/player_points_history_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if hasattr(self.request.user, 'shop_points'):
            context['points'] = self.request.user.shop_points.amount
        else:
            context['points'] = 0

        if not self.request.user.is_staff:
            context['history'] = PlayerPointsHistory.objects.filter(user=self.request.user).order_by('-creation_date')
        else:
            context['history'] = PlayerPointsHistory.objects.all().order_by('-creation_date')

        return context


class EventAttendanceListView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'fireshop/event_attendance_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        context['event'] = event
        context['going'] = event.attendances.filter(attendance_type='going').only('user').order_by('creation_date')
        context['maybe'] = event.attendances.filter(attendance_type='maybe').only('user').order_by('creation_date')
        context['notgoing'] = event.attendances.filter(attendance_type='notgoing').only('user').order_by('creation_date')
        context['unanswered'] = User.objects.exclude(user_attendances__event_id=event.id)
        context['attendance_categories'] = event.attendance_categories.all()
        context['colspan'] = 2 + context['attendance_categories'].count()
        context['confirmed'] = event.attendance_confirmations.all()
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
        event = Event.objects.get(pk=kwargs['pk'])
        try:
            ea = EventAttendance.objects.get(user=request.user, event=event)
            if ea.attendance_type != kwargs['typ']:
                old_attendance = AttendanceTypes[ea.attendance_type.upper()]
                ea.attendance_type = AttendanceTypes[kwargs['typ'].upper()]
                ea.save()
                messages.success(request, 'Sua sinalização no "{}" foi atualizada de "{}" para "{}"!'.format(ea.event,
                    old_attendance.label, ea.get_attendance_type_label()))
            else:
                messages.warning(request, 'Você já sinalizou "{}" para o evento "{}"'.format(
                        ea.get_attendance_type_label(), ea.event
                    ))
            return redirect('event_list')
        except EventAttendance.DoesNotExist:
            new_attendance = EventAttendance(user=request.user)
            new_attendance.event = event
            new_attendance.attendance_type = AttendanceTypes[kwargs['typ'].upper()]
            new_attendance.save()
            messages.info(request, 'Obrigado por sinalizar "{}" para o evento "{}"!'.format(new_attendance.get_attendance_type_label(), new_attendance.event))
            return redirect('event_list')

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

class ShopItemRedeemView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        item = ShopItem.objects.get(pk=kwargs['pk'])
        messages.info(request, 'Você requisitou "{}"'.format(item))
        return redirect('shop_item_list')


class PartyPlanningView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'fireshop/party_planning.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        context['event'] = event
        context['going'] = event.attendances.filter(attendance_type='going').only('user').order_by('creation_date')
        context['maybe'] = event.attendances.filter(attendance_type='maybe').only('user').order_by('creation_date')
        context['notgoing'] = event.attendances.filter(attendance_type='notgoing').only('user').order_by('creation_date')
        context['unanswered'] = User.objects.exclude(user_attendances__event_id=event.id)
        return context
