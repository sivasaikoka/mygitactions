from django.db import models

class VoiceInput(models.Model):
    language = models.CharField(max_length=20, default='en-IN')
    input_text = models.TextField()
    output_data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.language} - {self.timestamp}"
