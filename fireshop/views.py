from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, View, DetailView
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Event, ShopItem, ShopItemRedeem, EventAttendanceCategory, PlayerPoints
from .models import EventAttendance, AttendanceTypes, EventAttendanceConfirmation, PlayerPointsHistory
from .forms import EventForm
from django.contrib import messages
import logging
import pdb
import json

logger = logging.getLogger(__name__)

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

class EventAttendanceConfirmationView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        attendances = json.loads(request.GET['attendances'])
        event_id = kwargs['event']
        for member, category in attendances.items():
            user = User.objects.get(pk=member)
            event = Event.objects.get(pk=event_id)
            try:
                eac = EventAttendanceConfirmation.objects.get(user=user, event=event)
                logger.error("ALREADY EXISTS")
                #return HttpResponse("Presença de {} em {} já foi registrada.".format(user, event), status=200)
            except EventAttendanceConfirmation.DoesNotExist:
                eac = EventAttendanceConfirmation(user=user, event=event)
                eac.attendance_category = event.attendance_categories.get(id=category)
                eac.save()
                logger.error("OK")
                #return HttpResponse("Presença de {} em {} confirmada com sucesso.".format(user, event), status=200)
            except Exception as error:
                raise error
        return HttpResponse("OK", status=200)

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
            context['history'] = PlayerPointsHistory.objects.filter(user=self.request.user)
        else:
            context['history'] = PlayerPointsHistory.objects.all()
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
