from currencies.models import Currency
from currencies.conf import SESSION_KEY


class CurrencyFromLocaleMiddleware(object):
    code = 'USD'

    def process_request(self, request):
        lang = request.LANGUAGE_CODE

        if lang == 'en':
            self.code = 'USD'
        elif lang == 'es':
            self.code = 'MXN'

        if self.code and Currency.active.filter(code=self.code).exists():
            if hasattr(request, 'session'):
                request.session[SESSION_KEY] = self.code

    def process_response(self, request, response):
        if self.code and Currency.active.filter(code=self.code).exists():
            if not hasattr(request, 'session'):
                response.set_cookie(SESSION_KEY, self.code)

        return response
