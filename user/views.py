from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
from .forms import LoginForm, SignupForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail, EmailMessage, BadHeaderError
from django.template.loader import render_to_string


def sign_up(request):
    if request.user.is_authenticated:
        messages.warning(request, "Zaten giriş yapmıştın. Hasta mısın?")
        return redirect("index")
    else:
        form = SignupForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")

            newUser = User(username=username, email=email, first_name=first_name, last_name=last_name)
            newUser.set_password(password)

            # kullanıcıyı kayıt ettik ve doğrudan login yaptık
            newUser.save()
            login(request, newUser)
            messages.success(request, "Tebrikler! Aramıza hoşgeldin.")
            return redirect("index")
        context = {

            "form": form
        }
        return render(request, "login_logout_signup/sign_up.html", context)


def login_user(request):
    if request.user.is_authenticated:
        messages.notice(request, "Zaten giriş yapmıştın. Hasta mısın?")
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
                messages.info(request, "Kullanıcı adı veya parola hatalı. Lütfen tekrar dene!")
                return render(request, "login_logout_signup/login.html", context)

            messages.success(request, "Giriş yaptın. Hoşgeldin! :)")
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
    messages.success(request, "Hoşçakal! Tekrar gel olur mu? :'(")
    #  return render(request, "login_logout_signup/logout.html")
    return redirect("index")


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


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Parolanız başarıyla değiştirildi!')
            return redirect('index')
        else:
            messages.error(request, 'Lütfen hataları düzeltin.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'login_logout_signup/change_password.html', {
        'form': form
    })


def contact_us(request):
    form = ContactUsForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        cName = form.cleaned_data.get("cName")
        cEmail = form.cleaned_data.get("cEmail")
        cMessage = form.cleaned_data.get("cMessage")

        body = context
        sending = EmailMessage('Parola Sıfırlama', body, to=["iletisim@kolayinibul.com"])
        sending.send()
        messages.success(request, "Mesajınızı aldık, teşekkür ederiz!")
        return redirect("index")
    messages.warning((request,))
    return render(request, "help_pages/contact_us.html", context)



