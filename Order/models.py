from django.db import models

class Order(models.Model):
    customer = models.ForeignKey(
        'Customer.Customer',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    tracking_number = models.CharField(max_length=32, unique=True)
    status = models.CharField(max_length=20, choices=[
        ('Created', 'Created'),
        ('Picked', 'Picked'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ], default='Created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    VALID_TRANSITIONS = {
        'Created': ['Picked'],
        'Picked': ['Shipped'],
        'Shipped': ['Delivered'],
        'Delivered': [],
    }  #normal flow for a shipping process (just from my view! but this depends on the company business)
       #notice if you try to change the status from Picked to Delivered, an error will appear!

    def save(self, *args, **kwargs):
        if self._state.adding:  # New order
            super().save(*args, **kwargs)
            from OrderTracking.models import OrderTrackingEvent
            OrderTrackingEvent.objects.create(
                order=self,
                status=self.status,
                comment=f'Order created with status: {self.status}'
            )
        else:
            original_order = Order.objects.get(pk=self.pk)
            if original_order.status != self.status:
                if self.status not in self.VALID_TRANSITIONS.get(original_order.status, []):
                    raise ValueError(f'Invalid status transition from {original_order.status} to {self.status}')
                super().save(*args, **kwargs)
                from OrderTracking.models import OrderTrackingEvent
                OrderTrackingEvent.objects.create(
                    order=self,
                    status=self.status,
                    comment=f'Order status changed from {original_order.status} to {self.status}'
                )
            else:
                super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.tracking_number} - {self.customer.name}"

