# -*- coding: utf-8 -*-
import json
import datetime
import decimal

from django.utils.translation import ugettext as _
from constance import config
from django import forms
from django.utils import translation, timezone
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import check_for_language
from django.contrib.auth import login, authenticate
from django.views.generic.base import TemplateView, RedirectView, View
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.contrib.auth.forms import PasswordResetForm

from pinax import stripe
from cities.models import Country, City, Region, PostalCode

from .models import (User, Luggage, LuggageSize, Warehouse, LuggageClass,
                     LuggageWheels, Order, Address, ReturnTime, Invoice, Coupon)
from .mixins import AjaxableResponseMixin


__all__ = ['HomeView']


def check_dates_availiable(luggage_id, date_start, date_end):
    luggage = Luggage.objects.get(pk=luggage_id)
    cnt_in_rent = Order.objects.filter(date_end__gt=date_start, date_start__lt=date_end).count()

    return luggage.cnt - cnt_in_rent


def get_param(request, param):
    val = request.GET.get(param)

    if val is None:
        val = request.COOKIES.get('cur_'+param)

    return val


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self):
        ctx = super(HomeView, self).get_context_data()
        ctx['countries'] = Warehouse.get_available_countries()
        ctx['region'] = []
        ctx['sizes'] = LuggageSize.objects.all()
        return ctx


class SignupView(TemplateView):
    template_name = 'signup.html'


class SigninView(TemplateView):
    template_name = 'login.html'


class AccountView(LoginRequiredMixin, TemplateView):
    login_url = '/signin/'
    template_name = 'account.html'

    def get_context_data(self):
        ctx = super(AccountView, self).get_context_data()
        stripe.actions.customers.sync_customer(self.request.user.customer)
        ctx['address_list'] = self.request.user.address_set.filter(is_deleted=False)
        ctx['payment_list'] = self.request.user.customer.card_set.all()
        return ctx


class CartView(TemplateView):
    template_name = 'cart.html'

    def get_context_data(self):
        ctx = super(CartView, self).get_context_data()

        cart_j = self.request.COOKIES.get('cart', '[]')
        cart = json.loads(cart_j)
        items = []
        total_save = 0
        cart_total = 0
        cart_cnt = 0

        total_days = 0
        total_coupon = 0
        free_days = 0
        coupon = self.request.COOKIES.get('coupon', None)
        if coupon:
            coupon = Coupon.objects.get(pk=coupon)
            free_days = coupon.free_days
            today = timezone.now()
            if today > coupon.expire:
                coupon = None


        for item in cart:
            try:
                dates = item['dates']
                date_start, date_end = dates.split(' - ')
                date_start_d = datetime.datetime.strptime(date_start, "%Y-%m-%d")
                date_end_d = datetime.datetime.strptime(date_end, "%Y-%m-%d")
                days = (date_end_d - date_start_d).days or 1
                item['luggage'] = Luggage.objects.get(pk=item['luggage'])
                subtotal = item['luggage'].day_price*int(item['cnt'])*days
                item['subtotal'] = subtotal
                total_save += item['luggage'].full_price*int(item['cnt']) - subtotal
                cart_total += subtotal
                cart_cnt += int(item['cnt'])
                items.append(item)
                total_days += days
                if free_days > 0:
                    free_days -= days
                    if free_days < 0:
                        total_coupon += item['luggage'].day_price * (-1*free_days)
                        free_days = 0
                else:
                    total_coupon += subtotal
            except:
                pass

        if coupon:
            ctx['coupon_code'] = coupon.code
        else:
            ctx['coupon_code'] = ""

        if coupon and (not coupon.min_days or total_days > coupon.min_days) and (not coupon.min_total or cart_total > coupon.min_total):
            if coupon.discount:
                total_coupon = round(total_coupon * (100-coupon.discount)/100.0, 2)

        ctx['items'] = items
        ctx['total_coupon'] = total_coupon
        ctx['total_save'] = round(total_save, 2) if total_save > 0 else 0
        ctx['cart_total'] = round(cart_total, 2)
        ctx['cart_cnt'] = cart_cnt
        if self.request.user.is_authenticated():
            stripe.actions.customers.sync_customer(self.request.user.customer)
            ctx['address_list'] = self.request.user.address_set.filter(is_deleted=False)
            ctx['payment_list'] = self.request.user.customer.card_set.all()
        else:
            ctx['address_list'] = []
            ctx['payment_list'] = []

        return ctx


