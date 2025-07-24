from django.urls import path
from .views import OrderTrackingEventListView, OrderTrackingEventDetailView

urlpatterns = [
    path("<int:order_id>/", OrderTrackingEventListView.as_view(), name="order-tracking-list"),
    path("<int:pk>/detail/", OrderTrackingEventDetailView.as_view(), name="order-tracking-detail"),
]

