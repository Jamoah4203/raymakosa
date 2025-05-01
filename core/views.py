import requests
from django.shortcuts import render, redirect
from rest_framework import viewsets
from django.contrib.auth import authenticate, login, logout  # Added logout import
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .models import Customer, Network, DataPackage, Transaction, Payment, StaffNotification  # Combined model imports
from .serializers import CustomerSerializer, NetworkSerializer, DataPackageSerializer, TransactionSerializer, PaymentSerializer

# User login
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("admin_dashboard")  # Redirect to dashboard after login
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")

# Admin dashboard
@login_required
def admin_dashboard(request):
    transactions = Transaction.objects.all()
    return render(request, "admin_dashboard.html", {"transactions": transactions})

# User logout
def logout_view(request):
    logout(request)
    return redirect("login")

# Disburse Data (Fixed Duplicate Function)
@login_required
def disburse_data(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    if transaction.payment_status == "Paid":
        transaction.payment_status = "Completed"
        transaction.save()

        # Save notification
        StaffNotification.objects.create(message=f"Transaction {transaction.id} successfully disbursed.")

        messages.success(request, "Data Disbursed Successfully!")
        return redirect("admin_dashboard")

    messages.error(request, "Transaction not paid yet.")
    return redirect("admin_dashboard")

# Show homepage with available networks and packages
def index(request):
    networks = Network.objects.all()
    packages = DataPackage.objects.all()
    return render(request, "index.html", {"networks": networks, "packages": packages})

# Handles data purchase request
def buy_data(request):
    if request.method == "POST":
        phone_number = request.POST["phone_number"]
        network_id = request.POST["network"]
        package_id = request.POST["data_package"]

        network = Network.objects.get(id=network_id)
        package = DataPackage.objects.get(id=package_id)

        customer, created = Customer.objects.get_or_create(phone_number=phone_number)

        transaction = Transaction.objects.create(
            customer=customer,
            network=network,
            data_package=package,
            amount=package.price,
            payment_status="Pending",
        )

        return redirect("payment", transaction_id=transaction.id)

    return redirect("index")

# Payment confirmation page
def payment_page(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return render(request, "payment.html", {"transaction": transaction})

# Mock payment API confirmation
def confirm_payment(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    if transaction.payment_status == "Pending":
        transaction.payment_status = "Paid"
        transaction.save()

        # Simulated confirmation message
        return JsonResponse({"message": "Payment successful! Your transaction is now being processed."})

    return JsonResponse({"message": "Payment already confirmed."})

    return redirect("index")

# API ViewSets
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class NetworkViewSet(viewsets.ModelViewSet):
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer

class DataPackageViewSet(viewsets.ModelViewSet):
    queryset = DataPackage.objects.all()
    serializer_class = DataPackageSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