class OrdersView(LoginRequiredMixin, TemplateView):
    login_url = '/signin/'
    template_name = 'orders.html'

    def get_context_data(self):
        ctx = super(OrdersView, self).get_context_data()
        ctx['items'] = Order.objects.filter(user=self.request.user, is_returned=False)
        ctx['returntimes'] = ReturnTime.objects.all();
        return ctx


class DetailsView(DetailView):
    model = Luggage
    template_name = 'details.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(DetailsView, self).get_context_data(*args, **kwargs)
        ctx['total_save'] = round(self.object.full_price - self.object.day_price, 2)
        return ctx


class SearchView(ListView):
    model = Luggage
    template_name = 'search.html'
    paginate_by = 4
    context_object_name = 'items'

    def render_to_response(self, context, **response_kwargs):
        response = super(SearchView, self).render_to_response(context, **response_kwargs)

        for param in ['country', 'region', 'city', 'size', 'wheel', 'class']:
            val = self.request.GET.get(param)
            if val is not None:
                response.set_cookie("cur_"+param, val)

        return response

    def get_context_data(self):
        ctx = super(SearchView, self).get_context_data()

        ctx['luggage_sizes'] = LuggageSize.objects.all()
        ctx['luggage_classes'] = LuggageClass.objects.all()
        ctx['luggage_wheels'] = LuggageWheels.objects.all()

        ctx['size_title'] = 'all bags'
        ctx['country_title'] = 'any country'
        ctx['region_title'] = 'any region'
        ctx['city_title'] = 'any_city'

        try:
            country = get_param(self.request, 'country')
            ctx['country_title'] = Country.objects.get(id=country).code
        except:
            pass

        try:
            region = get_param(self.request, 'region')
            ctx['region_title'] = Region.objects.get(id=region).name
        except:
            pass

        try:
            city = get_param(self.request, 'city')
            ctx['city_title'] = City.objects.get(id=city).name
        except:
            pass

        try:
            size = get_param(self.request, 'size')
            ctx['size_title'] = "%s bags" % LuggageSize.objects.get(id=size).title.lower()
        except:
            pass

        return ctx

    def get_queryset(self):
        filters = {}

        country = get_param(self.request, 'country')
        if country:
            filters['warehouse__country__pk'] = country

        region = get_param(self.request, 'region')
        if region:
            filters['warehouse__region__pk'] = region

        size = get_param(self.request, 'size')
        if size:
            filters['luggage_size__pk'] = size

        wheel = get_param(self.request, 'wheel')
        if wheel:
            filters['luggage_wheels__pk'] = wheel

        clas = get_param(self.request, 'class')
        if clas:
            filters['luggage_class__pk'] = clas


        return Luggage.objects.filter(**filters)


class ApiEmailValidationView(AjaxableResponseMixin, View):
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email')
        valid = False
        if email:
            if request.user:
                valid = not User.objects.filter(email__iexact=email).exclude(pk=request.user.pk).exists()
            else:
                valid = not User.objects.filter(email__iexact=email).exists()

        if valid:
            return self.render_to_json_response({
                'success': 'OK',
            })
        else:
            return self.render_to_json_response({
                'message': _('User with this email already exists'),
            })


class ResetPassword(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput, min_length=6, max_length=100)
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput, min_length=6, max_length=100)


class ApiResetView(AjaxableResponseMixin, View):
    http_method_names = ['post', ]

    def post(self, request, *args, **kwargs):
        context = {}

        form = PasswordResetForm(request.POST)
        if form.is_valid():
            opts = {
                'request': request,
                'use_https': request.is_secure(),
                'from_email': settings.DEFAULT_FROM_EMAIL,
                'email_template_name': 'emails/forget/generate_link.html',
                'subject_template_name': 'emails/forget/reset_subject.txt',
                'html_email_template_name': 'emails/forget/generate_link.html',
            }
            form.save(**opts)

            context['success'] = True
            context['redirect_to'] = str(reverse_lazy('home'))
            return self.render_to_json_response(context)
        else:
            # Return an 'invalid login' error message.
            context['success'] = False
            context['error_msg'] = _('Invalid username.')

        return self.render_to_json_response(context)


