from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, hashers, authenticate, login, logout
from django.contrib import messages
from django.views import View
from .forms import RegisterForm, LoginForm

User = get_user_model()


class RegisterView(View):

    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            # first_name = request.POST.get('first_name')
            first_name = form.cleaned_data.get('first_name')
            # last_name = request.POST.get('last_name')
            last_name = form.cleaned_data.get('last_name')
            # email = request.POST.get('email')
            email = form.cleaned_data.get('email')
            # username = request.POST.get('username')
            username = form.cleaned_data.get('username')
            # password1 = request.POST.get('password')
            password1 = form.cleaned_data.get('password')
            # password2 = request.POST.get('password_confirm')
            password2 = form.cleaned_data.get('password_confirm')

            if password1 == password2:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists!')
                    return redirect('/accaunt/register')
                elif User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already exists!')
                    return redirect('/accaunt/register')
                else:
                    user = User.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        username=username,
                        password=hashers.make_password(password1)
                    )
                    user.save()
                    return redirect('/accaunt/login')
            else:
                messages.error(request, 'Passwords are not same!')
                return redirect('/accaunt/register')


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Username or password invalid!')
                return redirect('/accaunt/login')


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('/')
