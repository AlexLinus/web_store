from django.contrib import admin
from .models import Order, OrderItem, Cart
# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'phone', 'create_date']
#    inlines = [OrderItemInline]
#
    class Meta:
       model = Order

admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)
