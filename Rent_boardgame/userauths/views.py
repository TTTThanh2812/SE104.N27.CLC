from django.shortcuts import render, redirect
from userauths.froms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings

User = settings.AUTH_USER_MODEL

def register_view(request):
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        # print("User registred successfully")
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, You account was created successfully.", extra_tags='bg-green-500 text-white')
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect("core:home")
    
    else:       
        form = UserRegisterForm()
        # print("User cannot be registred")
    context = {
        'form': form,
    }
    return render(request, "userauths/sign_up.html", context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey you are alreadly Logged in.", extra_tags='bg-yellow-500 text-black')
        return redirect("core:home")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            # if it's raining
            user = User.objects.get(email=email)
        except:
            # It's not raining
            messages.warning(request, f"User with {email} dose not exist", extra_tags='bg-yellow-500 text-black')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"You are logged in.", extra_tags='bg-green-500 text-white')
            return redirect("core:home")
        else:
            messages.warning(request, f"User Dose Not Exits, create an account.", extra_tags='bg-yellow-500 text-black')

    context ={

    }
    
    return render(request, "userauths/sign_in.html", context)

def logout_view(request):
    logout(request)
    messages.warning(request, f"You logged out.", extra_tags='bg-yellow-500 text-black')
    
    return redirect("userauths:sign_in")