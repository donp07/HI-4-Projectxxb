from django.db import models

class GlucoseReading(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    reading = models.DecimalField(max_digits=5, decimal_places=2)
    date_time = models.DateTimeField()

