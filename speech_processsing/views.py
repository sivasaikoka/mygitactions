from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from .models import VoiceInput
from .serializers import VoiceInputSerializer
from django.shortcuts import render
import speech_recognition as sr
from gtts import gTTS
import os
import re
import pandas as pd
import logging

logger=logging.getLogger(__name__)

# Function to convert text to speech
#def say(text, lang='en'):
    #tts = gTTS(text=text, lang=lang)
    #tts.save('static/output.mp3')
    #os.system("mpg321 static/output.mp3")
    #os.remove('static/output.mp3')

def takecommand(language='en-IN'):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 2
        r.energy_threshold = 5000
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-IN")
            print(f"User said: {query}")
            return query
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return "Google Speech Recognition service error"
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
            return "Could not understand audio"
        except Exception as e:
            print(f"Recognition error: {e}")
            return "Some error occurred"


patterns = {
    
    'patient name': r"(?:patient\s*name|pt\.\s*name|Pt\.\s*Name)\s*(.*?)(?=\s*(?:age|gender|temperature|systolic|diastolic|pulse|spo2|sugar|height|weight|past\s*history\s*and\s*allergies|chief\s*complaints|provisional\s*diagnosis|advice|comments|drug\s*type|drug\s*name|units|drug\s*instruction|period|investigations\s*service\s*name|follow\s*up\s*date|referral\s*hospital|$))",
    'age': r"age\s*(.*?)(?=\s*(?:patient\s*name|gender|temperature|systolic|diastolic|pulse|spo2|sugar|height|weight|past\s*history\s*and\s*allergies|chief\s*complaints|provisional\s*diagnosis|advice|comments|drug\s*type|drug\s*name|units|drug\s*instruction|period|investigations\s*service\s*name|follow\s*up\s*date|referral\s*hospital|$))",
    'gender': r"(?:gender|gdr:)\s*(.*?)(?=\s*(?:patient\s*name|age|temperature|systolic|diastolic|pulse|spo2|sugar|height|weight|past\s*history\s*and\s*allergies|chief\s*complaints|provisional\s*diagnosis|advice|comments|drug\s*type|drug\s*name|units|drug\s*instruction|period|investigations\s*service\s*name|follow\s*up\s*date|referral\s*hospital|$))",
    'temperature': r"temperature\s*(.*?)(?=\s*(?:patient\s*name|age|gender|systolic|diastolic|pulse|spo2|sugar|height|weight|past\s*history\s*and\s*allergies|chief\s*complaints|provisional\s*diagnosis|advice|comments|drug\s*type|drug\s*name|units|drug\s*instruction|period|investigations\s*service\s*name|follow\s*up\s*date|referral\s*hospital|$))",
    'systolic': r"systolic\s*(.*?)(?=\s*(?:patient\s*name|age|gender|temperature|diastolic|pulse|spo2|sugar|height|weight|past\s*history\s*and\s*allergies|chief\s*complaints|provisional\s*diagnosis|advice|comments|drug\s*type|drug\s*name|units|drug\s*instruction|period|investigations\s*service\s*name|follow\s*up\s*date|referral\s*hospital|$))",
    'diastolic': r"(?:diastolic)\s*(.*?)(?=\s*(?:patient\s*name|age|gender|temperature|systolic|pulse|spo2|sugar|height|weight|past\s*history\s*and\s*allergies|chief\s*complaints|provisional\s*diagnosis|advice|comments|drug\s*type|drug\s*name|units|drug\s*instruction|period|investigations\s*service\s*name|follow\s*up\s*date|referral\s*hospital|$))",
    'pulse': r"(?:pulse|HR)\s*(.*?)(?=\s*(?:patient\s*name|age|gender|temperature|systolic|diastolic|spo2|sugar|height|weight|past\s*history\s*and\s*allergies|chief\s*complaints|provisional\s*diagnosis|advice|comments|drug\s*type|drug\s*name|units|drug\s*instruction|period|investigations\s*service\s*name|follow\s*up\s*date|referral\s*hospital|$))",
    'spo2': r"(?:spo2|O2\s*Sat)\s*(.*?)(?=\s*(?:patient\s*name|age|gender|temperature|systolic|diastolic|pulse|sugar|height|weight|past\s*history\s*and\s*allergies|chief\s*complaints|provisional\s*diagnosis|advice|comments|drug\s*type|drug\s*name|units|drug\s*instruction|period|investigations\s*service\s*name|follow\s*up\s*date|referral\s*hospital|$))",
    'sugar': r"(?:sugar|BSL)\s*(.*?)(?=\s*(?:patient\s*name|age|gender|temperature|systolic|diastolic|pulse|spo2|height|weight|past\s*history\s*and\s*allergies|chief\s*complaints|provisional\s*diagnosis|advice|comments|drug\s*type|drug\s*name|units|drug\s*instruction|period|investigations\s*service\s*name|follow\s*up\s*date|referral\s*hospital|$))",
    'height': r"(?:height|ht\.)\s*(.*?)(?=\s*(?:patient\s*name|age|gender|temperature|systolic|diastolic|pulse|spo2|sugar|weight|past\s*history\s*and\s*allergies|chief\s*complaints|provisional\s*diagnosis|advice|comments|drug\s*type|drug\s*name|units|drug\s*instruction|period|investigations\s*service\s*name|follow\s*up\s*date|referral\s*hospital|$))",
    'weight': r"(?:weight|wt\.)\s*(.*?)(?=\s*(?:patient\s*name|age|gender|temperature|systolic|diastolic|pulse|spo2|sugar|height|past\s*history\s*and\s*allergies|chief\s*complaints|provisional\s*diagnosis|advice|comments|drug\s*type|drug\s*name|units|drug\s*instruction|period|investigations\s*service\s*name|follow\s*up\s*date|referral\s*hospital|$))",
    'past history and allergies': r"(?:past\s*history\s*and\s*allergies|hx\s*&\s*allergies)\s*(.*?)(?=\s*(?:patient\s*name|age|gender|temperature|systolic|diastolic|pulse|spo2|sugar|height|weight|chief\s*complaints|provisional\s*diagnosis|advice|comments|drug\s*type|drug\s*name|units|drug\s*instruction|period|investigations\s*service\s*name|follow\s*up\s*date|referral\s*hospital|$))",
    'chief complaints': r"(?:chief\s*complaints|chief\s*c/o)\s*(.*?)(?=\s*(?:patient\s*name|age|gender|temperature|systolic|diastolic|pulse|spo2|sugar|height|weight|past\s*history\s*and\s*allergies|provisional\s*diagnosis|advice|comments|drug\s*type|drug\s*name|units|drug\s*instruction|period|investigations\s*service\s*name|follow\s*up\s*date|referral\s*hospital|$))",
    'provisional diagnosis': r"(?:provisional\s*diagnosis|provisional\s*DX)\s*(.*?)(?=\s*(?:patient\s*name|age|gender|temperature|systolic|diastolic|pulse|spo2|sugar|height|weight|past\s*history\s*and\s*allergies|chief\s*complaints|advice|comments|drug\s*type|drug\s*name|units|drug\s*instruction|period|investigations\s*service\s*name|follow\s*up\s*date|referral\s*hospital|$))",
    'advice': r"(?:advice|advce)\s*(.*?)(?=\s*(?:patient\s*name|age|gender|temperature|systolic|diastolic|pulse|spo2|sugar|height|weight|past\s*history\s*and\s*allergies|chief\s*complaints|provisional\s*diagnosis|comments|drug\s*type|drug\s*name|units|drug\s*instruction|period|investigations\s*service\s*name|follow\s*up\s*date|referral\s*hospital|$))",
    'comments': r"(?:comments|coment)\s*(.*?)(?=\s*(?:patient\s*name|age|gender|temperature|systolic|diastolic|pulse|spo2|sugar|height|weight|past\s*history\s*and\s*allergies|chief\s*complaints|provisional\s*diagnosis|advice|drug\s*type|drug\s*name|units|drug\s*instruction|period|investigations\s*service\s*name|follow\s*up\s*date|referral\s*hospital|$))",
    'drug type': r"(?:drug\s*type|meds)\s*(.*?)(?=\s*(?:patient\s*name|age|gender|temperature|systolic|diastolic|pulse|spo2|sugar|height|weight|past\s*history\s*and\s*allergies|chief\s*complaints|provisional\s*diagnosis|advice|comments|drug\s*name|units|drug\s*instruction|period|investigations\s*service\s*name|follow\s*up\s*date|referral\s*hospital|$))",
    'drug name': r"(?:drug\s*name|med\s*name)\s*(.*?)(?=\s*(?:patient\s*name|age|gender|temperature|systolic|diastolic|pulse|spo2|sugar|height|weight|past\s*history\s*and\s*allergies|chief\s*complaints|provisional\s*diagnosis|advice|comments|drug\s*type|units|drug\s*instruction|period|investigations\s*service\s*name|follow\s*up\s*date|referral\s*hospital|$))",
    'units': r"(?:units|freq)\s*(.*?)(?=\s*(?:patient\s*name|age|gender|temperature|systolic|diastolic|pulse|spo2|sugar|height|weight|past\s*history\s*and\s*allergies|chief\s*complaints|provisional\s*diagnosis|advice|comments|drug\s*type|drug\s*name|drug\s*instruction|period|investigations\s*service\s*name|follow\s*up\s*date|referral\s*hospital|$))",
    'drug instruction': r"(?:drug\s*instruction|med\s*instructions)\s*(.*?)(?=\s*(?:patient\s*name|age|gender|temperature|systolic|diastolic|pulse|spo2|sugar|height|weight|past\s*history\s*and\s*allergies|chief\s*complaints|provisional\s*diagnosis|advice|comments|drug\s*type|drug\s*name|units|period|investigations\s*service\s*name|follow\s*up\s*date|referral\s*hospital|$))",
    'period': r"(?:period|duration)\s*(.*?)(?=\s*(?:patient\s*name|age|gender|temperature|systolic|diastolic|pulse|spo2|sugar|height|weight|past\s*history\s*and\s*allergies|chief\s*complaints|provisional\s*diagnosis|advice|comments|drug\s*type|drug\s*name|units|drug\s*instruction|investigations\s*service\s*name|follow\s*up\s*date|referral\s*hospital|$))",
    'investigations service name': r"(?:investigations\s*service\s*name|tests)\s*(.*?)(?=\s*(?:patient\s*name|age|gender|temperature|systolic|diastolic|pulse|spo2|sugar|height|weight|past\s*history\s*and\s*allergies|chief\s*complaints|provisional\s*diagnosis|advice|comments|drug\s*type|drug\s*name|units|drug\s*instruction|period|follow\s*up\s*date|referral\s*hospital|$))",
    'follow up date': r"(?:follow\s*up\s*date|follow\s*update)\s*(.*?)(?=\s*(?:patient\s*name|age|gender|temperature|systolic|diastolic|pulse|spo2|sugar|height|weight|past\s*history\s*and\s*allergies|chief\s*complaints|provisional\s*diagnosis|advice|comments|drug\s*type|drug\s*name|units|drug\s*instruction|period|investigations\s*service\s*name|referral\s*hospital|$))",
    'referral hospital': r"(?:referral\s*hospital|referral\s*hosp)\s*(.*?)(?=\s*(?:patient\s*name|age|gender|temperature|systolic|diastolic|pulse|spo2|sugar|height|weight|past\s*history\s*and\s*allergies|chief\s*complaints|provisional\s*diagnosis|advice|comments|drug\s*type|drug\s*name|units|drug\s*instruction|period|investigations\s*service\s*name|follow\s*up\s*date|$))"
}



