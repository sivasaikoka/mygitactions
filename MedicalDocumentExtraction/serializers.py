# from rest_framework import serializers
# from .models import Prescription

# class FileUploadSerializer(serializers.Serializer):
#     class Meta:
#         model=Prescription
#         field='__all__'



from rest_framework import serializers
from .models import Prescription

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'
