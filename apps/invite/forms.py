from django.utils.safestring import mark_safe
from django import forms

from .signals import invite_is_created
from ..core.tasks import send_invite_email
from .models import Invitation as model_cls,InvitationChoices



class InviteForm(forms.ModelForm):

	invite_to_email = forms.EmailField(label="E-mail",required=True,widget=forms.EmailInput(attrs={
		'placeholder':'eg. kofi_anderson@mail.com','autofocus':True
		}))

	invite_message = forms.CharField(label="Message",required=True,widget=forms.Textarea(attrs={
		'placeholder':'Message to send to this e-mail address'
		}))

	class Meta:
		model = model_cls
		fields = ['invite_to_email','invite_message']


	def __init__(self,request,*args,**kwargs):
		self.request = request
		self.user = self.request.user
		super(self.__class__,self).__init__(*args,**kwargs)
		# default message body - short and easy to read invite message
		# use user set full-name of user sending the invite
		# limit invite_message body to 60 characters (UX count down on typing)
		# ajax to validate email: an invite was sent to this email X days ago,
		# -user already exists with given email,this email has been banned from this site etc
		# UI/UX show as an aside : slide in and out & also access it on user profile page
		# clean_invite_message : as user may clear the message body, and assign the default again
		default_message = mark_safe("{user} is inviting you to join ukvite.herokuapp.com".format(user=self.user.username))
		self.fields['invite_message'].initial = default_message


	def clean_invite_to_email(self):
		email = self.cleaned_data.get('invite_to_email')
		qs = model_cls._default_manager.filter(invite_to_email__iexact=email)
		if qs.exists():
			if qs[0].invite_status == InvitationChoices.ACCEPTED:
				raise forms.ValidationError("User with this e-mail already exists")
			elif qs[0].invite_status == InvitationChoices.SENT:
				if not qs[0].invite_from_user == self.user:
					raise forms.ValidationError("A user with this e-mail has already been invited")
				else:
					raise forms.ValidationError("You have already invited someone with this email")

		if self.user.email == email:
			raise forms.ValidationError("sorry,you cannot send an invite to yourself")
		return self.cleaned_data.get('invite_to_email')



	'''
	clean e-mail:
	- validate email (real-email address)
	-	in not-allowed e-mails?
	- user is not sending invite mail to themselves
	- e-mail exists
			-	activated (accepted )? then in use
			-	requires activation?
			- 	banned e-mails?

	'''

	def save(self,force_insert=False,force_update=False,commit=True,**kwargs):
		invite_obj = super().save(commit=False)

		invite_obj.invite_from_user = self.user
		invite_obj.invite_status = InvitationChoices.SENT
		if commit:
			invite_obj.save()
			# signal invite created
			invite_is_created.send(sender=self.__class__,
									invite=invite_obj)
			# celery to send email
			send_invite_email(invite_obj)
		return invite_obj
