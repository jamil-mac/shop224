from django.urls import path

from contacts import views

app_name = 'contacts'

urlpatterns = [
    path('', views.ContactCreateView.as_view(), name='contact'),
]