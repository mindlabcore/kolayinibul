from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
from .forms import LoginForm, SignupForm, ResetForm, ChangePasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Avatar, Profile


def sign_up(request):
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in. Are you sick?")
        return redirect("index")
    else:
        form = SignupForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            date_of_birth = form.cleaned_data.get("date_of_birth")

            newUser = User(username=username)
            newUser.set_password(password)
            newUser = User(email=email)
            newUser = User(date_of_birth=date_of_birth)
            # kullanıcıyı kayıt ettik ve doğrudan login yaptık
            newUser.save()
            login(request, newUser)
            messages.success(request, "Congratulation! Welcome.")
            return redirect("index")
        context = {

            "form": form
        }
        return render(request, "login_logout_signup/sign_up.html", context)


def login_user(request):
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in. Are you sick?")
        return redirect("index")
    else:
        print("*" * 30)
        print(request.GET)
        print("*" * 30)
        form = LoginForm(request.POST or None)
        context = {
            "form": form
        }
        go_to = request.POST.get('next', '/')  # GET ile next parametresinin değerini aldık
        print("/" * 30)
        print(go_to)
        print("/" * 30)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is None:
                messages.info(request, "Username or Password is incorrect! Try again.")
                return render(request, "login_logout_signup/login.html", context)

            messages.success(request, "Login successful! Welcome honey.")
            login(request, user)
            print("l" * 30)
            go_to = request.POST.get('next', '/')
            print("l" * 30)
            if go_to:
                go_to = request.POST.get(
                    'next')
                return redirect(go_to)  # GET ile aldığımız parametreyi go_to'ya atayıp return ettik.
                # Burada GET ile alırsak querydict none olarak dönüyor bir sebepten dolayı.
                # O yüzden POST ile next parametresini göndermeliyiz.
            else:

                return redirect("index")
        return render(request, "login_logout_signup/login.html", context)


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "Logout successful! Goodbye motherfucker! :)")
    return render(request, "login_logout_signup/logout.html")


def send_reset_link(request):
    form = ResetForm(request.POST or None)
    context = {
        "form": form
    }

    if form.is_valid():
        email = form.cleaned_data.get("email")

        if email is None:
            messages.info(request, "This e-mail is not registered! Try again.")
            return render(request, "login_logout_signup/reset_password.html", context)

        messages.success(request, "We sent link to your email for reset your password.")
        return redirect("index")

    return render(request, "login_logout_signup/reset_password.html", context)


def create_new_password(request):
    form = ChangePasswordForm(request.POST or None)
    context = {
        "form": form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        user = authenticate(username=username)

        if user is None:
            messages.info(request, "Username is incorrect! Try again.")
            return render(request, "login_logout_signup/create_new_password.html", context)

        messages.success(request, "We sent link to your email for reset your password.")
        return redirect("index")

    return render(request, "login_logout_signup/create_new_password.html", context)


@login_required
def upload_pic(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = Avatar.objects.get(pk=id)
            m.model_pic = form.cleaned_data['image']
            m.save()
            return HttpResponse('image upload success')
    return HttpResponseForbidden('allowed only via POST')


@login_required
def profile(request, slug):
    #  detail = Profile.objects.filter(id=id)
    #  profile_detail = Profile.objects.filter(slug=slug)
    profile_detail = get_object_or_404(Profile, slug=slug)
    context = {
        "profile_detail": profile_detail
    }
    return render(request, "profile_pages/profile.html", context)
