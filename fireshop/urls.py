from django.urls import path

from . import views

urlpatterns = [
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/new', views.EventCreateView.as_view(), name='event_add'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/<int:pk>/update', views.EventUpdateView.as_view(), name='event_update'),
    path('events/<int:pk>/attendance', views.EventAttendanceListView.as_view(), name='event_attendance_list'),
    path('events/<int:eid>/attendance/add', views.EventAttendanceCategoryCreateView.as_view(),
        name='event_attendance_category_add'),
    path('events/<int:event>/attendance/confirm',
        views.EventAttendanceConfirmationView.as_view(), name='event_attendance_confirm'),
    path('events/<int:pk>/attendance/<str:typ>', views.EventAttendanceCreateView.as_view(), name='event_attendance_add'),
    path('events/<int:pk>/planner/', views.PartyPlanningView.as_view(), name='party_planner'),
    path('shop/', views.ShopListView.as_view(), name='shop_item_list'),
    path('shop/points/new', views.PlayerPointsCreateView.as_view(), name='player_points_create'),
    path('shop/points/history', views.PlayerPointsHistoryListView.as_view(), name='player_points_history_list'),
    path('shop/<int:pk>/redeem', views.ShopItemRedeemView.as_view(), name='shop_item_redeem'),
    path('shop/items/new', views.ShopItemCreateView.as_view(), name='shop_item_create'),
    path('shop/items/<int:pk>', views.ShopItemUpdateView.as_view(), name='shop_item_update'),
]