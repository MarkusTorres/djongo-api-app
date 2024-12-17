from django.db import models


# Create your models here.
class Tokens(models.Model):
    user_id = models.CharField(max_length=50)
    token = models.CharField(max_length=50)
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["user_id"]
