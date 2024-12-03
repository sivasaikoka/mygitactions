from django.db import models

class Consultation(models.Model):
    temperature = models.FloatField(verbose_name='Temperature (°C)', default=0.0, help_text='Enter the patient\'s temperature in Celsius')
    pulse = models.FloatField(verbose_name='Pulse (bpm)', default=0.0, help_text='Enter the patient\'s pulse rate in beats per minute')
    systolic = models.FloatField(verbose_name='Systolic Pressure (mmHg)', default=0.0, help_text='Enter the patient\'s systolic blood pressure in mmHg')
    diastolic = models.FloatField(verbose_name='Diastolic Pressure (mmHg)', default=0.0, help_text='Enter the patient\'s diastolic blood pressure in mmHg')
    hemoglobin = models.FloatField(verbose_name='Hemoglobin (g/dL)', default=0.0, help_text='Enter the patient\'s hemoglobin level in grams per deciliter')
    rbsk = models.CharField(verbose_name='RBSK Status', max_length=100, default='', help_text='Enter the patient\'s Rashtriya Bal Swasthya Karyakram (RBSK) status')
    oxygen_count = models.FloatField(verbose_name='Oxygen Count (%)', default=0.0, help_text='Enter the patient\'s oxygen count in percentage')
    diabetic_value = models.FloatField(verbose_name='Diabetic Value (mg/dL)', default=0.0, help_text='Enter the patient\'s diabetic value in milligrams per deciliter')
    height = models.FloatField(verbose_name='Height (cm)', default=0.0, help_text='Enter the patient\'s height in centimeters')
    weight = models.FloatField(verbose_name='Weight (kg)', default=0.0, help_text='Enter the patient\'s weight in kilograms')
    other_history = models.TextField(verbose_name='Other Medical History', default='', help_text='Enter any other relevant medical history', null=False)
    other_complaints = models.TextField(verbose_name='Other Complaints', default='', help_text='Enter any other complaints reported by the patient', null=False)
    others_if_any = models.TextField(verbose_name='Others if Any', default='', help_text='Enter any other relevant details', null=False)
    present_illness = models.TextField(verbose_name='Present Illness', default='', help_text='Enter details about the patient\'s present illness', null=False)
    family_history = models.TextField(verbose_name='Family History', default='', help_text='Enter details about the patient\'s family medical history', null=False)
    allergies = models.TextField(verbose_name='Allergies', default='', help_text='Enter any known allergies of the patient', null=False)
    other_investigations = models.TextField(verbose_name='Other Investigations', default='', help_text='Enter details about any other investigations conducted', null=False)
    other_diagnosis = models.TextField(verbose_name='Other Diagnosis', default='', help_text='Enter any other diagnosis made', null=False)

    def __str__(self):
        return f'Consultation ID: {self.pk}'
