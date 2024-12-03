from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Prescription
from .serializers import PrescriptionSerializer
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from PIL import Image
import tempfile
import os
import PyPDF2
import re
import logging
import easyocr

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

patterns = {
    'patient_name': r'Patient\s*Name\s*:\s*(.*?)(?:\n|Age|Gender|,|/)',
    'date_of_birth': r'Date\s*of\s*Birth\s*:\s*([^\n]+)',
    'gender_age': r'Age\s*/\s*Gender\s*:\s*(\d+ Y:\d+ M:\d+ D)\s*/\s*(\w+)',
    'mobile_number': r'mobile\s*number\s*=?\s*([\d-]+)',
    'mrn': r'MRN\s*:\s*(\w+)',
    'weight': r'Weight\s*\(kg\)\s*:\s*([\d.]+)',
    'height': r'Height\s*\(cms\)\s*:\s*([\d.]+)',
    'bmi': r'BMI\s*:\s*([\d.]+)',
    'temperature': r'Temperature\s*:\s*([\d.]+)',
    'systolic_bp': r'Systolic\s*\(mmhg\)\s*:\s*([\d.]+)',
    'diastolic_bp': r'Diastolic\s*:\s*([\d.]+)',
    'map': r'MAP\s*:\s*([\d.]+)',
    'fvc': r'FVC\s*:\s*([\d.]+)',
    'fev1': r'FEV1\s*:\s*([\d.]+)',
    'pef': r'PEF\s*:\s*([\d.]+)',
    'ratio': r'Ratio\s*:\s*([\d.]+)',
    'cholesterol_total': r'TotalCholesterol\s*:\s*(\d+)',
    'triglycerides': r'Triglycerides\s*:\s*(\d+)',
    'hdl': r'HDL\s*:\s*(\d+)',
    'ldl': r'LDL\s*:\s*(\d+)',
    'blood_sugar_fasting': r'Fasting\s*:\s*([\d.]+)',
    'blood_sugar_post_prandial': r'Post-Prandial\s*:\s*([\d.]+)',
    'blood_sugar_random': r'Random\s*:\s*([\d.]+)',
    'respiration_rate': r'Respiration\s*rate\s*:\s*([\d.]+)',
    'pulse_rate': r'Pulse\s*/\s*Heart\s*Rate\s*:\s*([\d.]+)',
    'spo2': r'SpO2\s*:\s*([\d.]+)',
    'chief_complaints': r'Chief\s*Complaints\s*/\s*History\s*of\s*Present\s*illness\s*:\s*(.*?)(?:Drugs|Investigations)',
    'prescription': r'Drugs\s*(.*?)(?:Investigations|Procedures)',
    'investigations': r'Investigations\s*:\s*(.*?)(?:Procedures|General Instructions)',
    'procedures': r'Procedures\s*:\s*(.*?)(?:General\s*Instructions|Printed)',
    'general_instructions': r'General\s*Instructions\s*:\s*(.*?)\s*Printed',
    'next_appointment': r'Please\s*follow\s*up\s*with\s*the\s*nearest\s*referred\s*by\s*(.*?)\s*for',
    'doctor': r'Doctor\s*:\s*(.*?)\s*(?:Prescription|Date of Birth|Gender)',
    'order_date': r'Order\s*Date\s*:\s*(.*?)\s*PM',
    'report_name': r'Report\s*Name\s*:\s*(.*?)\s*MRN',
    'department_name': r'Department\s*Name\s*:\s*(.*?)\s*RDAD',
    'final_observation': r'Final\s*observation\s*:\s*(.*?)\s*Result',
    'result': r'Result\s*:\s*(.*?)\s*Doctor',
    'doctor_name': r'Doctor\s*Name\s*:\s*(.*?)\s*\*\*\* END OF REPORT \*\*\*',
    'specimen': r'Specimen\s*:\s*(.*?)\s*Result',
    'investigation_result': r'Investigation\s*Result\s*Units\s*Reference\s*Range\s*(.*?)\s*Remarks',
    'antibiotic_result': r'Antibiotic\s*Result\s*:\s*(.*?)\s*Microorganism',
    'microorganism_result': r'Microorganism\s*Result\s*:\s*(.*?)\s*\*\*\* END OF REPORT \*\*\*',
    'report_date': r'Report\s*Date\s*:\s*([^\n]+)',
}

