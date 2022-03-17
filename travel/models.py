# -*- coding: utf-8 -*-
import datetime

from cities.models import Country, City, Region, PostalCode
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils.timezone import utc
from django.contrib.auth.models import AbstractUser
from django.db.models import signals as signals
from django.utils.translation import ugettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from django.db.models.signals import post_save
from pinax.stripe.actions import customers
from post_office import mail


from .utils import str_trunc, PathAndRename, ModelDiffMixin

__all__ = ['User']

AbstractUser._meta.get_field('username').max_length = 256
AbstractUser._meta.get_field('first_name').max_length = 256
AbstractUser._meta.get_field('last_name').max_length = 256
AbstractUser._meta.get_field('email').max_length = 256

def create_admin_user(app_config, **kwargs):
    if app_config.name != 'module':
        return None

    try:
        User.objects.get(username='admin')
    except User.DoesNotExist:
        print('Creating admin user: login: admin, password: 123')
        assert User.objects.create_superuser('admin', 'admin@localhost', '123')
    else:
        print('Admin user already exists')


signals.post_migrate.connect(create_admin_user)


# Abstract

class TimeStampedModel(models.Model):
    date_added = models.DateTimeField(auto_now_add=True, db_index=True)
    date_updated = models.DateTimeField(auto_now=True, db_index=True)

    class Meta(object):
        abstract = True


class OrderedModel(models.Model):
    order = models.PositiveIntegerField(default=0)

    class Meta(object):
        abstract = True
        ordering = ['order']


# User

class User(AbstractUser):
    phone = models.CharField(max_length=16, default='', blank=True)


class Warehouse(TimeStampedModel):
    country = models.ForeignKey(Country)
    region = models.ForeignKey(Region)
    city = models.ForeignKey(City)

    @classmethod
    def get_available_countries(self):
        ids = Warehouse.objects.all().values_list('country__pk', flat=True).distinct()
        return Country.objects.filter(pk__in=ids).order_by('name')

    @classmethod
    def get_available_regions(self, country_id):
        ids = Warehouse.objects.filter(country__id=country_id).values_list('region__pk', flat=True).distinct()
        return Region.objects.filter(pk__in=ids).order_by('name')

    @classmethod
    def get_available_city(self, region_id):
        ids = Warehouse.objects.filter(region__id=region_id).values_list('city__pk', flat=True).distinct()
        return City.objects.filter(pk__in=ids).order_by('name')

    def __str__(self):
        return "%s %s %s" % (self.country, self.region, self.city)


class LuggageClass(TimeStampedModel, OrderedModel, TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=256),
        short_title=models.CharField(max_length=256)
    )

    def __str__(self):
        return self.title


class LuggageSize(TimeStampedModel, OrderedModel, TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=256),
        short_title=models.CharField(max_length=256)
    )

    def __str__(self):
        return self.title


class LuggageWheels(TimeStampedModel, OrderedModel, TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=256),
        short_title=models.CharField(max_length=256)
    )

    def __str__(self):
        return self.title


class Luggage(TimeStampedModel, TranslatableModel):
    warehouse = models.ForeignKey('Warehouse', null=True)
    title = models.CharField(max_length=256)
    full_price = models.FloatField()
    day_price = models.FloatField()
    cnt = models.PositiveIntegerField(default=0)
    luggage_wheels = models.ForeignKey('LuggageWheels', blank=True, null=True)
    luggage_size = models.ForeignKey('LuggageSize', blank=True, null=True)
    luggage_class = models.ForeignKey('LuggageClass', blank=True, null=True)
    translations = TranslatedFields(
        details=models.TextField(),
        features=models.TextField()
    )

    @property
    def get_features(self):
        res = self.features.split("\n")
        return "<ul class=\"features\">%s</ul>" % "".join(map(lambda x: "<li>%s</li>"%x, res))

    def __str__(self):
        return self.title


class LuggagePhoto(TimeStampedModel):
    luggage = models.ForeignKey(Luggage, related_name='photos')
    photo = models.ImageField(upload_to=PathAndRename('luggage'))


