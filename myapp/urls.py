from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name=''),
    path('flights/', views.showflights, name='flights'),
    path('invoice/', views.invoice, name='invoice'),
    path('form/', views.form, name='form'),
    path('bookedFlights/', views.showBookedFlights, name='bookedFlights'),
    path('cancel/', views.cancel, name='cancel'),
    path('confirm/', views.confirm, name='confirm'),
    path('createAccount/', views.createAccount, name='createAccount'),
    path('doneAccount/', views.doneAccount, name='doneAccount'),
    path('login/', views.login2, name='login2'),
    path('logout2/', views.logout2, name='logout2'),
    path('routes/', views.routes, name='routes'),
]
