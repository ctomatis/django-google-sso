import httplib2
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets

FLOW = flow_from_clientsecrets(**getattr(settings, 'GOOGLE_OAUTH'))


def index(request):
    redirect_path = request.GET.get('next') or getattr(settings, 'HOME_URL')
    if request.user.is_authenticated():
        return redirect(redirect_path)

    FLOW.params.update({
        'state': redirect_path, 'access_type': 'online'
    })

    return render(request, 'templates/index.html', {
        'authorize_url': FLOW.step1_get_authorize_url()
    })


def google_callback(request):
    try:
        credential = FLOW.step2_exchange(request.GET)
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build('oauth2', 'v2', http=http)
        user = service.userinfo().get().execute()
        return _authenticate_user(request, user.get('email', None))
    except:
        return redirect(getattr(settings, 'LOGIN_URL'))


def _authenticate_user(request, email=None):
    redirect_path = getattr(settings, 'LOGIN_URL')
    login_user = authenticate(email=email)
    if login_user is not None:
        login(request, login_user)
        redirect_path = request.GET.get('state')
    else:
        messages.error(request, email)
    return redirect(redirect_path)
