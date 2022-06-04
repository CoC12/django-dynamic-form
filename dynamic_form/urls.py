from django.urls import path

from dynamic_form.views import GetFormView

urlpatterns = [
    path('ddf-get-form/', GetFormView.as_view(), name='ddf-get-form'),
]
