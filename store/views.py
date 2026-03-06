from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Product, OrderItem
import razorpay


def home(request):
    return render(request, "home.html")


def checkout(request):
    return render(request, "checkout.html")


def place_order(request):

    if request.method == "POST":

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        pincode = request.POST.get("pincode")
        payment_method = request.POST.get("payment_method")
        amount = request.POST.get("amount")

        # Save order
        order = Order.objects.create(
            customer_name=name,
            phone=phone,
            address=address,
            pincode=pincode,
            payment_mode=payment_method,
            payment_status="Pending",
            total_amount=amount
        )

        product = Product.objects.first()

        if product:
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=1
            )

        # COD flow
        if payment_method == "cod":

            items = OrderItem.objects.filter(order=order)

            return render(request, "success.html", {
                "order": order,
                "items": items
            })

        # Razorpay flow
        elif payment_method == "razorpay":

            return redirect("/payment/?amount=" + str(amount))

    return redirect("/")


def razorpay_payment(request):

    amount = request.GET.get("amount")

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    payment = client.order.create({
        "amount": int(amount) * 100,
        "currency": "INR",
        "payment_capture": 1
    })

    context = {
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "payment": payment,
        "amount": amount
    }

    return render(request, "payment.html", context)


@csrf_exempt
def payment_success(request):

    payment_id = request.GET.get("razorpay_payment_id")
    amount = request.GET.get("amount")

    order = Order.objects.create(
        customer_name="Online Customer",
        phone="9999999999",
        address="Customer Address",
        pincode="600001",
        payment_mode="Online",
        payment_status="Paid",
        payment_id=payment_id,
        total_amount=amount
    )

    product = Product.objects.first()

    if product:
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1
        )

    items = OrderItem.objects.filter(order=order)

    return render(request, "success.html", {
        "order": order,
        "items": items
    })


def payment_failed(request):
    return render(request, "payment_failed.html")