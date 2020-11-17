''' This file is regarding the data delivering to the models and class and it decides what data 
to be delivered to them. that is by acting on the responses from the user '''

#importing inbuilt modules

from rest_framework import generics
from django.shortcuts import render
from .models import Student, StudentProgress ,Mcquestions, StudentPercentage, NumberOfQuestions
from .serializers import StudentSerializer
from django.db.models import Count
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
import os
from pathlib import Path
import random
from random import randint
from json import loads
from django.http import JsonResponse
from django.forms.models import model_to_dict
from datetime import datetime
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.authtoken.models import Token
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT= os.path.join(os.path.dirname(BASE_DIR), "media_root")

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client as TwilioClient

#authentication of communication between two 
account_sid = "AC65cd733f82e2d44cc6a460546243d3b3"
auth_token = "6ac559bb61cfe80a7ec91091a0fd1482"
twilio_phone = "+12513552160"
client = TwilioClient(account_sid, auth_token)


class StudentCreate(ModelViewSet):

    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    #parser class for accepting requests from various media types
    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        mobile_number = self.request.data.get('mobile')

        #filtering the email and phone number from the query set of student object
        data = Student.objects.filter(Q(email__exact=self.request.data.get('email')) | Q(mobile__exact=self.request.data.get('mobile')))
        
        otp = randint(100000, 999999)
        
        if len(data) == 0:
            if self.request.data.get('image')  == None:
                return JsonResponse(dict(detail="Please capture Images"), status=403)
            else:
                #otp send to register phone number
                try:
                    client.messages.create(
                        body="Please Enter This Otp " + str(otp) + " To Register at AspirenowGlobal",
                        from_=twilio_phone,
                        to=mobile_number
                    )
                    #save the details of student details
                    serializer.save(name=self.request.data.get('name'), email=self.request.data.get('email'), mobile=mobile_number, level=self.request.data.get('level'), image=self.request.data.get('image'),otp_at = datetime.now(), otp = otp)
                    data=Student.objects.get(email=self.request.data.get('email'))
                    filename = str(data.image)
                    data.image = filename+".jpeg"
                    data.save()
                    os.rename(MEDIA_ROOT+"/"+filename, MEDIA_ROOT+"/"+filename+".jpeg")
                    return JsonResponse(status=202,data={'200':'Otp send successfully'})

                #mobile number not registered    
                except TwilioRestException:
                    return JsonResponse(status=403,data={'403':'Mobile Number Invalid'})
        else:
            verifydata = Student.objects.get(mobile=mobile_number)
            if verifydata.varifed  == False:
                return JsonResponse(data={'201':'resent otp'}) 
            return JsonResponse(status=202,data={'402':'you already register'})


@csrf_exempt 
@api_view(["POST"])
#Verification of Mobile number using OTP
def otpverify(request): 
    mobile_number = request.data['mobile_number']
    otp = int(request.data['otp'])
    try:
        user = Student.objects.get(mobile=mobile_number)
    except:
        return JsonResponse(dict(detail="Mobile number Invalid"))
    
    otp_timestamp = user.otp_at.replace(tzinfo=None).timestamp()
    current_timestamp = datetime.now().timestamp()
    e = current_timestamp - otp_timestamp
    
    #Check the expiration of OTP
    if e < 550:
        if otp == int(user.otp):
            user.varifed = True
            user.save()
            return JsonResponse(dict(detail="Verify Successfully", id = user.id),status=200,)
        else:
            return JsonResponse(dict(detail="Renter the Code"),status=401,)
    else:
        return JsonResponse(dict(detail=" OTP expired"),status=401,)


@csrf_exempt 
@api_view(["POST"])
#Resending of OTP 
def resendotp(request): 
    mobile_number = request.data['mobile_number']
    try:
        user = Student.objects.get(mobile=mobile_number)
        #OTP generated
        otp = randint(100000, 999999)
        #OTP send to registered phone number
        try:   
            client.messages.create(
                body="Your verification code is " + str(otp),
                from_=twilio_phone,
                to=mobile_number
            )
            user.otp = otp 
            user.otp_at = datetime.now()
            user.save()
            return JsonResponse(status=202,data={'200':'Otp send successfully'})
        except TwilioRestException:
            return JsonResponse(status=403,data={'403':'Mobile Number Invalid'})
    except:
        return JsonResponse(dict(detail="Mobile Number Invalid"))


@csrf_exempt 
@api_view(["GET","POST"])
#Getting list of options available for Mcquestion
def AnswerList(request): 
    Number_of_Questions = NumberOfQuestions.objects.get(id=1)
    Question_data = Mcquestions.objects.all().values('id',"question", 'text1', 'text2', 'text3').order_by('?')[0:int(num.multiplechoice)]
    return Response({"status": "Progress","qdata":Question_data})
        
   
@csrf_exempt 
@api_view(["POST"])
#Submitting the answer
def SubmitAnswer(request,pk): 
    for i in request.data:
        #Checking for answer 
        try:
            #searching for marked answer
            data=Mcquestions.objects.get(id=request.data[i]['id'],is_correct=request.data[i]['answer'])
            #checking for marked answer is right or not 
            StudentProgress.objects.create(student_id=pk,question_id=request.data[i]['id'],is_right=True)
        except ObjectDoesNotExist:
            #if marked answer is wrong
            StudentProgress.objects.create(student_id=pk,question_id=request.data[i]['id'],is_right=False)
    return Response({"status": "Thanks For Submitting the answer"})

@csrf_exempt 
@api_view(["GET"])
#The percentage of student Test
def StudentScore(request,pk): 
    totalquestions = StudentProgress.objects.filter(student_id=pk).count()
    #get total corrected answers
    totalcorrect = StudentProgress.objects.filter(student_id=pk, is_right= True).count()
    #calculate the percentage
    percentage = int((totalcorrect / totalquestions) * 100)

    
    try:
        coupan = StudentPercentage.objects.get(student_id=pk)
        #generating the coupancode
        coupancode = coupan.coupancode
    except ObjectDoesNotExist:
        coupancode = ''.join(random.choice('0123456789ABCDEF') for i in range(6))
        print("coupancode", coupancode)
        coupanc = StudentPercentage.objects.create(student_id=pk,percentag=percentage,coupancode=str(coupancode))
    #checking for scholarship based on the persentage
    if percentage >= 90:
        return Response({"status": "Congratulations", " your efficiency is " : percentage," Discount ": "You are eligible for 25% Scholarship", "coupancode" :coupancode})
    elif percentage >= 80:
        return Response({"status": "Congratulations", " your efficiency is " : percentage, " Discount ": "You are eligible for 20% Scholarship", "coupancode" :coupancode})
    elif percentage >= 70:
        return Response({"status": "Congratulations", " your efficiency is " : percentage, " Discount ": "You are eligible for 10% Scholarship", "coupancode" :coupancode})
    elif percentage >= 60:
        return Response({"status": "Congratulations", "your efficiency is " : percentage, " Discount ": "You are eligible for 5% Scholarship"})
    else:
        cou = StudentPercentage.objects.get(student_id=pk)
        cou.coupancode = "N/A"
        cou.save()
        return Response({"status": "Better Luck Next Time", " percentage " : percentage })   