class ApiLoginView(AjaxableResponseMixin, View):
    http_method_names = ['post', ]

    def post(self, *args, **kwargs):
        context = {}
        email = self.request.POST['email']
        password = self.request.POST['password']
        username = ""

        try:
            u = User.objects.get(email=email)
            username = u.username
        except:
            pass

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                context['success'] = True
                context['redirect_to'] = str(reverse_lazy('home'))
                return self.render_to_json_response(context)
            else:
                # Return a 'disabled account' error message
                context['success'] = False
                context['error_msg'] = _('User account has been disabled.')
        else:
            # Return an 'invalid login' error message.
            context['success'] = False
            context['error_msg'] = _('Invalid username/password.')

        return self.render_to_json_response(context)


class ApiRegisterView(AjaxableResponseMixin, View):
    http_method_names = ['post', ]

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        phone = request.POST.get('phone', None)
        msg = ""

        user = request.user
        can_register = False
        if user.is_authenticated():
            can_register = False
            msg = _('You are already registered')
        elif User.objects.filter(username=email).exists():
            msg = _('User with this email already exists')
        else:
            user = User(username=email)
            can_register = True
        if can_register:
            if phone and email and password:
                user.email = email
                user.phone = phone
                user.set_password(password)
                user.save()

                user = authenticate(username=user.username, password=password)
                login(self.request, user)
                return self.render_to_json_response({
                    'success': True,
                    'redirect_to': str(reverse_lazy('home'))
                })
            else:
                msg = _('Not all required field were filled')
        return self.render_to_json_response({
            'success': False,
            'error_msg': msg
        })


class ApiGetRigionsView(AjaxableResponseMixin, View):
    def get(self, request, *args, **kwargs):
        list = []
        country_id = request.GET.get('parent_id', '')
        regions = Warehouse.get_available_regions(country_id)
        for reg in regions:
            list.append((reg.id, reg.name))
        return self.render_to_json_response(list)


class ApiGetCountryView(AjaxableResponseMixin, View):
    def get(self, request, *args, **kwargs):
        list = []
        countries = Warehouse.get_available_countries()
        for c in countries:
            list.append((c.id, c.name))
        return self.render_to_json_response(list)


class ApiGetCityView(AjaxableResponseMixin, View):
    def get(self, request, *args, **kwargs):
        list = []
        region_id = request.GET.get('parent_id', '')
        cities = Warehouse.get_available_city(region_id)
        for city in cities:
            list.append((city.id, city.name))
        return self.render_to_json_response(list)


class ApiGeoCountryView(AjaxableResponseMixin, View):
    def get(self, request, *args, **kwargs):
        res = list(Country.objects.all().values_list('pk', 'name'))
        return self.render_to_json_response(res)


class ApiGeoRegionView(AjaxableResponseMixin, View):
    def get(self, request, *args, **kwargs):
        country_id = request.GET.get('parent_id', '')
        res = list(Region.objects.filter(country_id=country_id).values_list('pk', 'name'))
        return self.render_to_json_response(res)


class ApiGeoCityView(AjaxableResponseMixin, View):
    def get(self, request, *args, **kwargs):
        region_id = request.GET.get('parent_id', '')
        res = list(City.objects.filter(region_id=region_id).values_list('pk', 'name'))
        return self.render_to_json_response(res)


class ApiGeoZipcodeView(AjaxableResponseMixin, View):
    def get(self, request, *args, **kwargs):
        city_id = request.GET.get('parent_id', '')
        res = list(PostalCode.objects.filter(city_id=city_id).values_list('pk', 'name'))
        return self.render_to_json_response(res)


