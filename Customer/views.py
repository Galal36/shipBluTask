from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from permissions import IsAdminOrReadOnly

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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
