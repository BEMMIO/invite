from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.urls import reverse

from ..account.forms import SignUpWithCode,LoginForm
from ..core.tasks import test_celery_func

def index(request):
	if request.user.is_authenticated:
		return redirect('account:app')
	# account code validation form
	# login form/login-redirect here
	test_celery_func.delay()
	login_form = LoginForm()
	invite_code_form = SignUpWithCode()
	ctx = {
	'invite_code_form':invite_code_form,
	'login_form':login_form,
	}
	return TemplateResponse(request,'index.html',ctx)