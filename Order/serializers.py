from rest_framework import serializers
from .models import Order
from Customer.models import Customer

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    # created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    # updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Order
        fields = ["id", "tracking_number", "customer", "status", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]

    def validate_tracking_number(self, value):
        # Only validate uniqueness for new orders or if tracking number is being changed
        instance = getattr(self, 'instance', None)
        if instance and instance.tracking_number != value:
            if Order.objects.filter(tracking_number=value).exists():
                raise serializers.ValidationError('This tracking number already exists.')
        elif not instance and Order.objects.filter(tracking_number=value).exists():
            raise serializers.ValidationError('This tracking number already exists.')
        return value
    
    def to_representation(self, instance):
                # Get the default representation
        ret = super().to_representation(instance)
        
        # Format created_at and updated_at for user-friendly display
        if instance.created_at:
            ret["created_at"] = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
        if instance.updated_at:
            ret["updated_at"] = instance.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            
        return ret

