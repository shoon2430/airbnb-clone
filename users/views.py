import os
import requests
from pprint import pprint


from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.contrib.auth.forms import UserCreationForm

from . import forms
from . import models

# Create your views here.


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    initial = {"email": "hoon@naver.com"}

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)

        return HttpResponseRedirect(self.get_success_url())


# class LoginView(View):
#     def get(self, request):

#         form = forms.LoginForm(initial={"email": "hoon@naver.com"})
#         return render(request, "users/login.html", {"form": form})

#     def post(self, request):
#         form = forms.LoginForm(request.POST)

#         if form.is_valid():
#             pprint(form.cleaned_data)

#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 print("login~")
#                 login(request, user)
#                 return redirect(reverse("core:home"))
#         return render(request, "users/login.html", {"form": form})


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignupView(FormView):

    template_name = "users/signup.html"
    form_class = forms.SignupForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)

        user.verify_email()
        return HttpResponseRedirect(self.get_success_url())


def complete_verification(request, key):

    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do : add success massage
    except models.User.DoesNotExist:
        # to do Error massage
        pass

    return redirect(reverse("core:home"))


def github_login(request):

    client_id = os.environ.get("GITHUB_ID")
    redirect_uri = "http://localhost:8000/user/continue/github/callback"

    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    print("GithubException")


def github_callback(request):
    # pprint(request.GET)
    try:
        client_id = os.environ.get("GITHUB_ID")
        client_secret = os.environ.get("GITHUB_SECRET")
        code = request.GET.get("code", None)

        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)

            if error is not None:
                raise GithubException()
            else:
                access_token = token_json.get("access_token", None)
                profile = requests.get(
                    "https://api.github.com/user",
                    headers={"Authorization": f"token {access_token}"},
                )
                profile_json = profile.json()
                pprint(profile_json)
                username = profile_json.get("login", "")
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")

                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException()
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            username=email,
                            first_name=name,
                            email=email,
                            bio=bio,
                            email_verified=True,
                            login_method=models.User.LOGIN_GITHUB,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException()
        else:
            raise GithubException()
    except GithubException:
        return redirect(reverse("users:login"))


def kakao_login(request):

    app_key = os.environ.get("KAKAO_REST_API")
    redirect_uri = "http://localhost:8000/user/continue/kakao/callback"

    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_key}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakacoException(Exception):
    pass


def kakao_callback(request):
    try:
        app_key = os.environ.get("KAKAO_REST_API")
        redirect_uri = "http://localhost:8000/user/continue/kakao/callback"
        code = request.GET.get("code")
        if code is not None:
            token_request = requests.post(
                f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={app_key}&redirect_uri={redirect_uri}&code={code}&"
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise KakacoException()

            access_token = token_json.get("access_token")
            profile_request = requests.get(
                f"https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            profile_json = profile_request.json()
            email = profile_json.get("kakao_account").get("email", None)

            if email is not None:
                properties = profile_json.get("properties")
                nickname = properties.get("nickname")
                profile_image = properties.get("profile_image")

                try:
                    user = models.User.objects.get(email=email)
                    if user.login_method != models.User.LOGIN_KAKAO:
                        raise KakacoException()

                except models.User.DoesNotExist:
                    user = models.User.objects.create(
                        email=email,
                        username=email,
                        first_name=nickname,
                        login_method=models.User.LOGIN_KAKAO,
                        email_verified=True,
                    )
                    user.set_unusable_password()
                    user.save()
                    if profile_image is not None:
                        photo_request = requests.get(profile_image)
                        user.avatar.save(
                            f"{nickname}-avatar", ContentFile(photo_request.content)
                        )

                login(request, user)
                return redirect(reverse("core:home"))
            else:
                raise KakacoException()
        else:
            raise KakacoException()
    except KakacoException:
        return redirect(reverse("users:login"))

