from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("checkout/", views.checkout, name="checkout"),
    path("place-order/", views.place_order, name="place_order"),
    path("payment/", views.razorpay_payment, name="payment"),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("payment-failed/", views.payment_failed, name="payment_failed"),
    path("payment/", views.razorpay_payment, name="payment"),
   

]
