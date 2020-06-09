from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Class, ClassTree, Character
from .forms import CharacterForm

# Create your views here.
class CharacterListView(ListView):
    model = Character
    context_object_name = 'characters'

class CharacterCreateView(CreateView):
    model = Character
    form_class = CharacterForm
    success_url = reverse_lazy('character_changelist')

class CharacterUpdateView(UpdateView):
    model = Character
    form_class = CharacterForm
    success_url = reverse_lazy('character_changelist')


def load_classes(request):
    tree_id = request.GET.get('class_tree')
    classes = Class.objects.filter(class_tree_id=tree_id).order_by('name')
    return render(request, 'firecommandcenter/classes_dropdown_list_options.html', {'classes': classes})