from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from permissions import IsAdminOrReadOnly
from rest_framework import generics, permissions, filters  #  filters import
from django_filters.rest_framework import DjangoFilterBackend  
class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow adminJalal or staff users to access.
    """
    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.username == 'adminJalal')

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
             #related filteing and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'phone']  # Enable search by name and phone
    filterset_fields = ['name']  # Enable exact filtering by name
    ordering_fields = ['name', 'phone']  # Enable ordering

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
