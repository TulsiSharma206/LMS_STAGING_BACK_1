from django.urls import path
from .views import  login , UserRU, CreateUser, confirmotp, resendotp, resetpassword, passwordchange, logout , ConsultationForm, EnrollForm, BatchList, enrollverify, construcverify, UserPayment, ConfirmPayment, resendcootp, resenderotp, contactUSForm , resendCUotp , contactUSverify , UserPaymentVerify, topicepurchase , topicepurget , userlist, fullcoursep, coursepayment      
from django.contrib.auth import views

urlpatterns = [
    path("api/login/", login, name="login"),
    path('api/profile/<int:pk>/', UserRU.as_view(), name='get assignment'),
    path('api/signup/', CreateUser.as_view(),name="signup"),
    path('api/confirmaccount/', confirmotp,name="confrim otp"),
    path('api/resendotp/', resendotp,name="resend otp"),
    path('api/resetpassword/', resetpassword,name="reset password"),
    path('api/changepassword/', passwordchange,name="reset password"),
    path("api/logout/", logout, name="logout"),

    path('api/consultation/', ConsultationForm.as_view(),name="ConsultationForm"),
    path("api/enroll/", EnrollForm.as_view(), name="Enroll Form"),

    path('api/batch/', BatchList.as_view(),name="List Batch"),

    path("api/everify/", enrollverify, name="enroll verify"),
    path("api/cverify/", construcverify, name="construction verify"),

    path("api/coresendotp/", resendcootp, name="consultation resend otp"),

    path("api/enrollsendotp/", resenderotp, name="enroll resend otp"),

    path("api/contactus/", contactUSForm.as_view(), name="submit contact form"),
    path("api/resentcuotp/", resendCUotp, name="contact resend otp"),
    path("api/contactverify/", contactUSverify, name="Verify contactus"),

    path("api/upayment/", UserPayment, name="User Direct payment"),
    path("api/upverify/", UserPaymentVerify, name="user payment Verify"),
    path("api/cpayment/", ConfirmPayment, name="confirm payment"),

    path("api/topicepur/", topicepurchase, name="topice purchase"),

    path("api/topicepurget/<pk>/", topicepurget, name="topice purchase Get"),

    path("api/userlist/", userlist, name="Alll user list"),

    path("api/coursepurchase/", fullcoursep, name="Full Course Purchase"),

    path("api/coursepayment/", coursepayment, name="Course confirm payment"),
]

