import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class PointOfInterest(models.Model):

    def coordinates_default():
        return {
            "lat": "",
            "long": ""
        }

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    external_id = models.CharField(blank=False, null=False, max_length=36)
    name = models.CharField(blank=False, null=False, max_length=250)
    description = models.TextField(blank=True, null=True)
    coordinates = models.JSONField(default=coordinates_default)
    category = models.CharField(blank=False, null=False, max_length=250)
    rating = ArrayField(models.CharField(max_length=5))

    def __str__(self):
        return self.name