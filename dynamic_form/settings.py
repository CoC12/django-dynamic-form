from django.conf import settings

DEFAULTS = {
    'FORM_KEYS': {},
}


class DynamicFormSettings:

    def __init__(self):
        self.user_settings = getattr(settings, 'DYNAMIC_FORM', {})
        self._cached_attrs = set()

    def __getattr__(self, attr):
        if attr not in DEFAULTS:
            raise AttributeError(f'Invalid setting: {attr}')
        try:
            value = self.user_settings[attr]
        except KeyError:
            value = DEFAULTS[attr]
        return value


dynamic_form_settings = DynamicFormSettings()
