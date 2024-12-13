from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import redirect, render
from recipe_catalog.forms import UserRegistrationForm, LoginForm
from recipe_catalog.constants import templates

def registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save() 
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, templates['registration_page'], {'form': form})

def login_view(request):
    form = LoginForm(data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                form.add_error(None, "Invalid username or password.")

    return render(request, templates['login_page'], {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')