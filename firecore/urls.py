from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('characters', views.CharacterListView.as_view(), name='character_changelist'),
    path('characters/add/', views.CharacterCreateView.as_view(), name='character_add'),
    path('characters/<int:pk>/', views.CharacterUpdateView.as_view(), name='character_change'),
    path('characters/delete/<int:pk>', views.CharacterDeleteView.as_view(), name='character_delete'),
    path('shops', views.PlayerShopListView.as_view(), name='playershop_list'),
    path('shops/add/', views.PlayerShopCreateView.as_view(), name='playershop_add'),
    path('shops/<int:pk>/', views.PlayerShopUpdateView.as_view(), name='playershop_change'),
    path('shops/delete/<int:pk>', views.PlayerShopDeleteView.as_view(), name='playershop_delete'),
    path('ajax/load-classes/', views.load_classes, name='ajax_load_classes')
]