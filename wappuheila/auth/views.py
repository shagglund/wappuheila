# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from wappuheila.common.utils import render_to_request_context_response
from django.contrib import messages
from django.views.generic.simple import redirect_to
from django.contrib.auth import authenticate, login
from wappuheila.auth import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import forms as auth_forms
from wappuheila.auth.forms import ChangeUserDetailsForm
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

@login_required
def username_change(request):
    return redirect_to(request, reverse('user_control_panel'), False)

@login_required
def user_control_panel(request):
    if request.method == 'POST':
        #handle the possible username change
        userdetails_form = ChangeUserDetailsForm(request.POST,instance = request.user)
        if userdetails_form.is_valid():
            if userdetails_form.cleaned_data['username']:
                request.user.username = userdetails_form.cleaned_data['username']
            if userdetails_form.cleaned_data['first_name']:
                request.user.first_name = userdetails_form.cleaned_data['first_name']
            if userdetails_form.cleaned_data['last_name']:
                request.user.last_name = userdetails_form.cleaned_data['last_name']
            request.user.save()
            messages.success(request, _("Käyttäjätietojen vaihto onnistui."))
        
    else:
        #create an empty username form
        userdetails_form = ChangeUserDetailsForm(instance = request.user)
            
    return render_to_request_context_response(request, "user_control_panel.html", 
                {'userdetails_form':userdetails_form});

def login_error(request):
    messages.error(request, "Login failed.")
    return redirect_to(request, '/',False)

def register(request):
    if request.method == "POST":
        next_url = request.POST.get("next")
        form = forms.UserCreationFormUniqueEmail(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_new_social = False
                user.save()
                messages.success(request, _("Rekisterointi onnistui"))
                user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
                login(request,user)
                return redirect_to(request, next_url, False)
            except ValidationError:
                pass
    else:
        next_url = request.GET.get("next")
        form = forms.UserCreationFormUniqueEmail()
    return render_to_request_context_response(request,"registration/register.html", {"form" : form, "next" : next_url})
