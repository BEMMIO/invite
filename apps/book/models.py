from django.db import models as m
from apps.users.models import User as model_cls
from ..core.utils.uploads import upload_cover_dir,upload_pdf_dir
# Create your models here.

class Author(m.Model):

	user 		=		m.ForeignKey(to=model_cls,blank=False,null=False,on_delete=m.CASCADE)

	created_at  =       m.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = (("-pk"),)

	def __str__(self):
		return self.user.username




class Book(m.Model):

	# book info
	title 		=		m.CharField(max_length=255,blank=False,null=False,unique=True)

	description =		m.TextField(max_length=500,blank=False,null=False)

	# images/files
	cover 		=		m.ImageField(upload_to=upload_cover_dir,blank=True,null=True)

	pdf 		=		m.FileField(upload_to=upload_pdf_dir,blank=True,null=True)


	author 		=   	m.ForeignKey(to=Author,blank=False,null=False,on_delete=m.CASCADE,related_name="books")

	# dates
	published_at= 		m.DateTimeField(blank=True,null=True)

	created_at  =		m.DateTimeField(auto_now_add=True)

	updated		=		m.DateTimeField(auto_now=True)


	class Meta:
		ordering = ["-pk"]
		verbose_name="Site Book"
		verbose_name_plural = "Site Book's"


	def __str__(self):
		return self.title