# Function to extract data based on defined patterns
def extract_data(text, patterns):
    data = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            if key == 'temperature' and '°f' not in value.lower():
                value += ' °F'
            elif key == 'systolic' and 'mm hg' not in value.lower():
                value += ' mm Hg'
            elif key == 'diastolic' and 'mm hg' not in value.lower():
                value += ' mm Hg'
            elif key == 'pulse' and 'bpm' not in value.lower():
                value += ' bpm'
            elif key == 'spo2' and '%' not in value.lower():
                value += ' %'
            elif key == 'sugar' and 'mg/dl' not in value.lower():
                value += ' mg/dl'
            elif key == 'height' and 'cm' not in value.lower():
                value += ' cm'
            elif key == 'weight' and 'kg' not in value.lower():
                value += ' kg'
            data[key] = value
        else:
            data[key] = ""
    return data

def home(request):
    voice_inputs = VoiceInput.objects.all().order_by('-id')
    return render(request, 'SpeechRecognition/index.html', {'voice_inputs': voice_inputs})



@api_view(['POST'])
def getVoice(request):
    try:
        language = request.data.get('language', 'en-IN')
        # command = takecommand(language)
        text=request.data.get('speech_result')
        extracted_data = extract_data(text, patterns)
        # Save voice input to database
        voice_input = VoiceInput.objects.create(language=language, input_text=text, output_data=extracted_data)
        
        # Serialize the data to send back as response
        serializer = VoiceInputSerializer(voice_input)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except sr.RequestError as e:
        return Response({'error': f"Could not request results from Google Speech Recognition service; {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except sr.UnknownValueError:
        return Response({'error': "Google Speech Recognition could not understand the audio"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def list_voice_inputs(request):
    voice_inputs = VoiceInput.objects.all()
    serializer = VoiceInputSerializer(voice_inputs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
def save_edited_voice(request):
    try:
        # Assuming 'language', 'speech_result', and 'editedData' are passed in request.data
        language = request.data.get('language', 'en-IN')
        text = request.data.get('input_text')
        edited_data = request.data.get('output_data', {})  # Get edited data from frontend

        if not isinstance(edited_data, dict):
            raise ValueError("editedData must be a dictionary")

        # Save edited voice input to database
        voice_input = VoiceInput.objects.create(
            language=language,
            input_text=text,
            output_data=edited_data  # Save the edited data directly
        )

        # Serialize the data to send back as response
        serializer = VoiceInputSerializer(voice_input)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(f"Error saving edited voice input: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
