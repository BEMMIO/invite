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
from django.utils.crypto import get_random_string
from django.shortcuts import redirect
from django.contrib import auth
from django.urls import reverse

from apps.invite.models import Invitation

def validate_code(request):
	code = request.POST.get('code').strip()
	bool_ = Invitation.is_invite_code_valid(str(code))
	if bool_:
		g_random_link = get_random_string(length=32) #add a one-time generated code to user unique code
		return redirect(reverse('account:new-user',kwargs={'random':g_random_link,'code':code}))
	else:
		print('in-valid code')
		return redirect('page:index')
