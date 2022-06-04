from django import forms
from django.forms.utils import ErrorDict
from django.template.loader import render_to_string
from django.utils.html import format_html

from dynamic_form.settings import dynamic_form_settings


class DynamicFormMixin:
    form_template = 'dynamic_form/default_form.html'
    do_dynamic_validate = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            self._is_field_hidden(name, field)
            self._is_field_disabled(name, field)
            self._is_field_required(name, field)
            self._set_queryset(name, field)
            self._set_choices(name, field)

    @property
    def form_key(self):
        form_path = f'{self.__class__.__module__}.{self.__class__.__name__}'
        return dynamic_form_settings.FORM_KEYS.get(form_path, form_path)

    def _is_field_hidden(self, name, field):
        if hasattr(self, f'is_hidden_{name}'):
            is_hidden = getattr(self, f'is_hidden_{name}')()
            if is_hidden:
                field.widget = forms.HiddenInput()
                field.required = False

    def _is_field_disabled(self, name, field):
        if hasattr(self, f'is_disabled_{name}'):
            is_disabled = getattr(self, f'is_disabled_{name}')()
            if is_disabled:
                field.disabled = True
                field.required = False

    def _is_field_required(self, name, field):
        if hasattr(self, f'is_required_{name}'):
            is_required = getattr(self, f'is_required_{name}')()
            if is_required:
                field.required = True

    def _set_queryset(self, name, field):
        if hasattr(self, f'set_queryset_{name}'):
            queryset = getattr(self, f'set_queryset_{name}')()
            field.queryset = queryset

    def _set_choices(self, name, field):
        if hasattr(self, f'set_choices_{name}'):
            choices = getattr(self, f'set_choices_{name}')()
            field.choices = choices

    def render_form(self):
        return format_html(
            '<div class="ddf-form-container" data-form-key="{}">{}</div>',
            self.form_key,
            self.get_form_html(),
        )

    def get_form_html(self):
        return render_to_string(
            self.form_template,
            self.get_form_context(),
        )

    def get_form_context(self):
        context = {
            'form': self,
        }
        return context

    def full_clean(self):
        self._errors = ErrorDict()
        if self.do_dynamic_validate:
            super().full_clean()
