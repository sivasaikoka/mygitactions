from django.urls import path
from .views import getVoice, list_voice_inputs, home,save_edited_voice
app_name='SpeechRecognition'
urlpatterns = [
    path('', home, name='home'),
    path('voice/', getVoice, name='get_voice'),
    path('list_voice_inputs/', list_voice_inputs, name='list_voice_inputs'),
    path('save-edited-voice/', save_edited_voice, name='save_edited_voice'),
]
