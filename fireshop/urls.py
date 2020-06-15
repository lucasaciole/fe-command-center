from django.urls import path

from . import views

urlpatterns = [
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/new', views.EventCreateView.as_view(), name='event_add'),
    path('events/<int:pk>', views.EventUpdateView.as_view(), name='event_update'),
    path('planner/', views.PartyPlanningView.as_view(), name='party_planner'),
    path('shop/', views.ShopListView.as_view(), name='shop_item_list'),
    path('shop/<int:pk>/redeem', views.ShopItemRedeemView.as_view(), name='shop_item_redeem'),
    path('shop/items/new', views.ShopItemCreateView.as_view(), name='shop_item_create'),
    path('shop/items/<int:pk>', views.ShopItemUpdateView.as_view(), name='shop_item_update'),
]