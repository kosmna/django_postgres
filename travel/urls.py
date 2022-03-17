# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy

from .views import (HomeView, ResetPassword, SignupView, SigninView, AccountView,
                    ApiRegisterView, ApiEmailValidationView, ApiLoginView, DetailsView,
                    SearchView, ChangeLocaleView, CartView, OrdersView, ApiGetRigionsView,
                    ApiAddToCartView, ApiUpdateCartView, ApiGeoCountryView, ApiGeoRegionView,
                    ApiGeoCityView, ApiGeoZipcodeView, ApiGetCityView, ApiGetCountryView,
                    ApiAddAddressView, ApiRemoveAddressView, ApiAddPaymentView, ApiRemovePaymentView,
                    ApiCreateOrderView, ApiReturnItemView, ApiResetView, ApiUpdateUserView,
                    ApiApplyCouponView)

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^account/$', AccountView.as_view(), name='account'),
    url(r'^details/(?P<pk>[0-9]+)/$', DetailsView.as_view(), name='details'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^cart/$', CartView.as_view(), name='cart'),
    url(r'^orders/$', OrdersView.as_view(), name='orders'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^signin/$', SigninView.as_view(), name='signin'),
    url(r'^logout/$', auth_views.logout, {'next_page': settings.LOGOUT_URL}, name="logout"),
    url(r'^change-locale/(?P<locale_code>[\w-]+)/$', ChangeLocaleView.as_view(), name='change_locale'),

    url(r'^api/login/$', ApiLoginView.as_view(), name='login'),
    url(r'^api/reset/$', ApiResetView.as_view(), name='api_reset'),
    url(r'^api/register/$', ApiRegisterView.as_view(), name='register'),
    url(r'^api/email-validation/$', ApiEmailValidationView.as_view(), name='email_validation'),
    url(r'^api/get_country/$', ApiGetCountryView.as_view(), name='get_country'),
    url(r'^api/get_regions/$', ApiGetRigionsView.as_view(), name='get_regions'),
    url(r'^api/get_city/$', ApiGetCityView.as_view(), name='get_city'),
    url(r'^api/add_to_cart/$', ApiAddToCartView.as_view(), name='add_to_cart'),
    url(r'^api/update_cart/$', ApiUpdateCartView.as_view(), name='update_cart'),
    url(r'^api/update_user/$', ApiUpdateUserView.as_view(), name='update_user'),
    url(r'^api/add_address/$', ApiAddAddressView.as_view(), name='add_address'),
    url(r'^api/remove_address/$', ApiRemoveAddressView.as_view(), name='remove_address'),
    url(r'^api/add_payment/$', ApiAddPaymentView.as_view(), name='add_payment'),
    url(r'^api/remove_payment/$', ApiRemovePaymentView.as_view(), name='remove_payment'),
    url(r'^api/create_order/$', ApiCreateOrderView.as_view(), name='create_order'),
    url(r'^api/return_item/$', ApiReturnItemView.as_view(), name='return_item'),
    url(r'^api/apply_coupon/$', ApiApplyCouponView.as_view(), name='apply_coupon'),

    url(r'^api/geo/country/$', ApiGeoCountryView.as_view(), name='api_all_country'),
    url(r'^api/geo/region/$', ApiGeoRegionView.as_view(), name='api_all_region'),
    url(r'^api/geo/city/$', ApiGeoCityView.as_view(), name='api_all_ciry'),
    url(r'^api/geo/zipcode/$', ApiGeoZipcodeView.as_view(), name='api_all_zipcode'),


    # 3 reset password
    url(r'^reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {
            'template_name': 'new_password.html',
            'set_password_form': ResetPassword,
            'post_reset_redirect': reverse_lazy('reset_password_complete')
        },
        name='reset_password'),

    # 4 already reset
    url(r'^reset/done/$', auth_views.password_reset_complete,
        {'template_name': 'already_reset.html'},
        name='reset_password_complete'),
]

