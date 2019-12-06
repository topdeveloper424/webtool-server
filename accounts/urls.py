from django.urls import path,include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('sign-in', views.signin,name='sign_in'),
    path('sign-up', views.sign_up,name='sign_up'),
    path('sign-out', views.sign_out,name='sign_out'),
]

