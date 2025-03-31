from django.db import models
from djongo import models


# Create your models here.
class Tokens(models.Model):
    _id = models.ObjectIdField()
    id = models.PositiveIntegerField(default=0, blank=False)
    user_id = models.CharField(max_length=50)
    token = models.CharField(max_length=50)
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["user_id"]
