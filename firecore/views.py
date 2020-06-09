from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Class, ClassTree, Character
from .forms import CharacterForm


# Create your views here.
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

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

def load_classes(request):
    tree_id = request.GET.get('class_tree')
    classes = Class.objects.filter(class_tree_id=tree_id).order_by('name')
    return render(request, 'firecore/classes_dropdown_list_options.html', {'classes': classes})