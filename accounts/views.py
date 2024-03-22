from django.shortcuts import render, redirect
from accounts.forms import UserRegisterForm
from django.contrib.auth import authenticate, login
from django.contrib import messages


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Hey {username}! Your account has been created!")
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1']
                                    )
            login(request, new_user)
            return redirect("pages:home")
    else:
        form = UserRegisterForm()

    context = {'form': form, }

    return render(request, 'accounts/signup.html', context)
