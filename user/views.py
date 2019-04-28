from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import LoginForm, SignupForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Profile
from django.contrib.auth import update_session_auth_hash
from blog.models import Post
from job.models import JobAdvertisement
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm


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


            newUser = User(username=username, email=email)
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


def profile(request, slug):
    #  detail = Profile.objects.filter(id=id)
    #  profile_detail = Profile.objects.filter(slug=slug)
    profile_detail = get_object_or_404(Profile, slug=slug)
    user_posts = Post.objects.filter(author=profile_detail.id)
    user_jobs = JobAdvertisement.objects.filter(employer=profile_detail.id)

    context = {
        "profile_detail": profile_detail,
        "user_posts": user_posts,
        "user_jobs": user_jobs,
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


@login_required
def update_profile(request):
    #  Profile sayfası.
    profile = get_object_or_404(Profile, user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if profile.user != request.user:
        messages.error(request, "Bu işlem için yetkili değilsiniz!")
        return redirect("my_profile")

    else:
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.updated_date = timezone.now()
            profile.save()
            form.save_m2m()

            messages.success(request, "Profil bilgileri başarıyla değiştirildi!")
            return redirect("my_profile")
        context = {
            "profile": profile,
            "form": form,
        }
    return render(request, "profile_pages/edit_profile.html", context)


@login_required
def github_password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Parolanız başarıyla güncellendi!')
            return redirect('my_profile')
        else:
            messages.error(request, 'Lütfen hataları düzeltin.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'login_logout_signup/github_password_set.html', {'form': form})
