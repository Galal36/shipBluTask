from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "user", "name", "phone"]
        read_only_fields = ["user"]

    def validate(self, data):
        """
        Check that a customer with the same name and phone doesn't already exist.
        """
        name = data.get('name')
        phone = data.get('phone')
        
        # Check if we're updating an existing customer
        instance = getattr(self, 'instance', None)
        
        # For new customers or when name/phone is being changed
        if not instance or instance.name != name or instance.phone != phone:
            existing_customer = Customer.objects.filter(name=name, phone=phone).first()
            if existing_customer:
                raise serializers.ValidationError({
                    'detail': f'A customer with name "{name}" and phone "{phone}" already exists. '
                             f'Please use a different name or phone number.'
                })
        
        return data
