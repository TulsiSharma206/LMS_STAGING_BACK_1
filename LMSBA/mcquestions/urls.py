''' This file is regarding the different paths related to the requests from user to the view module'''
from django.urls import path
from .views import AnswerList, SubmitAnswer, StudentCreate , StudentScore, otpverify ,resendotp


urlpatterns = [
    #Call to the AnswerList method in view.py with parameter Answer as request
    path('Answer/', AnswerList,name="All Answer"),

    #Call to the SubmitAnswer method in view.py with two parameter "Answer" as right answer and "pk" as student identification
    path('sAnswer/<pk>/', SubmitAnswer,name="submit Answer"),

    #Use of object of class StudentCreate in view.py in order to view the signup and sending the otp verification
    path('student/', StudentCreate.as_view({'get': 'list', 'post' : 'create'}),name="student signup"),
    
    #Call to the StudentScore method in view.py with two parameter "score" of student and "pk" as student identification
    path('score/<pk>/', StudentScore,name="Student Score"),
    
    #Call to the otpverify in view.py in order to verify otp with one parameter request to verify
    path('verify/', otpverify,name="Verify otp"),

    #Call to the resendotp in view.py in order to redend the otp with one parameter request for resend
    path('resendotp/', resendotp,name="resend otp"),

]
