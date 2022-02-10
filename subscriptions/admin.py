from my_admin.admin import admin_site

from .models import Plan, UserSubscription, SubscriptionTransaction
# Register your models here.
admin_site.register(Plan)
admin_site.register(UserSubscription)
admin_site.register(SubscriptionTransaction)