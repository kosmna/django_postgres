#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, glob, re, random, glob

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ["DJANGO_SETTINGS_MODULE"] = "project.settings"

import django
django.setup()

from cities.models import Country, City, Region, PostalCode

from luggage.models import Luggage, LuggageClass, LuggageClassTranslation
from luggage.models import LuggagePhoto, LuggageSize, LuggageSizeTranslation
from luggage.models import LuggageWheels, LuggageWheelsTranslation, Warehouse
import random

def clean_all():
    LuggageWheels.objects.all().delete()
    LuggagePhoto.objects.all().delete()
    LuggageClass.objects.all().delete()
    LuggageSize.objects.all().delete()
    Luggage.objects.all().delete()

def import_dics():
    luggage_luggageclass_1 = LuggageClass()
    luggage_luggageclass_1.order = 2
    luggage_luggageclass_1.save()

    luggage_luggageclass_2 = LuggageClass()
    luggage_luggageclass_2.order = 1
    luggage_luggageclass_2.save()

    luggage_luggageclass_3 = LuggageClass()
    luggage_luggageclass_3.order = 3
    luggage_luggageclass_3.save()

    # Processing model: luggage.models.LuggageSize


    luggage_luggagesize_1 = LuggageSize()
    luggage_luggagesize_1.order = 1
    luggage_luggagesize_1.save()

    luggage_luggagesize_2 = LuggageSize()
    luggage_luggagesize_2.order = 2
    luggage_luggagesize_2.save()

    luggage_luggagesize_3 = LuggageSize()
    luggage_luggagesize_3.order = 3
    luggage_luggagesize_3.save()

    # Processing model: luggage.models.LuggageWheels


    luggage_luggagewheels_1 = LuggageWheels()
    luggage_luggagewheels_1.order = 1
    luggage_luggagewheels_1.save()

    luggage_luggagewheels_2 = LuggageWheels()
    luggage_luggagewheels_2.order = 2
    luggage_luggagewheels_2.save()

    luggage_luggagewheels_3 = LuggageWheels()
    luggage_luggagewheels_3.order = 3
    luggage_luggagewheels_3.save()

    luggage_luggagewheels_4 = LuggageWheels()
    luggage_luggagewheels_4.order = 4
    luggage_luggagewheels_4.save()


    # Processing model: luggage.models.LuggageClassTranslation


    luggage_luggageclass_translation_1 = LuggageClassTranslation()
    luggage_luggageclass_translation_1.language_code = u'en'
    luggage_luggageclass_translation_1.title = u'Premium'
    luggage_luggageclass_translation_1.short_title = u'Premium'
    luggage_luggageclass_translation_1.master = luggage_luggageclass_1
    luggage_luggageclass_translation_1.save()

    luggage_luggageclass_translation_2 = LuggageClassTranslation()
    luggage_luggageclass_translation_2.language_code = u'es'
    luggage_luggageclass_translation_2.title = u'Prima'
    luggage_luggageclass_translation_2.short_title = u'Prima'
    luggage_luggageclass_translation_2.master = luggage_luggageclass_1
    luggage_luggageclass_translation_2.save()

    luggage_luggageclass_translation_3 = LuggageClassTranslation()
    luggage_luggageclass_translation_3.language_code = u'en'
    luggage_luggageclass_translation_3.title = u'B\xe1sico'
    luggage_luggageclass_translation_3.short_title = u'B\xe1sico'
    luggage_luggageclass_translation_3.master = luggage_luggageclass_2
    luggage_luggageclass_translation_3.save()

    luggage_luggageclass_translation_4 = LuggageClassTranslation()
    luggage_luggageclass_translation_4.language_code = u'en'
    luggage_luggageclass_translation_4.title = u'Luxury'
    luggage_luggageclass_translation_4.short_title = u'Luxury'
    luggage_luggageclass_translation_4.master = luggage_luggageclass_3
    luggage_luggageclass_translation_4.save()

    luggage_luggageclass_translation_5 = LuggageClassTranslation()
    luggage_luggageclass_translation_5.language_code = u'es'
    luggage_luggageclass_translation_5.title = u'Lujo'
    luggage_luggageclass_translation_5.short_title = u'Lujo'
    luggage_luggageclass_translation_5.master = luggage_luggageclass_3
    luggage_luggageclass_translation_5.save()

    # Processing model: luggage.models.LuggageSizeTranslation


    luggage_luggagesize_translation_1 = LuggageSizeTranslation()
    luggage_luggagesize_translation_1.language_code = u'en'
    luggage_luggagesize_translation_1.title = u'Carry On'
    luggage_luggagesize_translation_1.short_title = u'Carry On'
    luggage_luggagesize_translation_1.master = luggage_luggagesize_1
    luggage_luggagesize_translation_1.save()

    luggage_luggagesize_translation_2 = LuggageSizeTranslation()
    luggage_luggagesize_translation_2.language_code = u'es'
    luggage_luggagesize_translation_2.title = u'Continua'
    luggage_luggagesize_translation_2.short_title = u'Continua'
    luggage_luggagesize_translation_2.master = luggage_luggagesize_1
    luggage_luggagesize_translation_2.save()

    luggage_luggagesize_translation_3 = LuggageSizeTranslation()
    luggage_luggagesize_translation_3.language_code = u'en'
    luggage_luggagesize_translation_3.title = u'Medium Size'
    luggage_luggagesize_translation_3.short_title = u'Medium Size'
    luggage_luggagesize_translation_3.master = luggage_luggagesize_2
    luggage_luggagesize_translation_3.save()

    luggage_luggagesize_translation_4 = LuggageSizeTranslation()
    luggage_luggagesize_translation_4.language_code = u'es'
    luggage_luggagesize_translation_4.title = u'Talla mediana'
    luggage_luggagesize_translation_4.short_title = u'Talla mediana'
    luggage_luggagesize_translation_4.master = luggage_luggagesize_2
    luggage_luggagesize_translation_4.save()

    luggage_luggagesize_translation_5 = LuggageSizeTranslation()
    luggage_luggagesize_translation_5.language_code = u'es'
    luggage_luggagesize_translation_5.title = u'Talla grande'
    luggage_luggagesize_translation_5.short_title = u'Talla grande'
    luggage_luggagesize_translation_5.master = luggage_luggagesize_3
    luggage_luggagesize_translation_5.save()

    luggage_luggagesize_translation_6 = LuggageSizeTranslation()
    luggage_luggagesize_translation_6.language_code = u'en'
    luggage_luggagesize_translation_6.title = u'Large Size'
    luggage_luggagesize_translation_6.short_title = u'Large Size'
    luggage_luggagesize_translation_6.master = luggage_luggagesize_3
    luggage_luggagesize_translation_6.save()

    # Processing model: luggage.models.LuggageWheelsTranslation


    luggage_luggagewheels_translation_1 = LuggageWheelsTranslation()
    luggage_luggagewheels_translation_1.language_code = u'en'
    luggage_luggagewheels_translation_1.title = u'2 Wheels'
    luggage_luggagewheels_translation_1.short_title = u'2'
    luggage_luggagewheels_translation_1.master = luggage_luggagewheels_1
    luggage_luggagewheels_translation_1.save()

    luggage_luggagewheels_translation_2 = LuggageWheelsTranslation()
    luggage_luggagewheels_translation_2.language_code = u'es'
    luggage_luggagewheels_translation_2.title = u'2 Ruedas'
    luggage_luggagewheels_translation_2.short_title = u'2'
    luggage_luggagewheels_translation_2.master = luggage_luggagewheels_1
    luggage_luggagewheels_translation_2.save()

    luggage_luggagewheels_translation_3 = LuggageWheelsTranslation()
    luggage_luggagewheels_translation_3.language_code = u'en'
    luggage_luggagewheels_translation_3.title = u'4 Wheels'
    luggage_luggagewheels_translation_3.short_title = u'4'
    luggage_luggagewheels_translation_3.master = luggage_luggagewheels_2
    luggage_luggagewheels_translation_3.save()

    luggage_luggagewheels_translation_4 = LuggageWheelsTranslation()
    luggage_luggagewheels_translation_4.language_code = u'es'
    luggage_luggagewheels_translation_4.title = u'4 Ruedas'
    luggage_luggagewheels_translation_4.short_title = u'4'
    luggage_luggagewheels_translation_4.master = luggage_luggagewheels_2
    luggage_luggagewheels_translation_4.save()

    luggage_luggagewheels_translation_5 = LuggageWheelsTranslation()
    luggage_luggagewheels_translation_5.language_code = u'en'
    luggage_luggagewheels_translation_5.title = u'6 Wheels'
    luggage_luggagewheels_translation_5.short_title = u'6'
    luggage_luggagewheels_translation_5.master = luggage_luggagewheels_3
    luggage_luggagewheels_translation_5.save()

    luggage_luggagewheels_translation_6 = LuggageWheelsTranslation()
    luggage_luggagewheels_translation_6.language_code = u'es'
    luggage_luggagewheels_translation_6.title = u'6 Ruedas'
    luggage_luggagewheels_translation_6.short_title = u'6'
    luggage_luggagewheels_translation_6.master = luggage_luggagewheels_3
    luggage_luggagewheels_translation_6.save()

    luggage_luggagewheels_translation_7 = LuggageWheelsTranslation()
    luggage_luggagewheels_translation_7.language_code = u'en'
    luggage_luggagewheels_translation_7.title = u'No Wheels'
    luggage_luggagewheels_translation_7.short_title = u'No Wheels'
    luggage_luggagewheels_translation_7.master = luggage_luggagewheels_4
    luggage_luggagewheels_translation_7.save()

    luggage_luggagewheels_translation_8 = LuggageWheelsTranslation()
    luggage_luggagewheels_translation_8.language_code = u'es'
    luggage_luggagewheels_translation_8.title = u'sin Ruedas'
    luggage_luggagewheels_translation_8.short_title = u'sin Ruedas'
    luggage_luggagewheels_translation_8.master = luggage_luggagewheels_4
    luggage_luggagewheels_translation_8.save()

