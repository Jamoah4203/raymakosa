from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Officer(AbstractUser):
    """User model for officers managing the transactions"""

    groups = models.ManyToManyField(Group, related_name="officer_set")
    user_permissions = models.ManyToManyField(Permission, related_name="officer_set")

    class Meta:
        app_label = "core"

class Customer(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.phone_number

class Network(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class DataPackage(models.Model):
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    package_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.package_name} - {self.network.name}"

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    data_package = models.ForeignKey(DataPackage, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.payment_status}"

class Payment(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Transaction {self.transaction.id}"

class StaffNotification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
