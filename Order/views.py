from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Order
from .serializers import OrderSerializer
from Customer.models import Customer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.shortcuts import get_object_or_404
from permissions import IsAdminOrReadOnly # Import the custom permission

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow adminJalal or staff users to access.
    (Kept for reference, but IsAdminOrReadOnly is now used)
    """
    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.username == 'adminJalal')

class IsAdminOrOrderOwner(permissions.BasePermission):
    """
    Custom permission to allow admin users full access and regular users access to their own orders.
    (Kept for reference, but IsAdminOrReadOnly is now used for write operations)
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.username == 'adminJalal':
            return True
        # For read operations, allow owner. For write, IsAdminOrReadOnly will deny non-admins.
        return obj.customer.user == request.user

class OrderPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all().select_related('customer')
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly] # Changed
    pagination_class = OrderPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'customer__name']
    search_fields = ['tracking_number', 'customer__name']
    ordering_fields = ['created_at', 'status', 'tracking_number']
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        qs = super().get_queryset()
        # Normal users only see their own orders
        if not (self.request.user.is_staff or self.request.user.username == 'adminJalal'):
            qs = qs.filter(customer__user=self.request.user)
        return qs

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly] # Changed
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

class OrderStatusUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly] # Changed
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        new_status = request.data.get('status')
        
        if not new_status:
            return Response({'error': 'Status is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Validate status transition
            if new_status not in order.VALID_TRANSITIONS.get(order.status, []):
                return Response({
                    'error': f'Invalid status transition from {order.status} to {new_status}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            order.status = new_status
            order.save()
            
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
