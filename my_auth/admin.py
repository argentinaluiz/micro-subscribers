from my_admin.admin import admin_site
from .models import Group, Permission, User
# Register your models here.

admin_site.register(User)
admin_site.register(Group)
admin_site.register(Permission)
