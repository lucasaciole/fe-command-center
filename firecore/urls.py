from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('characters', views.CharacterListView.as_view(), name='character_changelist'),
    path('characters/add/', views.CharacterCreateView.as_view(), name='character_add'),
    path('characters/<int:pk>/', views.CharacterUpdateView.as_view(), name='character_change'),
    path('characters/delete/<int:pk>', views.CharacterDeleteView.as_view(), name='character_delete'),
    path('ajax/load-classes/', views.load_classes, name='ajax_load_classes')
]