from . import views 
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from. forms import LoginForm,MyPasswordResetForm,MyPasswordChangeForm,MySetPasswordForm
urlpatterns = [
   path("",views.home),
   path("contact/",views.contact,name="contact"),
   path("about/",views.about,name="about"),
   path("category/<slug:val>",views.CategoryView.as_view(),name="category"),
    path("category/<val>",views.CategoryTitle.as_view(),name="category-title"),
   path("product-detail/<int:pk>",views.Productdetail.as_view(),name="product-detail"),
     path('profile/',views.ProfileView.as_view(),name='profile'),
     path('address/',views.address,name='address'),
     path('updateaddress/<int:pk>',views.updateAddress.as_view(),name="updateaddress"),
    path('add-to-cart/',views.add_to_cart,name='add-to-cart'),
   path('cart/',views.show_cart,name='showcart'),
   path('checkout/',views.checkout.as_view(),name='checkout'),
   path('paymentdone/',views.payment_done,name="paymentdone"),
   path("orders/",views.Orderdetails.as_view(),name="order"),

     # login authentication
      path("customer-registartion/",views.CustomerRegistartionView.as_view(),name="customerregistration"),
     path('accounts/login/',auth_view.LoginView.as_view(template_name='login.html',authentication_form=LoginForm),name="login"),# built in login form
     # password rest view
     # change password
     path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='changepassword.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone'),name="passwordchange"),
     path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'),name="passwordchangedone"),

     # logout
     path('logout/',views.logout,name='logout'),

      # forgot password
      path('password-reset/',auth_view.PasswordResetView.as_view(template_name='password_reset.html',form_class=MyPasswordResetForm),name="password-reset"),
     path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name="password_reset_done"),
     path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=MySetPasswordForm),name="password_reset_confirm"),
     path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),

]
if settings.DEBUG:
  urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    