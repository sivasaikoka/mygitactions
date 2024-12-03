from django import forms

class VitalHistoryForm(forms.Form):
    temperature = forms.DecimalField(label='Temperature (in Celsius)', help_text='Enter temperature in Celsius (e.g., 37.5)')
    pulse = forms.IntegerField(label='Pulse (beats per minute)', help_text='Enter pulse rate in beats per minute (e.g., 72)')
    systolic = forms.IntegerField(label='Systolic Blood Pressure (mmHg)', help_text='Enter systolic blood pressure in mmHg (e.g., 120)')
    diastolic = forms.IntegerField(label='Diastolic Blood Pressure (mmHg)', help_text='Enter diastolic blood pressure in mmHg (e.g., 80)')
    hemoglobin = forms.DecimalField(label='Hemoglobin (g/dL)', help_text='Enter hemoglobin level in g/dL (e.g., 14)')
    rbsk = forms.CharField(label='RBSK (e.g., normal)', help_text='Enter RBSK status (e.g., normal)')
    oxygen_count = forms.DecimalField(label='Oxygen Count (%)', help_text='Enter oxygen count in percentage (e.g., 98)')
    diabetic_value = forms.DecimalField(label='Diabetic Value (mg/dL)', help_text='Enter diabetic value in mg/dL (e.g., 100)')
    height = forms.DecimalField(label='Height (in cm)', help_text='Enter height in centimeters (e.g., 175)')
    weight = forms.DecimalField(label='Weight (in kg)', help_text='Enter weight in kilograms (e.g., 70)')
    history = forms.CharField(label='History', initial='no')  # Default value 'no'

class OtherHistoryForm(forms.Form):
    history = forms.CharField(label='History', initial='no')  # Default value 'no'

class CCBriefHistoryForm(forms.Form):
    chiefComplaints = forms.CharField(label='Chief Complaints', help_text='Enter chief complaints separated by commas (e.g., Headache, Stomach pain)')
    otherComplaints = forms.CharField(label='Other Complaints', help_text='Enter any other complaints (e.g., Fever)', initial='')
    othersifany = forms.CharField(label='Others If Any', help_text='Enter any additional information if any', initial='')
    presentIllness = forms.CharField(label='Present Illness', help_text='Enter present illness or symptoms', initial='')
    familyhistory = forms.CharField(label='Family History', help_text='Enter family history if any', initial='')
    history = forms.CharField(label='History', initial='no')  # Default value 'no'

class AllergyForm(forms.Form):
    allergies = forms.CharField(label='Allergies', help_text='Enter allergies separated by commas (e.g., None)', initial='')
    history = forms.CharField(label='History', initial='no')  # Default value 'no'

class InvestigationForm(forms.Form):
    master = forms.CharField(label='Master', help_text='Enter investigations separated by commas (e.g., Blood test, X-ray)')
    otherInvestigation = forms.CharField(label='Other Investigation', help_text='Enter any other investigations', initial='')
    history = forms.CharField(label='History', initial='no')  # Default value 'no'

class DiagnosisForm(forms.Form):
    provisionalDiagnosis = forms.CharField(label='Provisional Diagnosis', help_text='Enter provisional diagnosis separated by commas (e.g., Migraine, Gastritis)')
    othersifany = forms.CharField(label='Others If Any', help_text='Enter any additional information if any', initial='')
    history = forms.CharField(label='History', initial='no')  # Default value 'no'