additional_patterns = {
    'abha_number': r'ABHA\s*Number\s*:\s*(\S+)',
    'age': r'Age\s*:\s*(\d+)',
    'gender': r'Gender\s*:\s*(\w+)',
    'date_time': r'Date\s*&\s*Time\s*:\s*([0-9-:\s]+)',
    'diagnosis': r'Provisional\s*Diagnosis\s*:\s*(.*?)\n(?:Advice|Diet)',
    'advice': r'Advice\s*:\s*(.*?)\n(?:Diet|Comments)',
    'comments': r'Comments\s*:\s*(.*?)\n(?:Pharmacy\s*Details|Instructions)',
    'drug_name': r'\d+\s*TABLET\s*([\w\s]+)\s*\d+mg',
    'units_dosage': r'Units\s*\(Dosage\)\s*:\s*(\d+\s*mg)',
    'pharmacy_details': r'Pharmacy\s*Details\s*:\s*(.*?)\n(?:Instructions|Comments)',
    'follow_up_advice': r'Follow\s*up\s*advice\s*:\s*(.*?)\s*$',
    'blood_group': r'Blood\s*Group\s*:\s*(\w+)',
    'allergies': r'Allergies\s*:\s*(.*?)\n',
    'insurance_policy_number': r'Insurance\s*Policy\s*Number\s*:\s*(\w+)',
    'emergency_contact': r'Emergency\s*Contact\s*:\s*(.*?)\s*Relation',
    'relation_to_patient': r'Relation\s*to\s*Patient\s*:\s*(\w+)',
    'contact_address': r'Contact\s*Address\s*:\s*(.*?)\s*Phone',
    'phone_number': r'Phone\s*Number\s*:\s*(\d+)',
    'hospital_name': r'Hospital\s*Name\s*:\s*(.*?)\n',
    'hospital_address': r'Hospital\s*Address\s*:\s*(.*?)\n',
    'insurance_provider': r'Insurance\s*Provider\s*:\s*(.*?)\n',
    'symptoms': r'Symptoms\s*:\s*(.*?)\s*(?:Medication|Treatment)',
    'medication': r'Medication\s*:\s*(.*?)\s*(?:Dosage|Instructions)',
    'dosage': r'Dosage\s*:\s*(.*?)\s*(?:Frequency|Instructions)',
    'frequency': r'Frequency\s*:\s*(.*?)\s*(?:Instructions|Duration)',
    'duration': r'Duration\s*:\s*(.*?)\s*(?:Remarks|Comments)',
    'remarks': r'Remarks\s*:\s*(.*?)\s*(?:Next\s*Appointment|Follow-Up)',
    'follow_up_date': r'Follow-Up\s*Date\s*:\s*(.*?)\s*(?:Doctor|Location)',
    'location': r'Location\s*:\s*(.*?)\s*(?:Doctor|Contact)',
    'email': r'Email\s*:\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4})',
}

patterns.update(additional_patterns)

def extract_text_from_image(image_file):
    image = Image.open(image_file)
    temp_image_path = os.path.join(tempfile.gettempdir(), next(tempfile._get_candidate_names()) + '.png')
    image.save(temp_image_path)
    
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(temp_image_path, detail=0)
    
    return ' '.join(result)

def extract_text_from_pdf(pdf_file):
  """
  Extracts text from a PDF file using PyPDF2.

  Args:
      pdf_file: A file object containing the PDF data.

  Returns:
      A string containing the extracted text from all pages of the PDF.
  """

  pdf_reader = PyPDF2.PdfReader(pdf_file)
  full_text = ""

  # Iterate through all pages and extract text
  for page_num in range(len(pdf_reader.pages)):
    page = pdf_reader.pages[page_num]
    full_text += page.extract_text()

  return full_text

def extract_information_from_text(text):
    extracted_data = {}

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            extracted_data[key] = match.group(1).strip()

    return extracted_data

def process_image(image_file):
    extracted_text = extract_text_from_image(image_file)
    return extract_information_from_text(extracted_text)

def process_pdf(pdf_file):
    extracted_text = extract_text_from_pdf(pdf_file)
    return extract_information_from_text(extracted_text)

class PrescriptionUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        try:
            image_file = request.FILES['image']
            if image_file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                extracted_data = process_image(image_file)
            elif image_file.name.lower().endswith('.pdf'):
                extracted_data = process_pdf(image_file)
            else:
                return Response({"error": "Unsupported file format. Please upload a PNG, JPG, JPEG image, or PDF file."}, status=status.HTTP_400_BAD_REQUEST)

            prescription = Prescription.objects.create(image=image_file, text=str(extracted_data))
            serializer = PrescriptionSerializer(prescription)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def home_view(request):
    return render(request, 'MedicalDocumentExtraction/upload.html')
