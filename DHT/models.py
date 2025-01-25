# Create your models here.
from django.db import models
class Dht11(models.Model):
 temp = models.FloatField(null=True)
 hum = models.FloatField(null=True)
 dt = models.DateTimeField(auto_now_add=True,null=True)
class SensorData(models.Model):
    temp = models.FloatField()  # Temperature
    hum = models.FloatField()   # Humidity
    date = models.DateTimeField(auto_now_add=True)  # Timestamp


from django.db import models
from django.contrib.auth.models import User

class Incident(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    seen = models.BooleanField(default=False)  # Indicates whether the incident has been acknowledged
    seen_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="acknowledged_incidents"
    )  # The user who acknowledged the incident

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Incident at {self.timestamp} - Temp: {self.temperature}°C"
from django.db import models
from django.contrib.auth.models import User

class UserComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    temperature = models.FloatField()
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} at {self.timestamp}"
