
# Create your models here.
from django.db import models
from shared.models import AutoCreatedUpdatedMixin, UUIDMixin
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class Plan(UUIDMixin, AutoCreatedUpdatedMixin):
    name = models.CharField(max_length=255)


class PlanCost(UUIDMixin, AutoCreatedUpdatedMixin):
    ANNUALLY = 'annually'
    SEMIANNUALLY = 'semiannually'
    PERIOD_CHOICES = [
        (SEMIANNUALLY, 'Semiannually'),
        (ANNUALLY, 'Annually'),
    ]
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[
                                MinValueValidator(0)],)
    recurrence_period = models.CharField(
        choices=PERIOD_CHOICES,
        max_length=30
    )
    plan = models.ForeignKey(
        Plan,
        help_text=_('the subscription plan for these cost details'),
        on_delete=models.CASCADE,
        related_name='costs',
    )


class UserSubscription(UUIDMixin, AutoCreatedUpdatedMixin):
    user = models.ForeignKey(
        get_user_model(),
        help_text=_('the user this subscription applies to'),
        null=True,
        on_delete=models.PROTECT,
        related_name='subscriptions',
    )
    plan = models.ForeignKey(
        PlanCost,
        help_text=_('the plan costs and billing frequency for this user'),
        null=True,
        on_delete=models.PROTECT,
        related_name='subscriptions'
    )
    ends_at = models.DateTimeField(
        blank=True,
        help_text=_('the date to finish billing this subscription'),
        null=True,
        verbose_name='billing start end',
    )
    date_billing_last = models.DateTimeField(
        blank=True,
        help_text=_('the last date this plan was billed'),
        null=True,
        verbose_name='last billing date',
    )
    active = models.BooleanField(
        default=True,
        help_text=_('whether this subscription is active or not'),
    )
    cancelled = models.BooleanField(
        default=False,
        help_text=_('whether this subscription is cancelled or not'),
    )


class SubscriptionTransaction(UUIDMixin, AutoCreatedUpdatedMixin):
    user = models.ForeignKey(
        get_user_model(),
        help_text=_('the user this subscription applies to'),
        null=True,
        on_delete=models.PROTECT,
        related_name='transactions',
    )
    plan_cost = models.ForeignKey(
        PlanCost,
        help_text=_('the plan costs that were billed'),
        null=True,
        on_delete=models.SET_NULL,
        related_name='transactions'
    )
    date_payment = models.DateTimeField(
        help_text=_('the datetime the transaction was billed'),
        verbose_name='transaction date',
    )
    amount = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text=_('how much was billed for the user'),
        validators=[MinValueValidator(0)]
    )
