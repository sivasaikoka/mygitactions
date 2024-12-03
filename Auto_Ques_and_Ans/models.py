from django.db import models



class QuestionInput(models.Model):
    text = models.TextField(max_length=100000)  # Optional: Store input text

    
