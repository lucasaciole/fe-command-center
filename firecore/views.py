from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Class, ClassTree, Character, PlayerShop
from .forms import CharacterForm, PlayerShopForm


# Create your views here.
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curr_player_points = self.request.user.playerpoints_set.first()
        if curr_player_points is None:
            context['points'] = 0
        else:
            context['points'] = curr_player_points.ammount
        return context


class CharacterListView(LoginRequiredMixin, ListView):
    model = Character
    context_object_name = 'characters'

    def get_queryset(self):
        return Character.objects.filter(user_id=self.request.user.id).order_by('name')

class CharacterCreateView(LoginRequiredMixin, CreateView):
    model = Character
    form_class = CharacterForm
    success_url = reverse_lazy('character_changelist')

    def get_form_kwargs(self):
        kwargs = super(CharacterCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

class CharacterUpdateView(LoginRequiredMixin, UpdateView):
    model = Character
    form_class = CharacterForm
    success_url = reverse_lazy('character_changelist')

    def get_form_kwargs(self):
        kwargs = super(CharacterUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

class CharacterDeleteView(LoginRequiredMixin, DeleteView):
    model = Character
    success_url = reverse_lazy('character_changelist')

class PlayerShopListView(LoginRequiredMixin, ListView):
    model = PlayerShop
    context_object_name = 'shops'

    def get_queryset(self):
        return PlayerShop.objects.filter(user_id=self.request.user.id).order_by('shop_name')

class PlayerShopCreateView(LoginRequiredMixin, CreateView):
    model = PlayerShop
    form_class = PlayerShopForm
    success_url = reverse_lazy('playershop_list')

    def get_form_kwargs(self):
        kwargs = super(PlayerShopCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

class PlayerShopUpdateView(LoginRequiredMixin, UpdateView):
    model = PlayerShop
    form_class = PlayerShopForm
    success_url = reverse_lazy('playershop_list')

    def get_form_kwargs(self):
        kwargs = super(PlayerShopUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

class PlayerShopDeleteView(LoginRequiredMixin, DeleteView):
    model = PlayerShop
    success_url = reverse_lazy('playershop_list')

def load_classes(request):
    tree_id = request.GET.get('class_tree')
    classes = Class.objects.filter(class_tree_id=tree_id).order_by('name')
    return render(request, 'firecore/classes_dropdown_list_options.html', {'classes': classes})
