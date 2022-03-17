
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.utils import translation

from luggage.models import Order, Invoice


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start')
        translation.activate('en')

        for order in Order.objects.filter(is_returned=False):
            if order.duedays == 1:
                order.send_remind_email()
                self.stdout.write('Send remind notification for order {pk}'.format(pk=order.pk))

        for invoice in Invoice.objects.filter(is_paid=False):
            invoice.send_remind_email()
            self.stdout.write('Send remind notification for invoice {pk}'.format(pk=invoice.pk))

        self.stdout.write('Finish')
