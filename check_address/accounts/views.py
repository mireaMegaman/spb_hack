from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.forms import UserRegisterForm
from django.views import View
from django.contrib.auth.decorators import login_required

# Create your views here.

class RegistrationView(View):
    context = {}

    def get(self, request):
        form = UserRegisterForm()
        self.context['form'] = form
        return render(request, 'register.html', context=self.context)
    
    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт {username}!')
            return redirect('text')
        else:
            raise Http404


@login_required
def profile(request):
    return render(request, 'profile.html')