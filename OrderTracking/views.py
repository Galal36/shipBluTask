from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import OrderTrackingEvent
from .serializers import OrderTrackingEventSerializer
from Order.models import Order
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.shortcuts import get_object_or_404
from permissions import IsAdminOrReadOnly # Import the custom permission

class IsAdminOrOrderOwner(permissions.BasePermission):
    """
    Custom permission to allow admin users full access and regular users access to their own order tracking.
    (Kept for reference, but IsAdminOrReadOnly is now used for method permissions)
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.username == 'adminJalal':
            return True
        # For read operations, allow owner. For write, IsAdminOrReadOnly will deny non-admins.
        return obj.order.customer.user == request.user

class OrderTrackingEventListView(generics.ListAPIView):
    serializer_class = OrderTrackingEventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly] # Changed
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        order = get_object_or_404(Order, id=order_id)
        
        # Check if user has permission to view this order's tracking
        # This object-level permission is still needed even with IsAdminOrReadOnly
        if not (self.request.user.is_staff or self.request.user.username == 'adminJalal'):
            if order.customer.user != self.request.user:
                return OrderTrackingEvent.objects.none() # Return empty queryset if not authorized
        
        return OrderTrackingEvent.objects.filter(order=order).order_by('-timestamp')

class OrderTrackingEventDetailView(generics.RetrieveAPIView):
    queryset = OrderTrackingEvent.objects.all()
    serializer_class = OrderTrackingEventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly] # Changed
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
