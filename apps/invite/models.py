import uuid
from enum import Enum

from django.db import models

from ..users.models import User



__all__ = ['Invitation']


def get_default_uuid():
    return str(uuid.uuid4().hex)


class InvitationChoices:
	ACCEPTED = 'accepted'
	REJECTED = 'rejected' 
	SENT  	 = 'sent'

	CHOICES = [
		(ACCEPTED,'Accepted'),
		(REJECTED,'Rejected'),
		(SENT,'Sent'),
	]


# set expiry to 21 days

class Invitation(models.Model):

	uuid 				=		models.CharField(max_length=32,editable=False,null=False,
								blank=False,unique=True,default=get_default_uuid)

	invite_from_user 	=		models.ForeignKey(to=User,blank=True,null=True,
								verbose_name=("invitation from user"),related_name="invites_from_user",
								on_delete=models.CASCADE)

	invite_to_email		=		models.EmailField(max_length=255,verbose_name="Email",unique=True,blank=False,null=False)


	invite_to_user 		=		models.OneToOneField(to=User,blank=True,null=True,
								on_delete=models.CASCADE,related_name="invite")


	invite_token 		=		models.CharField(max_length=15,blank=True,null=True,
								verbose_name=("Code"))	

	invite_message 		=		models.TextField(max_length=225,blank=True,null=True,
								verbose_name=("Message"))

	invite_status 		= 		models.CharField(max_length=10,blank=True,null=True,
								choices=InvitationChoices.CHOICES,verbose_name="Invite Status")


	created_date		=		models.DateTimeField(auto_now_add=True)

	modified_date		=		models.DateTimeField(auto_now=True)


	class Meta:
		verbose_name    = "User invitation"
		verbose_name_plural = "User invitation"
		unique_together = (("invite_from_user", "invite_to_email","invite_token"),)


	def __str__(self):
		return "{0} sent an invite to {1}".format(self.invite_from_user.username,self.invite_to_email)


	def save(self,*args,**kwargs):
		self.invite_to_email = self.invite_to_email.lower()
		super(Invitation,self).save(*args,**kwargs)


	@classmethod
	def is_invite_code_valid(cls,code:str):
		qs = cls._default_manager.filter(invite_status=InvitationChoices.SENT)
		qs = qs.filter(invite_token__iexact=code)
		return qs.exists()