class ApiCreateOrderView(AjaxableResponseMixin, View):
    http_method_names = ['post', ]

    def post(self, request, *args, **kwargs):
        invoice = None
        total_cnt = 0
        total_days = 0
        total_freedays = 0
        free_days = 0
        new_orders = []
        try:
            user = request.user
            if not user.is_authenticated():
                return self.render_to_json_response({'success': False, })

            address = Address.objects.get(pk=request.POST.get('address'))
            payment = user.customer.card_set.get(id=request.POST.get('payment'))

            coupon = request.COOKIES.get('coupon', None)
            if coupon:
                coupon = Coupon.objects.get(pk=coupon)
                free_days = coupon.free_days
                today = timezone.now()
                if today > coupon.expire:
                    coupon = None

            cart_j = request.COOKIES.get('cart', '[]')
            cart = json.loads(cart_j)

            invoice = Invoice.objects.create(
                number="1",
                user=user,
                amount=0,
                comments="",
                invoice_date=timezone.now(),
            )


            for item in cart:
                dates = item['dates']
                date_start, date_end = dates.split(' - ')
                date_start_d = datetime.datetime.strptime(date_start, "%Y-%m-%d")
                date_end_d = datetime.datetime.strptime(date_end, "%Y-%m-%d")
                days = (date_end_d - date_start_d).days or 1
                luggage = Luggage.objects.get(pk=item['luggage'])
                cnt = int(item['cnt'])

                cnt_availiable = check_dates_availiable(luggage.id, date_start_d, date_end_d)

                if cnt > cnt_availiable:
                    raise Exception(_('not enough bags for selected dates'))

                total_cnt += cnt
                total_days += days

                for i in range(int(item['cnt'])):
                    o = Order()
                    o.invoice = invoice
                    o.luggage = luggage
                    o.address = address
                    o.user = request.user
                    o.date_start = date_start_d
                    o.date_end = date_end_d
                    o.total = luggage.day_price*days
                    if free_days > 0:
                        free_days -= days
                        if free_days < 0:
                            total_freedays += luggage.day_price * (-1*free_days)
                            free_days = 0
                    else:
                        total_freedays += o.total
                    o.save()
                    invoice.amount += o.total
                    new_orders.append(o)

            if coupon and (not coupon.min_days or total_days > coupon.min_days) and (not coupon.min_total or invoice.amount > coupon.min_total):
                if coupon.free_days:
                    invoice.amount = total_freedays
                if coupon.discount:
                    invoice.amount = round(invoice.amount * (100-coupon.discount)/100.0, 2)

            payment = stripe.actions.charges.create(
                description="Luggary Invoice: {}\nRenting bags on luggary.com".format(invoice.number),
                amount=decimal.Decimal(invoice.amount),
                source=payment.stripe_id,
                currency='usd',
                customer=user.customer
            )
            # if payment.paid:
            invoice.is_paid = payment.paid
            invoice.save()

            res = self.render_to_json_response({'success': True, })
            res.set_cookie('cart', '[]')

            Order.send_email(user, new_orders)

            return res

        except Exception as e:
            if not invoice:
                invoice.delete()
                invoice = None
            pass

        if not invoice or not invoice.is_paid:
            if invoice:
                invoice.delete()
            for o in new_orders:
                o.delete()

        return self.render_to_json_response({'success': False, })


class ApiAddPaymentView(AjaxableResponseMixin, View):
    http_method_names = ['post', ]
    def post(self, request, *args, **kwargs):
        error_msg = _('Cannot add payment method')
        try:
            user = request.user
            if not user.is_authenticated():
                return self.render_to_json_response({'success': False, })

            token = request.POST.get('token')
            card = stripe.actions.sources.create_card(user.customer, token)

            return self.render_to_json_response({'success': True, 'id': card.id, 'last4': card.last4, 'brand': card.brand})
        except Exception as e:
            if e.message:
                error_msg = e.message
            pass
        return self.render_to_json_response({'success': False, 'error_msg': error_msg})


class ApiRemovePaymentView(AjaxableResponseMixin, View):
    http_method_names = ['post', ]
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            if not user.is_authenticated():
                return self.render_to_json_response({'success': False, })

            payment_id = int(request.POST.get('address_id'))
            payment = user.customer.card_set.get(id=payment_id)
            stripe.actions.sources.delete_card(user.customer, payment.stripe_id)

            return self.render_to_json_response({'success': True, })
        except:
            pass
        return self.render_to_json_response({'success': False, })



class ApiAddAddressView(AjaxableResponseMixin, View):
    http_method_names = ['post', ]
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            if not user.is_authenticated():
                return self.render_to_json_response({'success': False, })

            title = request.POST.get('title')
            country = request.POST.get('country')
            region = request.POST.get('region')
            zipcode = request.POST.get('zipcode')
            city = request.POST.get('city')
            street = request.POST.get('street')

            a = Address()
            a.user = user
            a.title = title
            a.country = Country.objects.get(id=country)
            a.region = Region.objects.get(id=region)
            a.city = City.objects.get(id=city)
            a.code = zipcode
            a.street = street
            a.save()

            label = '%s, %s, %s, %s %s' % (a.title, a.street, a.city.name, a.region.code, a.country.code)

            return self.render_to_json_response({'success': True, 'id': a.id, 'label': label })
        except:
            pass
        return self.render_to_json_response({'success': False, 'error_msg': _('Cannot add address')})


