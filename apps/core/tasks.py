from datetime import timedelta

from config.celery import app

from django.conf import settings
from django.template.loader import render_to_string 
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.core.mail import BadHeaderError

from ..users.models import User as model_cls
from ..account.mail import send_mail



@app.task
# celery perform computational tasks
def test_celery_func():
	for i in range(80):
		print(i)
	return " Celery YEEH -:) "



@app.task
def send_invite_email(invite):
	domain = settings.SITE_DOMAIN

	link_url = settings.SITE_DOMAIN

	subject = "Invite to Join Site"

	ctx = {
	"domain":domain,
	"message":invite.invite_message,
	"code":invite.invite_token,
	"link_url" : link_url
	}

	message = get_template(
		template_name = "account/email_template.html"
	).render(ctx)

	to_email = invite.invite_to_email

	from_email =  settings.DEFAULT_FROM_EMAIL

	email = EmailMessage(
		subject,message,from_email,[to_email])
	email.content_subtype = "html"

	try:
		email.send()
	except BadHeaderError:
		pass


@app.task
def remind_users_to_activate_code():
	users = model_cls._default_manager.filter(is_active=False)
	emails = [user.email for user in users]
	# send reminded to thse whose invite as been 2 days

	send_mail(
		"Account needs activation",
		"Please activate your account",
		settings.DEFAULT_FROM_EMAIL,
		emails,
	)

