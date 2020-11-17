''' This file is regarding the different functions provided by the Mcquestion Module of the LMS project
        The different functions provided are:
         1. Student: This is meant for adding the new students.
         2. McQuestion: This is meant for adding the new questions along with their answers.
         3. Student Progress: This is meant for showing the answered question given by student.
         4. Student percentage: This is meant for giving performance of student.
         5. Number of Questions: This is meant for dividing the questions into mock nad assesment questions. 
         '''
#importing the inbuilt modules
from django.db import models
from django.utils import timezone
from user.models import User

#Model for adding the Student details
class Student(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    image = models.FileField(upload_to="studentimages")
    otp = models.CharField(max_length=17, blank=True, null=True)
    otp_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    varifed = models.BooleanField(default=False)
    def __str__(self):
        return self.name

#Model for adding Mcquestions along with right answer
class Mcquestions(models.Model):
    question = models.CharField(max_length=255)
    text1 = models.CharField(max_length=255)
    text2 = models.CharField(max_length=255)
    text3 = models.CharField(max_length=255)
    is_correct = models.CharField(max_length=255)

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name = "Mcquestions"
        verbose_name_plural = "Mcquestions"

#Model gives number of questions answered by the student
class StudentProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='StudentProgress')
    question = models.ForeignKey(Mcquestions, on_delete=models.CASCADE, related_name='StudentAnswers')
    is_right = models.BooleanField(default=False)
    class Meta:
        verbose_name = "StudentProgress"
        verbose_name_plural = "StudentProgress"


#Model for adding the percentage of Test given by Student
class StudentPercentage(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='StudentPercentage')
    percentag = models.CharField(max_length=255, verbose_name='percentage')
    created_at = models.DateTimeField(auto_now_add=True)
    coupancode = models.CharField(max_length=255, verbose_name='coupan code')

#Model for dividing Mcquestions  into mock questions and assement question.
class NumberOfQuestions(models.Model):
    multiplechoice = models.CharField(max_length=255, verbose_name='number of questions show in mcquestions')
    mock = models.CharField(max_length=255, verbose_name='number of questions show in mock')
    assement = models.CharField(max_length=255, verbose_name='number of questions show in assement')
    
    class Meta:
        verbose_name = "NumberOfQuestions"
        verbose_name_plural = "NumberOfQuestions"
