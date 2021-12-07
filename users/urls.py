from django.urls import path
from . import views

urlpatterns = [
        path('signup/',views.signup),
        path('signin/',views.Login.as_view(),name='login'),
]