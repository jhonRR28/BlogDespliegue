from django.urls import path
from .views import newsletter_signup, newslwtter_unsubscribe

app_name = 'newsletter'

urlpatterns = [
    path('entrenamiento/', newsletter_signup, name="optin" ),
    path('unsubscribe/', newslwtter_unsubscribe, name="unsubscribe" ),
]
