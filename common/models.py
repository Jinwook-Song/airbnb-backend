from django.db import models

# Create your models here.


class CommonModel(models.Model):
    """Common model definition, blueprint for other models"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Django dosen't create database about this model
    class Meta:
        abstract = True
