from django.db import models

class data(models.Model):

	main_status = models.CharField(max_length=30, blank=True)
	extracted_info = models.CharField(max_length=255,blank=True)
	place = models.CharField(max_length=30, blank=True)
	seen= models.IntegerField(blank=True)
	time= models.DateTimeField(auto_now_add=True, blank=True)
	
