import uuid
import re
import os

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    Permission,
    PermissionsMixin,
)
from django.core import validators
from django.utils import timezone
from django.apps import apps
from django.db import models


class UserManager(BaseUserManager):
	def create_user(self,username,email,password=None,is_active=True,is_staff=False,**kwargs):
		"""create a user instance given email and password"""
		email = UserManager.normalize_email(email)

		user = self.model(
			username=username,email=email,is_active=is_active,is_staff=is_staff,**kwargs
		)

		if not username:
			raise ValueError("User must have an username.")

		if not email:
			raise ValueError("User must have an email address.")

		if password:
			user.set_password(password)
		user.save()
		return user

	def create_superuser(self, username,email, password=None, **kwargs):
		return self.create_user(username,email,password,is_staff=True,is_superuser=True,**kwargs)


def get_default_uuid():
    return str(uuid.uuid4().hex)


def avatar_upload_dir(user_obj,file_obj):
	file_ext = file_obj.split('.')[-1].lower
	_file = '{0}.{1}'.format(user_obj.uuid,file_ext)
	return os.path.join('avatars',_file)



class User(PermissionsMixin,AbstractBaseUser):
	uuid 				=		models.CharField(max_length=32,editable=False,null=False,
								blank=False,unique=True,default=get_default_uuid)

	username 			=		models.CharField(max_length=255,unique=True,
								help_text=("Required. 30 characters or fewer. letters, numbers, and "
								"/./-/_ characters."),
								validators=[validators.RegexValidator(re.compile(r"^[\w.-]+$"),("Enter a valid username."), "invalid")])

	email 				=		models.EmailField(verbose_name = ("e-mail address"), max_length=255, null=False, blank=False, unique=True)

	is_active   		=  		models.BooleanField(verbose_name = ("active"),default=True,help_text = ("Designates whether this user should be treated as "
								"active. Unselect this instead of deleting accounts."))

	is_staff    		=       models.BooleanField(verbose_name = ('staff status'), default=False,
								help_text="Designates whether the user can log into this admin site.")

	full_name 			=		models.CharField(verbose_name = ("full name"), max_length=256, blank=True)

	date_joined 		= 		models.DateTimeField(verbose_name = ("date joined"),blank=True,null=True,
								help_text="Designates the date user accepted invitation token")

	invite_code 		=		models.CharField(verbose_name = ("Invite Code"), max_length=16, blank=True,null=True)

	joined_from_ip 		=		models.GenericIPAddressField(null=True, blank=True)

	default_avatar 		= 		models.ImageField(verbose_name = ("user default avatar"),max_length=255,blank=True,null=True)

	avatar_src 		 	= 		models.ImageField(upload_to=avatar_upload_dir,verbose_name = ("user uploaded avatar "),max_length=255,blank=True,null=True)

	created_date		=		models.DateTimeField(auto_now_add=True,blank=True,null=True)

	modified_date 		=		models.DateTimeField(auto_now=True,blank=True,null=True)


	USERNAME_FIELD 		= 		"username"
	REQUIRED_FIELDS 	= 		["email"]


	objects 			=	UserManager()


	def _clean(self):
		self.username = self.normalize_username(self.username)
		self.email 	  = UserManager.normalize_email(self.email)

	def clean(self):
		self._clean

	