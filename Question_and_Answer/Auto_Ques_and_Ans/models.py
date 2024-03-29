from django.db import models



class QuestionInput(models.Model):
    text = models.TextField(max_length=10000)  # Optional: Store input text

    
