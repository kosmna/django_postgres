# -*- coding: utf-8 -*-
from django.contrib.admin.options import ModelAdmin, StackedInline
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib import admin
from django import forms
from reversion.admin import VersionAdmin
from parler.admin import TranslatableAdmin

from .models import (User, LuggageClass, LuggageSize, LuggageWheels, Luggage,
                     LuggagePhoto, Address, Order, ReturnTime, Coupon,
                     Warehouse, Invoice)

@admin.register(User)
class UserAdmin(VersionAdmin, UserAdmin):
    pass


class OrderedAdmin(ModelAdmin):
    # mandatory display & editable 'order' field
    list_display = ('order',)
    list_editable = ('order',)
    ordering = ('order',)

    class Media:
        js = ['/static/js/admin_list_reorder.js', ]




class LuggageClassAdmin(OrderedAdmin, TranslatableAdmin):
    list_display = (u'id', 'title', 'order', 'date_added', 'date_updated')
    list_filter = ('date_added', 'date_updated')
admin.site.register(LuggageClass, LuggageClassAdmin)


class LuggageSizeAdmin(OrderedAdmin, TranslatableAdmin):
    list_display = (u'id', 'title', 'order', 'date_added', 'date_updated')
    list_filter = ('date_added', 'date_updated')
admin.site.register(LuggageSize, LuggageSizeAdmin)


class LuggageWheelsAdmin(OrderedAdmin, TranslatableAdmin):
    list_display = (u'id', 'title', 'order', 'date_added', 'date_updated')
    list_filter = ('date_added', 'date_updated')
admin.site.register(LuggageWheels, LuggageWheelsAdmin)


class LuggagePhotoInlineAdmin(admin.TabularInline):
    model = LuggagePhoto
    extra = 1


class LuggageAdmin(TranslatableAdmin):
    list_display = (
        u'id',
        'title',
        'full_price',
        'day_price',
        'cnt',
        'luggage_wheels',
        'luggage_size',
        'luggage_class',
        'details',
        'features',
        'date_added',
        'date_updated',
    )
    list_filter = (
        'luggage_wheels',
        'luggage_size',
        'luggage_class',
        'date_added',
        'date_updated',
    )
    inlines = [LuggagePhotoInlineAdmin, ]
admin.site.register(Luggage, LuggageAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'user',
        'title',
        'country',
        'region',
        'code',
        'city',
        'street',
        'date_added',
        'date_updated',
    )
    list_filter = (
        'user',
        'date_added',
        'date_updated',
    )
admin.site.register(Address, AddressAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'user',
        'luggage',
        'is_returned',
        'total',
        'scheduled_return_time',
        'date_added',
        'date_updated',
    )
    list_filter = (
        'date_added',
        'date_updated',
        'user',
        'luggage',
        'is_returned',
        'scheduled_return_time',
    )
admin.site.register(Order, OrderAdmin)


class ReturnTimeAdmin(admin.ModelAdmin):
    list_display = (u'id', 'title', 'date_added', 'date_updated')
    list_filter = ('date_added', 'date_updated')
admin.site.register(ReturnTime, ReturnTimeAdmin)


class WarehouseAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'country',
        'region',
        'city',
        'date_added',
        'date_updated',
    )
    list_filter = ('date_added', 'date_updated',)
admin.site.register(Warehouse, WarehouseAdmin)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'number',
        'user',
        'amount',
        'comments',
        'invoice_date',
        'is_paid',
    )
    list_filter = ('user', 'invoice_date', 'is_paid')
admin.site.register(Invoice, InvoiceAdmin)


class CouponAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'date_added',
        'date_updated',
        'code',
        'min_days',
        'min_total',
        'discount',
        'free_days',
        'expire',
    )
    list_filter = ('date_added', 'date_updated', 'expire')
admin.site.register(Coupon, CouponAdmin)

StackedInline.sortable_field_name = ''  # fix for grapelli sortable_field_name error
admin.TabularInline.sortable_field_name = ''  # fix for grapelli sortable_field_name error
