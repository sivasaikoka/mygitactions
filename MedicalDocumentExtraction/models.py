# # prescription/models.py

# from django.db import models

# class Prescription(models.Model):
#     # Define the fields of the Prescription model here
#     image = models.ImageField(upload_to='prescriptions/')
#     text = models.TextField(blank=True)

#     def __str__(self):
#         return f"Prescription {self.id}"


from django.db import models

class Prescription(models.Model):
    image = models.ImageField(upload_to='prescriptions/')
    text = models.TextField(blank=True)

    def __str__(self):
        return f"Prescription {self.id}"
