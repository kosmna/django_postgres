# -*- coding: utf-8 -*-
import json

def context_params(request):
    cart_j = request.COOKIES.get('cart', '[]')
    cart = json.loads(cart_j)

    cart_cnt = 0
    for el in cart:
        cart_cnt += int(el['cnt'])

    return {
        'cart_cnt': cart_cnt,
    }
