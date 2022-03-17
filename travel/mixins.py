import json

from django.http import HttpResponse


class AjaxableResponseMixin(object):
    def __getattr__(self, name):
        if name == 'response_data':
            if not getattr(self, '_response_data', None):
                self._response_data = {}

            return self._response_data

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            self.response_data['pk'] = self.object.pk
            return self.render_to_json_response(self.response_data)
        else:
            return response
