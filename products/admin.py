from django.contrib import admin
from  . models import Product,Customer,Cart,OrderPlaced,Payment
# Register your models here.
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','title','discounted_price','selling_price','description','product_image']
admin.site.register(Product,ProductModelAdmin)


class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','locality','city','state','zipcode']
admin.site.register(Customer,CustomerModelAdmin)

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','products','quantity']


class PaymentModelAdmin(admin.ModelAdmin):
    list_display=['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']
admin.site.register(Payment,PaymentModelAdmin)
class OrderPlacedAdmin(admin.ModelAdmin):
     list_display=['id','user','product','quantity','ordered_date','status','payment']
admin.site.register(OrderPlaced,OrderPlacedAdmin)