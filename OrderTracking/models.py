from django.db import models

class OrderTrackingEvent(models.Model):
    order = models.ForeignKey('Order.Order', on_delete=models.CASCADE, related_name='tracking_events')
    status = models.CharField(max_length=20, choices=[
        ('Created', 'Created'),
        ('Picked', 'Picked'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ])
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.comment:
            self.comment = f'Status changed to {self.status}.'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Tracking for Order {self.order.tracking_number} - Status: {self.status}"

    class Meta:
        ordering = ['-timestamp']

