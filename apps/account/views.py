from django.conf import settings
from django.contrib import messages
from django.utils.http import is_safe_url
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.shortcuts import redirect
from django.contrib import auth
from django.urls import reverse

from .forms import RegisterForm
from ..users.models import User
from ..invite.forms import InviteForm
from .forms import LoginForm

backend_auth = getattr(settings,"BACKEND_AUTH")


@login_required
def app(request,
	template="account/account_app.html",
	**kwargs):
	invite_form = InviteForm(request)
	if request.method == 'POST':
		invite_form = InviteForm(request,data=request.POST)
		if invite_form.is_valid():
			invite_form.save()
		else:
			print("invalid email")

	ctx = {
	'invite_form':invite_form,
	}

	return TemplateResponse(request,template,ctx)


# decorator valid code access only or error
def new_user_registered(request,random,code):
	model_cls = User

	is_activated = False

	user = get_object_or_404(model_cls,invite_code__iexact=code)
	form = RegisterForm(user=user)
	if not user.is_active:
		if request.method == 'POST':
			form = RegisterForm(user=user,data=request.POST)
			if form.is_valid():
				user = form.save()
				auth.login(request,user,backend=backend_auth)
				return redirect('account:app')
			else:
				print("in-valid")
	else:
		is_activated = True
		print("already activated message")

	ctx = {
	'form':form,
	"is_activated":is_activated
	}

	return TemplateResponse(request,'account/account_reg.html',ctx)



def user_login(request):
	if request.method == "POST":
		next = request.POST.get('next', request.GET.get('next', 
        request.META.get('HTTP_REFERER', None)))
		print(next)
		login_form = LoginForm(data = request.POST)
		if login_form.is_valid():
			cd = login_form.cleaned_data
			username = cd['username']
			password = cd['password']

			try:
				user = auth.authenticate(username=username,password=password)
			except:
				pass
			if not user is None and user:
				auth.login(request,user)
				return redirect('account:app')
			else:
				print('in-valid user credentials')
		else:
			print("in-valid")
	return redirect('page:index')




def user_logout(request):
	auth.logout(request)
	return redirect('page:index')