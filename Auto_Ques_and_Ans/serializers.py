from rest_framework import serializers
from .models import QuestionInput

class QuestionInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionInput
        fields = '__all__'
