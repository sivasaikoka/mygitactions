from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    occupation = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    height = models.FloatField()
    weight = models.FloatField()
    bmi = models.FloatField()
    bp_value = models.CharField(max_length=20)
    diabetes = models.CharField(max_length=10)
    energy_levels = models.CharField(max_length=20)
    sleep_issues = models.CharField(max_length=20)
    diet = models.CharField(max_length=100)
    physical_activity_level = models.CharField(max_length=20)
    smoking_alcohol = models.CharField(max_length=20)
    mental_health = models.CharField(max_length=20)
    symptoms = models.JSONField()
    family_history = models.TextField()
    diagnosis_conditions = models.TextField()
    ayush_practices = models.TextField()

class Beneficiary(models.Model):
    id = models.AutoField(primary_key=True)
    beneficiary_id = models.IntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    oxygen_count = models.FloatField()
    temperature = models.FloatField()
    pulse_rate = models.FloatField()
    diabetic_value = models.FloatField()
    systolic = models.FloatField()
    diastolic = models.FloatField()
    capture_date = models.DateTimeField(auto_now_add=True)

class Prediction(models.Model):
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE)
    prediction_date = models.DateField()
    predicted_bmi = models.FloatField()
    predicted_diabetic_value = models.FloatField()
    predicted_systolic = models.FloatField()
    predicted_diastolic = models.FloatField()