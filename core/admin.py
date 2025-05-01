from django.contrib import admin
from .models import Officer, Customer, Network, DataPackage, Transaction, Payment
from .models import StaffNotification

# Register your models here.

admin.site.register(Officer)
admin.site.register(Customer)
admin.site.register(Network)
admin.site.register(DataPackage)
admin.site.register(Transaction)
admin.site.register(Payment)
admin.site.register(StaffNotification)