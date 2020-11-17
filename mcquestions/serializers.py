from rest_framework import serializers
from .models import Student 


#Converting a Student Model’s data to JSON/XML format by automatically generate set of fields and automatically generate validator
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student 
        fields = '__all__'

