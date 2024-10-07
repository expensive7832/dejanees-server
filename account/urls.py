from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup.as_view(), name="signup"),
    path('verify/<int:id>/<int:code>', views.verify_user, name="verify"),
    path('login/', views.login.as_view(), name="login"),
    path('forgetpassword/', views.verifyemail.as_view(), name="verifyemail"),
    path('verify-otp/', views.verifyotp.as_view(), name="verifyotp"),
    path('password/', views.changepassword, name="passwordchange"),
    path('user/', views.getuser, name="getuser"),
    path('user/<int:id>', views.getuserbyid, name="getuserbyid"),
    path('deleteuser/<int:pk>', views.deleteuser, name="deluserbyid"),
    path('update/<int:pk>', views.updateuser, name="updateuser"),
    path('createstaff/', views.createstaff, name="createstaff"),
    path('staffs/', views.storeStaff, name="staffs"),
    path('allstaffs/', views.AllStaff, name="allstaffs"),
    
    # store
    
    path('phone/', views.addphone, name="phone"),
    path('fetchphone/', views.getphone, name="getphone"),
    
    path('address/', views.addaddress, name="address"),
    path('fetchaddress/', views.getaddress, name="getaddress"),
    
    path('counter/', views.addcounter, name="counter"),
    path('fetchcounter/', views.getcounter, name="getcounter"),
     path('delcounter/<int:pk>', views.deletecounter, name="delcounter"),
    
    path('addclient/', views.addclient, name="client"),
    path('fetchclient/', views.gettrustedclient, name="getclient"),
    path('delclient/<int:id>', views.deleteclient, name="delclient"),
    
    path('addproject/', views.addproject, name="project"),
    path('fetchproject/', views.getproject, name="getproject"),
    path('delproject/<int:id>', views.deleteproject, name="delproject"),
    
    path('addtestimonial/', views.addtestimonial, name="testimonial"),
    path('fetchtestimonial/', views.gettestimonial, name="gettestimonial"),
    path('fetchtestimonialadmin/', views.gettestimonialAdmin, name="gettestimonialadmin"),
    path('deltestimonial/<int:id>', views.deletetestimonia, name="deltestimonial"),
    path('updtestimonial/<int:id>', views.updatetestimonial, name="updestimonial"),


    path('mail/', views.sendEmail.as_view(), name="mail"),

]
