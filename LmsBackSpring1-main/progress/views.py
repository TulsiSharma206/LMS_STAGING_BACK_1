from django.shortcuts import render
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from .models import TeacherProgre, Batches, StudentProgres
from course.models import Count ,Course, Chapter ,FileUpload, Purchase 
from rest_framework.authtoken.models import Token
from user.models import User


@csrf_exempt 
@api_view(["GET"])
def teacherlist(request):
    userinfo = User.objects.filter(is_active=True, is_staff=True).values('id','email')
    return Response({'userinfo' : userinfo})


@csrf_exempt
@api_view(["GET"])
def batchlist(request):
    data = Batches.objects.all().values('id', 'name')
    return Response({'data': data})


@csrf_exempt
@api_view(["GET"])
def coursecomplete(request):
    data = Course.objects.all().values('id', 'title', 'image')
    return Response({'data': data})


@csrf_exempt
@api_view(["GET"])
def chaptercount(request, pk):
    data = Chapter.objects.filter(course_id=pk).values('id', 'title')
    return Response({'data': data})

@csrf_exempt
@api_view(["GET"])
def mediacount(request, pk):
    data = FileUpload.objects.filter(chapter_id=pk).values('id', 'name')
    return Response({'data': data})


@csrf_exempt
@api_view(["POST"])
def teacherprogres(request):
    batchid = request.data['batchid']
    coursid = request.data['coursid']
    teacherid = request.data['teacherid']
    chapterid = request.data['chapterid']
    mediaid = request.data['mediaid']
    half = request.data['half']
    full = request.data['full']

    chaptercount = Chapter.objects.filter(course_id=coursid).count()  
    
    chapterper = (100 / float(chaptercount))
    
    mediacount = FileUpload.objects.filter(chapter_id=chapterid).count()  
    
    mediaper = (chapterper / float(mediacount))
    
    if full == "1":
        videoweight = float(mediaper)
    else:
        videoweight = (float(mediaper) / 2)
    
    try:
        tw = TeacherProgre.objects.get(media_id = mediaid)
        if full == "1":
            tw.fullcomplete = True
        else :
            tw.partialcomplete = True
        tw.weight = videoweight
        tw.save()
    except ObjectDoesNotExist:
        twdata = TeacherProgre.objects.create(batch_id =batchid, student_id=teacherid, course_id = coursid, chapter_id= chapterid, media_id = mediaid, weight=videoweight)
        if full == "1":
            twdata.fullcomplete = True
        else :
            twdata.partialcomplete = True
        twdata.save()
    return Response({'Status': 200})


def Teacherpro(request):
    return render(request, "progress/teacherprogres.html")


# Current we assign static batch id "1" but after we assign dynamic batch id according user token get user which batch presents and that batch used this
# batch connect user Foreign Key
@csrf_exempt
@api_view(["POST"])
def teacherprogresdata(request):
    batchid = request.data['batchid']

    t = request.META['HTTP_AUTHORIZATION']
    try:
        userid = Token.objects.get(key=t)
        user = int(userid.user.id)
        if userid.user.id is None:
            return Response({"Fail": "User Not Login"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = Course.objects.filter(id__in=Purchase.objects.filter(purchaseuser=userid.user).values('cours'),status=True).values('id')

            j = 0
            # Here Batch id we used user table get batchid and used here
            for i in TeacherProgre.objects.filter(batch_id =batchid).values('weight'):
                j += float(i['weight'])
            print("j", j)

            return Response({"coursecount": data.count(), "weight" : j})
    except ObjectDoesNotExist:
        return Response({"Fail": "Session Logout"})



# Particular Chapter progress
#@csrf_exempt
#@api_view(["GET"])
#def progress(request,pk): # Pk Course id
#    t = request.META['HTTP_AUTHORIZATION']
#    userid=Token.objects.get(key=t)
#    userv=userid.user.id
#    if userv is None:
#        return Response({"Fail": "User Not Login"}, status=status.HTTP_400_BAD_REQUEST)
#    else:
#        complete = Count.objects.filter(user_id=userv, is_complete=True).count()
#        Chaptervideos = FileUpload.objects.filter(id__in=Purchase.objects.filter(purchaseuser=userid.user, cours_id=pk ,status=True).values('media')).count()
#        if complete !=0:
#
#            #prog = int( (complete/ Chaptervideos) * 100 )
#            try:
#                progress = StudentProgress.objects.get(student_id=userv,course_id=pk)
#                progress.total = Chaptervideos
#                progress.complete = comple
#                progress.save()
#            except ObjectDoesNotExist:
#                progress = StudentProgress.objects.create(student_id=userv,course_id=pk, total=Chaptervideos, complete=complete)
#            #return Response({"Status": prog})
#            return Response({"complete": complete, "Chaptervideos": Chaptervideos})
#
#            return Response({"Status": "Student not start that courses"})
#        else:
#            complete = "0"
#            return Response({"complete": complete, "Chaptervideos": Chaptervideos})



@csrf_exempt
@api_view(["POST"])
def stprogress(request):
    t = request.META['HTTP_AUTHORIZATION']
    userid=Token.objects.get(key=t)
    userv=userid.user.id
    coursid = request.data['coursid']
    #chapterid = request.data['chapterid']
    mediaid = request.data['mediaid']
    videolen = request.data['videolen']

    data = FileUpload.objects.get(id=mediaid)
    chapterid=data.chapter.id


    chaptercount = Chapter.objects.filter(course_id=coursid).count()
    chapterper = (100 / float(chaptercount))
    mediacount = FileUpload.objects.filter(chapter_id=chapterid).count()
    mediaper = (chapterper / float(mediacount))
    vidchunks = round(mediaper / 3, 2)

    try :
        progres = StudentProgres.objects.get(student_id=userv, course_id=coursid, chapter_id=chapterid, media_id=mediaid)
        if videolen  >  progres.videolen:
            progres.weight += vidchunks
            progres.videolen = videolen
            progres.save()
        return Response({"Status": "Stored Successfully"}, status=201)
    except ObjectDoesNotExist:
        StudentProgres.objects.create(student_id=userv, course_id=coursid, chapter_id=chapterid, media_id=mediaid,videolen=videolen, weight=0)
        return Response({"Status": "Created Successfully"}, status=200)


@csrf_exempt
@api_view(["GET"])
def studentprogress(request):
    t = request.META['HTTP_AUTHORIZATION']
    try:
        userid = Token.objects.get(key=t)
        user = int(userid.user.id)
        if userid.user.id is None:
            return Response({"Fail": "User Not Login"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            allcourse =  Course.objects.filter(id__in=Purchase.objects.filter(purchaseuser=userid.user).values('cours'),status=True).count()
            allchapter =  Chapter.objects.filter(id__in=Purchase.objects.filter(purchaseuser=userid.user).values('chapter')).count()
            allweight =  StudentProgres.objects.filter(student_id=user).values('weight')
            return Response({"allweight": allweight, "allchapter":allchapter, "allcourse": allcourse})
    except ObjectDoesNotExist:
        return Response({"Fail": "Session Logout"})
