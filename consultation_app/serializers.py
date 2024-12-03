from rest_framework import serializers

class VitalHistorySerializer(serializers.Serializer):
    temperature = serializers.CharField()
    pulse = serializers.CharField()
    systolic = serializers.CharField()
    diastolic = serializers.CharField()
    hemoglobin = serializers.CharField()
    rbsk = serializers.CharField()
    oxygen_count = serializers.CharField()
    diabetic_value = serializers.CharField()
    height = serializers.CharField()
    weight = serializers.CharField()
    history = serializers.CharField(default="no")  # Ensure 'history' is present with default value

class OtherHistorySerializer(serializers.Serializer):
    history = serializers.CharField(default="no")  # Ensure 'history' is present with default value

class CCBriefHistorySerializer(serializers.Serializer):
    chiefComplaints = serializers.ListField(child=serializers.DictField())
    otherComplaints = serializers.CharField()
    othersifany = serializers.CharField()
    presentIllness = serializers.CharField()
    familyhistory = serializers.CharField()
    history = serializers.CharField(default="no")  # Ensure 'history' is present with default value

class AllergySerializer(serializers.Serializer):
    allergies = serializers.CharField()
    history = serializers.CharField(default="no")  # Ensure 'history' is present with default value

class InvestigationSerializer(serializers.Serializer):
    master = serializers.ListField()
    otherInvestigation = serializers.CharField()
    history = serializers.CharField(default="no")  # Ensure 'history' is present with default value

class DiagnosisSerializer(serializers.Serializer):
    provisionalDiagnosis = serializers.ListField()
    othersifany = serializers.CharField()
    history = serializers.CharField(default="no")  # Ensure 'history' is present with default value

class InputDataSerializer(serializers.Serializer):
    vital_history = VitalHistorySerializer()
    other_history = OtherHistorySerializer()
    cc_brief_history = CCBriefHistorySerializer()
    allergy = AllergySerializer()
    investigation = InvestigationSerializer()
    diagnosis = DiagnosisSerializer()

class OutputDataSerializer(serializers.Serializer):
    type_of_consultation_prediction = serializers.DictField()
    prescribed_medications_prediction = serializers.DictField()
    advice_prediction = serializers.DictField()
