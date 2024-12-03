# Generated by Django 5.0.3 on 2024-04-24 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.FloatField(default=0.0, help_text="Enter the patient's temperature in Celsius", verbose_name='Temperature (°C)')),
                ('pulse', models.FloatField(default=0.0, help_text="Enter the patient's pulse rate in beats per minute", verbose_name='Pulse (bpm)')),
                ('systolic', models.FloatField(default=0.0, help_text="Enter the patient's systolic blood pressure in mmHg", verbose_name='Systolic Pressure (mmHg)')),
                ('diastolic', models.FloatField(default=0.0, help_text="Enter the patient's diastolic blood pressure in mmHg", verbose_name='Diastolic Pressure (mmHg)')),
                ('hemoglobin', models.FloatField(default=0.0, help_text="Enter the patient's hemoglobin level in grams per deciliter", verbose_name='Hemoglobin (g/dL)')),
                ('rbsk', models.CharField(default='', help_text="Enter the patient's Rashtriya Bal Swasthya Karyakram (RBSK) status", max_length=100, verbose_name='RBSK Status')),
                ('oxygen_count', models.FloatField(default=0.0, help_text="Enter the patient's oxygen count in percentage", verbose_name='Oxygen Count (%)')),
                ('diabetic_value', models.FloatField(default=0.0, help_text="Enter the patient's diabetic value in milligrams per deciliter", verbose_name='Diabetic Value (mg/dL)')),
                ('height', models.FloatField(default=0.0, help_text="Enter the patient's height in centimeters", verbose_name='Height (cm)')),
                ('weight', models.FloatField(default=0.0, help_text="Enter the patient's weight in kilograms", verbose_name='Weight (kg)')),
                ('other_history', models.TextField(default='', help_text='Enter any other relevant medical history', verbose_name='Other Medical History')),
                ('other_complaints', models.TextField(default='', help_text='Enter any other complaints reported by the patient', verbose_name='Other Complaints')),
                ('others_if_any', models.TextField(default='', help_text='Enter any other relevant details', verbose_name='Others if Any')),
                ('present_illness', models.TextField(default='', help_text="Enter details about the patient's present illness", verbose_name='Present Illness')),
                ('family_history', models.TextField(default='', help_text="Enter details about the patient's family medical history", verbose_name='Family History')),
                ('allergies', models.TextField(default='', help_text='Enter any known allergies of the patient', verbose_name='Allergies')),
                ('other_investigations', models.TextField(default='', help_text='Enter details about any other investigations conducted', verbose_name='Other Investigations')),
                ('other_diagnosis', models.TextField(default='', help_text='Enter any other diagnosis made', verbose_name='Other Diagnosis')),
            ],
        ),
    ]