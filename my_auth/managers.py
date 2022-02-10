from django.contrib.auth.models import GroupManager as DjangoGroupManager
from django.db import transaction

class GroupManager(DjangoGroupManager):

    def add_with_user(self, user, group_names):
        user_groups = self.filter(user=user)
        groups = self.filter(name__in=group_names)
        print(groups, user_groups, group_names)
        with transaction.atomic():
            for group in groups.difference(user_groups):
                user.groups.add(group)