# from django.urls import path
# from . import views

# app_name = 'MedicalDocumentExtraction'

# urlpatterns = [
#     path('', views.home, name='home'),  # Home URL
#     path('upload/', views.upload_image, name='upload_image'),  # Upload URL
# ]


from django.urls import path
from .views import PrescriptionUploadView, home_view

app_name = 'MedicalDocumentExtraction'

urlpatterns = [
    path('upload/', PrescriptionUploadView.as_view(), name='api_upload'),
    path('', home_view, name='home'),
]
