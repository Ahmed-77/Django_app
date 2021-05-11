from django.db import models
from datetime import datetime
import os




class Patient(models.Model):
	id = models.CharField(primary_key=True, max_length=10)
	Aadhar_num = models.CharField(max_length=16)
	name = models.CharField(max_length=50)
	contact_number = models.CharField(max_length=50)
	date_of_birth = models.CharField(max_length=50)
	gender = models.CharField(max_length=8)
	email = models.CharField(max_length=50)

	def __str__(self):
		return self.name

	def num_photos(self):
		try:
			DIR = f"app/facerec/dataset/{self.name}_{self.id}"
			img_count = len(os.listdir(DIR))
			return img_count
		except:
			return 0