class Address(TimeStampedModel):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=256)
    country = models.ForeignKey(Country)
    region = models.ForeignKey(Region)
    code = models.CharField(max_length=12)
    city = models.ForeignKey(City)
    street = models.CharField(max_length=256)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s" % (self.user, self.title)


class Order(TimeStampedModel, ModelDiffMixin):
    invoice = models.ForeignKey('Invoice')
    user = models.ForeignKey(User)
    luggage = models.ForeignKey(Luggage)
    is_returned = models.BooleanField(default=False)
    total = models.FloatField()
    scheduled_return_time = models.ForeignKey('ReturnTime', null=True, blank=True, )
    date_start = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)
    address = models.ForeignKey(Address)

    def notify_return(self):
        context = {
            "user": self.user,
            "order": self
        }

        mail.send([self.user.email], settings.DEFAULT_FROM_EMAIL, template='return_order', context=context)

    def send_remind_email(self):
        context = {
            "user": self.user,
            "order": self
        }

        mail.send([self.user.email], settings.DEFAULT_FROM_EMAIL, template='remind_return', context=context)

    def save(self, *args, **kwargs):
        if self.pk and 'is_returned' in self.changed_fields and self.is_returned:
            self.notify_return()

        return super(Order, self).save(*args, **kwargs)

    @classmethod
    def send_email(self, user, orders):
        address = None
        if len(orders):
            a = orders[0].address
            address = "%s, %s %s, %s %s" % (a.title, a.city.name, a.street, a.region.name, a.country.code)

        context = {
            "user": user,
            "orders": orders,
            "address": address
        }

        mail.send([user.email], settings.DEFAULT_FROM_EMAIL, template='new_order_user', context=context)
        to_emails = [user.email for user in User.objects.filter(is_staff=True).exclude(email="admin@example.com")]
        if to_emails:
            mail.send([to_emails], settings.DEFAULT_FROM_EMAIL, template='new_order_admin', context=context)


    @property
    def duedate(self):
        return self.date_end

    @property
    def duedays(self):
        timediff = self.duedate - datetime.datetime.utcnow().replace(tzinfo=utc)
        return timediff.days

    @property
    def expired(self):
        timediff = datetime.datetime.utcnow().replace(tzinfo=utc) - self.date_end
        if timediff.days >0:
            return timediff.days

        return 0

    def __str__(self):
        return "%s %s" % (self.user, self.luggage)


class ReturnTime(TimeStampedModel):
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class Invoice(models.Model):
    number = models.CharField(max_length=64, default="")
    user = models.ForeignKey(User)
    amount = models.FloatField()
    comments = models.TextField()
    invoice_date = models.DateTimeField()
    is_paid = models.BooleanField(default=False)

    def pay(self):
        if self.is_paid:
            return
        if self.amount:
            stripe.actions.customers.sync_customer(self.user.customer)
            stripe.actions.charges.create(
                description="Luggary Invoice: {}".format(self.number),
                amount=decimal.Decimal(self.amount),
                customer=self.user.customer
            )
        self.is_paid = True
        self.save()

    def send_remind_email(self):
        context = {
            "user": self.user,
            "invoice": self
        }

        mail.send([self.user.email], settings.DEFAULT_FROM_EMAIL, template='remind_invoice', context=context)

    def __str__(self):
        return "%s" % self.number


def create_stripe_user(sender, instance, **kwargs):
    if kwargs['created']:
        customers.create(user=instance)


def create_invoice_number(sender, instance, **kwargs):
    if kwargs['created']:
        instance.number = "INV-%010X" % instance.pk
        instance.save()


class Coupon(TimeStampedModel):
    code = models.CharField(max_length=256, unique=True)
    min_days = models.IntegerField(null=True, blank=True)
    min_total = models.IntegerField(null=True, blank=True)
    discount = models.FloatField(default=0, blank=True, help_text="Percentage of discount (e.g. 15)")
    free_days = models.IntegerField(default=0, blank=True)
    expire = models.DateTimeField()

    def clean(self):
        if not self.discount and not self.free_days:
            raise ValidationError("Please enter discount or free_days")
        return super(Coupon, self).clean()

    def __str__(self):
        return "%s" % self.code


models.signals.post_save.connect(create_invoice_number, sender=Invoice)
models.signals.post_save.connect(create_stripe_user, sender=User)
