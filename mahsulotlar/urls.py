from django.urls import path
from mahsulotlar.views import *
from akkauntlar.views import *

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('store', store, name='store'),
    path('cart', Cart.as_view(), name='cart'),
    path('orders', OrderView.as_view(), name='orders'),

    #Views from akkauntlar
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout, name='logout'),
    path('check-out', CheckOut.as_view(), name='checkout'),
]
