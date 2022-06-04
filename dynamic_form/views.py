from django.http import HttpResponse
from django.utils.module_loading import import_string
from django.views import View

from dynamic_form.exceptions import DuplicateKeyException, FormKeyError
from dynamic_form.settings import dynamic_form_settings


class GetFormView(View):

    def post(self, request, *args, **kwargs):
        form = self._get_form(request.POST)
        return HttpResponse(
            form.get_form_html()
        )

    def _get_form(self, post_data):
        form_key = post_data.get('ddf-form-key')
        module_path = self._get_form_keys_reversed(form_key)
        Form = import_string(module_path)
        return Form(post_data)

    def _get_form_keys_reversed(self, form_key):
        form_keys = dynamic_form_settings.FORM_KEYS
        form_keys_reversed = [
            key for key, value in form_keys.items() if value == form_key
        ]
        if len(form_keys_reversed) == 0:
            raise FormKeyError(f'Form key is not defined: {form_key}')
        if len(form_keys_reversed) != 1:
            raise DuplicateKeyException(f'Form key is duplicated: {form_key}')
        return form_keys_reversed[0]
