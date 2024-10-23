from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
# Create your views here
from . models import Product,Customer,Cart,Payment,OrderPlaced
from . forms import CustomerRegistrationform,CustomerProfileForm
from django.contrib import messages
import razorpay
from django.conf import settings
from django.contrib.auth.models import AnonymousUser


def order(request):
    return render(request,"order.html")

def home(request):
    return render(request,"index.html")
def contact(request):
    return render(request,"contact.html")
def about(request):
    return render(request,"about.html")
class CategoryView(View):
    def get(self,request,val):
        product=Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title')
        return render(request,"category.html",locals())

class CategoryTitle(View):
    def get(self,request,val):
        product=Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        return render(request,"category.html",locals())
class Productdetail(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        return render(request,"productdetail.html",locals())


class CustomerRegistartionView(View):
    def get(self,request):
        form=CustomerRegistrationform()
        return render(request,'customerregistartion.html',locals())
    
    def post(self,request):
        form=CustomerRegistrationform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'customerregistartion.html',locals())
    

class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,'profile.html',locals())
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']

            reg=Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! Profile register Successfully")
        else:
           messages.warning(request,"Invalid Input Data")
        return render(request,'profile.html',locals())
    

def address(request):
    address=Customer.objects.filter(user=request.user)
    return render(request,'address.html',locals())


class updateAddress(View):
     def get(self,request,pk):
         add=Customer.objects.get(pk=pk)
         form=CustomerProfileForm(instance=add)
         return render(request,'updateaddress.html',locals())
     def post(self,request,pk):
         form=CustomerProfileForm(request.POST)
         if form.is_valid():
             add=Customer.objects.get(pk=pk)
             add.name=form.cleaned_data['name']
             add.locality=form.cleaned_data['locality']
             add.city=form.cleaned_data['city']
             add.mobile=form.cleaned_data['mobile']
             add.state=form.cleaned_data['state']
             add.zipcode=form.cleaned_data['zipcode']
             add.save()
             messages.success(request,"Congratulations! Address Updated Successfully")
         else:
           messages.warning(request,"Invalid Input Data")
         return redirect("address")
def logout(request):
    return redirect("login")
    

#  used to add the items in database table
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,products=product).save()
    return redirect("/cart")

# used to dispaly the cart
def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.quantity* p.products.discounted_price
        amount=amount+value
    totalamount=amount+40
   
    return render(request,'addtocart.html',locals())


class checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=request.user)
        cart_items=Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value=p.quantity* p.products.discounted_price
            famount=famount+value
        totalamount=famount +40
        razoramount=int(totalamount *100)# for converting in RS
        client=razorpay.Client(auth=("rzp_test_j33IPGv9e7LhhJ", "cmy1U2aJPtcas3zY5t4xoK9L"))
        data={"amount":razoramount,"currency":"INR"}
        payment_response=client.order.create(data=data)
        print(payment_response)
        order_id=payment_response['id']
        order_status=payment_response['status']
        if order_status== 'created':
            payment=Payment(
              user=user,
              amount=totalamount,
              razorpay_order_id=order_id,
              razorpay_payment_status=order_status

            )
            payment.save()
       

        return render(request,"checkout.html",locals())
    
def payment_done(request):
    
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    print(order_id, payment_id, cust_id)
    
    customer=Customer.objects.get(id=cust_id)
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid=True
    payment.razorpay_payment_id=payment_id
    payment.save()
    user=request.user
    print(user)
    if isinstance(user,AnonymousUser):
        return redirect("/contact")
    # to save order details
    else:
         cart=Cart.objects.filter(user=user)
         for c in cart:
             OrderPlaced(user=user,customer=customer,product=c.products,quantity=c.quantity,payment=payment,status="Accepted").save()
             c.delete()
    return redirect("/orders")

class Orderdetails(View):
    def get(self,request,):
        Orderdetails=OrderPlaced.objects.filter(status="Accepted")
        Orderdetails = Orderdetails[::-1]
        return render(request,"order.html",locals())








    


