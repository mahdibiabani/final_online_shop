from django.shortcuts import render, redirect
from accounts.forms import UserRegisterForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings

User = settings.AUTH_USER_MODEL


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


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('pages:home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.warning(request, f"User with email {email} does not exist")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"you are logged in as {user.username}")
            return redirect("pages:home")
        else:
            messages.warning(request, f"user does not exist")

    context = {
    }
    return render(request, 'accounts/login.html', context)
