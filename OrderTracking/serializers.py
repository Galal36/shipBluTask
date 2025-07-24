from rest_framework import serializers
from .models import OrderTrackingEvent

class OrderTrackingEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTrackingEvent
        fields = ["id", "order", "status", "timestamp", "comment"]
        read_only_fields = ["timestamp"]




    def to_representation(self, instance):
        # get the default representation
        ret = super().to_representation(instance)
        
        # to make it user-friendly time format like in serlizer of Order
        if instance.timestamp:
            ret["timestamp"] = instance.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            
        return ret

