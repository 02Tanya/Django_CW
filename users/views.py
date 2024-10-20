import random
import secrets

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from config import settings
from users.forms import RecoverForm, RegistrationForm, UserForm, UserModerationForm
from users.models import User


# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = RegistrationForm

    def get_success_url(self):
        return reverse("users:login")

    def form_valid(self, form):
        user = form.save()
        token = secrets.token_hex(16)
        user.token = token
        user.is_active = False
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/verify/{token}"
        message = f"Привет, для подтверждения почты тебе нужно перейти по ссылке: {url}"
        send_mail("Верификация почты", message, settings.EMAIL_HOST_USER, [user.email])
        return super().form_valid(form)


def verify(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


def restore_access(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.get(email=email)
        new_password = "".join([str(random.randint(0, 9)) for _ in range(8)])

        message = f"Ваш новый пароль : {new_password}"
        send_mail(
            "Восстановление доступа", message, settings.EMAIL_HOST_USER, [user.email]
        )
        user.set_password(new_password)
        user.save()
        return redirect(reverse("users:login"))
    else:
        form = RecoverForm
        context = {"form": form}
        return render(request, "users/restore.html", context)


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = "users/user_list.html"
    permission_required = ("users.view_user",)

    def get_queryset(self):
        customer_list = super().get_queryset()
        user = self.request.user
        if user.is_blocked == True:
            raise Http404("Вы заблокрованы")
        else:
            return customer_list


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "users/user_form1.html"
    form_class = UserForm
    success_url = reverse_lazy("users:user_list")

    def get_object(self, queryset=None):
        """редактируем текущего пользователя без передачи пк"""
        return self.request.user


class UserModerationView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserModerationForm
    template_name = "users/user_form2.html"
    permission_required = ("users.block_users",)

    def get_success_url(self):
        return reverse_lazy("users:user_list")
