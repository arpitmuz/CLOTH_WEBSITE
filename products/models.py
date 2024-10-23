from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES=(
   ('JS','Jeans'),
   ('ST','Shirts'),
   ('TS','T-Shirts'),
   ('PS','Pants'),
   ('HS','HAlf-Shirts'),
   ('LP','Ladies-pants'),
   ('TP','Tops'),
   ('LG','Leggings')

)


class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image=models.ImageField(upload_to='product/',max_length=250,null=True,default="none")
    def _str_(self):
     return self.title


STATE_CHOICES = (
   ("AN","Andaman and Nicobar Islands"),
   ("AP","Andhra Pradesh"),
   ("AR","Arunachal Pradesh"),
   ("AS","Assam"),
   ("BR","Bihar"),
   ("CG","Chhattisgarh"),
   ("CH","Chandigarh"),
   ("DN","Dadra and Nagar Haveli"),
   ("DD","Daman and Diu"),
   ("DL","Delhi"),
   ("GA","Goa"),
   ("GJ","Gujarat"),
   ("HR","Haryana"),
   ("HP","Himachal Pradesh"),
   ("JK","Jammu and Kashmir"),
   ("JH","Jharkhand"),
   ("KA","Karnataka"),
   ("KL","Kerala"),
   ("LA","Ladakh"),
   ("LD","Lakshadweep"),
   ("MP","Madhya Pradesh"),
   ("MH","Maharashtra"),
   ("MN","Manipur"),
   ("ML","Meghalaya"),
   ("MZ","Mizoram"),
   ("NL","Nagaland"),
   ("OD","Odisha"),
   ("PB","Punjab"),
   ("PY","Pondicherry"),
   ("RJ","Rajasthan"),
   ("SK","Sikkim"),
   ("TN","Tamil Nadu"),
   ("TS","Telangana"),
   ("TR","Tripura"),
   ("UP","Uttar Pradesh"),
   ("UK","Uttarakhand"),
   ("WB","West Bengal")
)

class Customer(models.Model):
   user=models.ForeignKey(User,on_delete=models.CASCADE)
   name=models.CharField(max_length=200)
   locality=models.CharField(max_length=200)
   city=models.CharField(max_length=50)
   mobile=models.IntegerField(default=0)
   zipcode=models.IntegerField()
   state=models.CharField(choices=STATE_CHOICES,max_length=100)

   def _str_(self):
      return self.name
   


class Cart(models.Model):
   user=models.ForeignKey(User,on_delete=models.CASCADE)
   products=models.ForeignKey(Product,on_delete=models.CASCADE)
   quantity=models.PositiveIntegerField(default=1)

   @property # used to find the total cost
   def total_cost(self):
      return self.quantity *self.products.discounted_price

STATUS_CHOICES =(
   ('Accepted','Accepted'),
   ('Packed','Packed'),
   ('On The Way','On The Way'),
   ('Delivered','Delivered'),
   ('Cancel','Cancel'),
   ('Pending','Pending'),
)


class Payment(models.Model):
   user=models.ForeignKey(User,on_delete=models.CASCADE)
   amount=models.FloatField()
   razorpay_order_id=models.CharField(max_length=100,blank=True,null=True)
   razorpay_payment_status=models.CharField(max_length=100,blank=True,null=True)
   razorpay_payment_id=models.CharField(max_length=100,blank=True,null=True)
   paid=models.BooleanField(default=False)




class OrderPlaced(models.Model):
   user=models.ForeignKey(User,on_delete=models.CASCADE)
   customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
   product=models.ForeignKey(Product,on_delete=models.CASCADE)
   quantity=models.PositiveIntegerField(default=1)
   ordered_date=models.DateTimeField(auto_now_add=True)
   status=models.CharField(max_length=50,choices=STATUS_CHOICES,default="Pending")
   payment=models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
   
   
   @property
   def total_cost(self):
      return self.quantity *self.product.discounted_price