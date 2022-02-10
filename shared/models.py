from django.db import models
import uuid

# Create your models here.
from django.db import models

class UUIDMixin(models.Model):
     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

     class Meta:
        abstract = True

class AutoCreatedUpdatedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='atualizado em')

    class Meta:
        abstract = True