class ApiRemoveAddressView(AjaxableResponseMixin, View):
    http_method_names = ['post', ]
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            if not user.is_authenticated():
                return self.render_to_json_response({'success': False, })

            address_id = int(request.POST.get('address_id'))
            address = Address.objects.get(pk=address_id, user=user)
            address.is_deleted = True
            address.save()

            return self.render_to_json_response({'success': True, })
        except:
            pass
        return self.render_to_json_response({'success': False, })


class ApiReturnItemView(AjaxableResponseMixin, View):
    http_method_names = ['post', ]
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            if not user.is_authenticated():
                return self.render_to_json_response({'success': False, })

            id = request.POST.get('id')
            returndate = ReturnTime.objects.get(id = request.POST.get('returndate'))
            if id == 'all':
                for order in Order.objects.filter(user=user, is_returned=False):
                    order.scheduled_return_time = returndate
                    order.save()
            else:
                order = Order.objects.get(user=user, id=id)
                order.scheduled_return_time = returndate
                order.save()

            return self.render_to_json_response({'success': True, })
        except:
            pass
        return self.render_to_json_response({'success': False, })


class ApiUpdateCartView(AjaxableResponseMixin, View):
    http_method_names = ['post', ]
    def post(self, request, *args, **kwargs):
        try:
            cart_id = int(request.POST.get('cart_id'))
            luggage_id = int(request.POST.get('luggage_id'))
            luggage = Luggage.objects.get(pk=luggage_id)

            cnt = request.POST.get('cnt')
            dates = request.POST.get('dates')

            if not cnt or not dates:
                return self.render_to_json_response({'success': False, })

            cnt = int(cnt)
            date_start, date_end = dates.split(' - ')
            date_start_d = datetime.datetime.strptime(date_start, "%Y-%m-%d")
            date_end_d = datetime.datetime.strptime(date_end, "%Y-%m-%d")

            cnt_availiable = check_dates_availiable(luggage_id, date_start_d, date_end_d)

            if cnt > cnt_availiable:
                return self.render_to_json_response({'success': False, 'cnt': cnt_availiable })

            cart_j = request.COOKIES.get('cart', '[]')
            cart = json.loads(cart_j)

            id = 0
            el_id = 0
            exist = False
            cart_cnt = 0
            for el in cart:
                if el['cart_id'] == cart_id:
                    exist = True
                    if el['cnt'] + cnt > cnt_availiable:
                        return self.render_to_json_response({'success': False, 'cnt': cnt_availiable - int(el['cnt'])})
                    el['cnt'] = cnt
                    el['date_start'] = date_start
                    el['date_end'] = date_end
                    el['dates'] = dates
                    el_id = id
                cart_cnt += int(el['cnt'])
                id += 1


            if not exist:
                return self.render_to_json_response({'success': False, })
            elif cart[el_id]['cnt'] == 0:
                del cart[el_id]

            cart_j = json.dumps(cart)

            res = self.render_to_json_response({'success': True, 'cnt': cart_cnt })
            res.set_cookie('cart', cart_j)
            return res
        except:
            pass

        return self.render_to_json_response({'success': False, })


class ApiUpdateUserView(AjaxableResponseMixin, View):
    http_method_names = ['post', ]
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            msg = []

            email = request.POST.get('email')
            phone = request.POST.get('phone')
            pass1 = request.POST.get('password1')
            pass2 = request.POST.get('password2')

            if email is not None and user.email != email:
                user.email = email
                msg.append(_("Email was updated"))

            if phone is not None and user.phone != phone:
                user.phone = phone
                msg.append(_("Phone was updated"))

            if pass1 is not None and pass2 is not None and pass1 == pass2:
                user.set_password(pass1)
                msg.append(_("Password was updated"))

            user.save()

            return self.render_to_json_response({'success': True, 'msg': '<br>'.join(msg)})
        except:
            pass

        return self.render_to_json_response({'success': False, })


