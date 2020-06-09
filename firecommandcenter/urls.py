from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.CharacterListView.as_view(), name='character_changelist'),
    path('add/', views.CharacterCreateView.as_view(), name='character_add'),
    path('<int:pk>/', views.CharacterUpdateView.as_view(), name='character_change'),

    path('ajax/load-classes/', views.load_classes, name='ajax_load_classes')
]