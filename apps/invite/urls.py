from django.urls import path

from .import views


urlpatterns = [
    path('validate-code/',views.validate_code,name='code-validate'),
]


app_name = "invite"