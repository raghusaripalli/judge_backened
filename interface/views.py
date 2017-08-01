from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template.context_processors import csrf

from interface.forms import MyRegistrationForm


@login_required(login_url="login/")
def home(request):
    request.COOKIES['username'] = request.user
    response = render(request, "home.html")
    response.set_cookie('username', request.user)
    return response

def register_user(request):
    args = {}
    if request.method == 'POST':
        # print request.POST
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login')
        else:
            # print form.error_messages
            # print form.non_field_errors
            args['errors'] =  form.errors
    else:
        form = MyRegistrationForm()
    args['form'] = form
    args.update(csrf(request))
    return render(request, 'register.html',args)
