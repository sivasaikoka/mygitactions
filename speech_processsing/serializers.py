from rest_framework import serializers
from .models import VoiceInput

class VoiceInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceInput
        fields = '__all__'
