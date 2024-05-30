from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView

from accounts.forms import SignUpForm, LoginForm, UpdateUserForm, UpdateProfileForm
from accounts.models import ExtendedUser


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = 'registration/signup.html'

    def dispatch(self, request, *args, **kwargs):
        # перенаправит на домашнюю страницу, если пользователь попытается получить доступ к странице регистрации
        # после авторизации
        if request.user.is_authenticated:
            return redirect(to='/')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('blog:post_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blog:post_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super().form_valid(form)


class ProfileViews(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UpdateUserForm(instance=self.request.user)
        context['profile_form'] = UpdateProfileForm(instance=self.request.user.profile)
        return context

    def post(self, request, *args, **kwargs):
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль успешно обновлен')
            return redirect('users-profile')
        else:
            context = self.get_context_data()
            context['user_form'] = user_form
            context['profile_form'] = profile_form
            return self.render_to_response(context)


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'registration/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-profile')


class VerifyView(View):
    template_name = 'registration/activate.html'

    def get(self, request, uuid):
        user = get_object_or_404(ExtendedUser, verification_uuid=uuid, is_verified=False)
        user.is_verified = True
        user.is_active = True
        user.save()
        return render(request, self.template_name)