class ApiApplyCouponView(AjaxableResponseMixin, View):
    http_method_names = ['post', ]

    def post(self, request, *args, **kwargs):
        try:
            code = request.POST.get('code')
            coupon = Coupon.objects.get(code=code)

            today = timezone.now()
            if today > coupon.expire:
                return self.render_to_json_response({'success': False, 'msg': _('Coupon is expired')})

            cart_j = self.request.COOKIES.get('cart', '[]')
            cart = json.loads(cart_j)
            items = []
            total_save = 0
            cart_total = 0
            cart_cnt = 0

            total_days = 0
            total_coupon = 0
            free_days = 0

            for item in cart:
                try:
                    dates = item['dates']
                    date_start, date_end = dates.split(' - ')
                    date_start_d = datetime.datetime.strptime(date_start, "%Y-%m-%d")
                    date_end_d = datetime.datetime.strptime(date_end, "%Y-%m-%d")
                    days = (date_end_d - date_start_d).days or 1
                    item['luggage'] = Luggage.objects.get(pk=item['luggage'])
                    subtotal = item['luggage'].day_price*int(item['cnt'])*days
                    item['subtotal'] = subtotal
                    total_save += item['luggage'].full_price*int(item['cnt']) - subtotal
                    cart_total += subtotal
                    cart_cnt += int(item['cnt'])
                    items.append(item)
                    total_days += days
                    if free_days > 0:
                        free_days -= days
                        if free_days < 0:
                            total_coupon += item['luggage'].day_price * (-1*free_days)
                            free_days = 0
                    else:
                        total_coupon += subtotal
                except:
                    pass

            if coupon and (not coupon.min_days or total_days > coupon.min_days) and (not coupon.min_total or cart_total > coupon.min_total):
                if coupon.discount:
                    total_coupon = round(total_coupon * (100-coupon.discount)/100.0, 2)

            res = self.render_to_json_response({'success': True, 'total_coupon': total_coupon})
            res.set_cookie('coupon', coupon.pk)
            return res
        except:
            pass

        return self.render_to_json_response({'success': False, 'msg': _('Invalid code')})


class ApiAddToCartView(AjaxableResponseMixin, View):
    http_method_names = ['post', ]

    def post(self, request, *args, **kwargs):
        try:
            luggage_id = int(request.POST.get('luggage_id'))
            luggage = Luggage.objects.get(pk=luggage_id)

            cnt = request.POST.get('cnt')
            dates = request.POST.get('dates')

            if not cnt or not dates:
                return self.render_to_json_response({'success': False, })

            cnt = int(cnt)
            date_start, date_end = dates.split(' - ')
            date_start_d = datetime.datetime.strptime(date_start, "%Y-%m-%d")
            date_end_d = datetime.datetime.strptime(date_end, "%Y-%m-%d")

            cnt_availiable = check_dates_availiable(luggage_id, date_start_d, date_end_d)

            if cnt > cnt_availiable:
                return self.render_to_json_response({'success': False, 'cnt': cnt_availiable })

            cart_j = request.COOKIES.get('cart', '[]')
            cart = json.loads(cart_j)
            cart_cnt = 0
            i = 0

            exist = False
            for el in cart:
                if el['luggage'] == luggage_id and el['date_start'] == date_start and el['date_end'] == date_end:
                    exist = True
                    if el['cnt'] + cnt > cnt_availiable:
                        return self.render_to_json_response({'success': False, 'cnt': cnt_availiable - int(el['cnt'])})
                    el['cnt'] = int(el['cnt']) + cnt
                cart_cnt += int(el['cnt'])
                i += 1

            if not exist:
                o = {
                    'cart_id': i,
                    'luggage': luggage.pk,
                    'cnt': cnt,
                    'date_start': date_start,
                    'date_end': date_end,
                    'dates': dates,
                }
                cart_cnt += int(cnt)
                cart.append(o)

            cart_j = json.dumps(cart)

            res = self.render_to_json_response({'success': True, 'cnt': cart_cnt })
            res.set_cookie('cart', cart_j)
            return res
        except:
            pass

        return self.render_to_json_response({'success': False, })


class ChangeLocaleView(RedirectView):
    url = "/"
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        url = "/"
        try:
            url = self.request.META['HTTP_REFERER']
        except:
            pass

        return url

    def get(self, request, locale_code, *args, **kwargs):
        response = super(ChangeLocaleView, self).get(request, args, *kwargs)
        if locale_code and check_for_language(locale_code):
            translation.activate(locale_code)
            if hasattr(request, 'session'):
                request.session['django_language'] = locale_code
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, locale_code)
            translation.activate(locale_code)
        return response