def import_data():
    # Initial Imports

    # Processing model: luggage.models.Luggage

    for i in range(100):
        luggage = Luggage()
        luggage.set_current_language('en')
        luggage.title = u'SwissGear Large Trolley Bag'
        luggage.full_price = round(100+random.random()*200, 2)
        luggage.day_price = round(3+random.random()*7, 2)
        luggage.cnt = int(5+random.random()*20)
        luggage.luggage_wheels =  random.choice(LuggageWheels.objects.all())
        luggage.luggage_size =  random.choice(LuggageSize.objects.all())
        luggage.luggage_class =  random.choice(LuggageClass.objects.all())
        luggage.details = u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed'
        luggage.features = u'Lorem ipsum dolor sit amet, consectetur \r\nadipisicing elit, sed do eiusmod tempor incididunt \r\nut labore et dolore magna aliqua. Duis aute\r\nirure dolor in reprehenderit in voluptate velit esse'
        luggage.save()

        for i in range(random.randrange(1,3)):
            photo = LuggagePhoto()
            photo.luggage = luggage
            photo.photo = 'luggage/4R5l6xqban.png'
            photo.save()

def import_warehouses():
    c_usa = Country.objects.get(name='United States')
    c_mx = Country.objects.get(name='Mexico')

    for i in range(20):
        c = random.choice([c_usa, c_mx])
        r = random.choice(c.region_set.all())
        t = random.choice(r.city_set.all())
        while Warehouse.objects.filter(city=t).exists():
            t = random.choice(r.city_set.all())

        w = Warehouse()
        w.country = c
        w.region = r
        w.city = t
        w.save()


def assign_warehouses():
    for bag in Luggage.objects.all():
        bag.warehouse = random.choice(Warehouse.objects.all())
        bag.save()


#clean_all()
#import_dics()
#import_data()
import_warehouses()
assign_warehouses()
