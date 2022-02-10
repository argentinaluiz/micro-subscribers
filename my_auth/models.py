from django.db import models
from django.contrib.auth.models import AbstractUser, Group as DjangoGroup, Permission as DjangoPermission
from typing import Dict
from .managers import GroupManager
# Create your models here.

class ResourceAccess:
    data: Dict = {}

    def __init__(self, data) -> None:
        if data:
            self.data = data

    def has_client(self, client_name):
        return client_name in self.data

    def has_client_role(self, client_name, role):
        return role in self.data.get(client_name, {'roles': []}).get('roles', [])
    
    def get_client_roles(self, client_name):
        return self.data.get(client_name, {'roles': []}).get('roles', [])

def empty_resource_access():
    return dict()

class User(AbstractUser):
    id = models.UUIDField(primary_key=True)
    resource_access = models.JSONField(null=True, default=empty_resource_access)

    @property
    def permission(self) -> ResourceAccess:
        return ResourceAccess(self.resource_access)

class Group(DjangoGroup):

    objects = GroupManager()

    class Meta:
        proxy = True
        app_label = 'my_auth'

class Permission(DjangoPermission):

    class Meta:
        proxy = True
        app_label = 'my_auth'