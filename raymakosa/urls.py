"""
URL configuration for raymakosa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import CustomerViewSet, NetworkViewSet, DataPackageViewSet, TransactionViewSet, PaymentViewSet
from django.contrib.auth import logout  # Add this import
from core.views import login_view, logout_view, admin_dashboard, disburse_data, payment_page
from core.views import index, buy_data, confirm_payment


router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'networks', NetworkViewSet)
router.register(r'data-packages', DataPackageViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'payments', PaymentViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path("", index, name="index"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("disburse/<int:transaction_id>/", disburse_data, name="disburse_data"),
    path("payment/<int:transaction_id>/", payment_page, name="payment"),
    path("buy/", buy_data, name="buy_data"),
    path("confirm_payment/<int:transaction_id>/", confirm_payment, name="confirm_payment"),
    
]



