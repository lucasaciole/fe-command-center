from django.urls import path

from . import views

urlpatterns = [
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('shop/', views.ShopListView.as_view(), name='shop_item_list'),
    path('shop/<int:pk>/redeem', views.ShopItemRedeemView.as_view(), name='shop_item_redeem'),
    path('shop/items/new', views.ShopItemCreateView.as_view(), name='shop_item_create'),
    path('shop/items/<int:pk>', views.ShopItemUpdateView.as_view(), name='shop_item_update'),
]