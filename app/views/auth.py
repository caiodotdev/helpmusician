from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView, RedirectView

from app.forms import NewUserForm, LoginForm


class RegisterView(FormView):
    template_name = 'account/signup.html'
    form_class = NewUserForm
    success_url = '/app/'

    def form_valid(self, form):
        data = form.cleaned_data
        form.create(data)
        messages.success(self.request, "Usuario registrado com sucesso.")
        return super(RegisterView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Nao foi possivel registrar. Altere os dados e tente novamente.")
        return super(RegisterView, self).form_invalid(form)


class LoginView(FormView):
    template_name = 'account/login.html'
    form_class = LoginForm
    success_url = '/app/'

    def get(self, request, *args, **kwargs):
        return super(LoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        user = authenticate(self.request, username=data['username'], password=data['password'])
        if user is not None:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            messages.error(self.request, 'Credenciais invalidas, Tente novamente')
            return super(LoginView, self).form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Usuario ou senha invalidos.')
        return super(LoginView, self).form_invalid(form)


class LogoutUser(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(self.request)
        return super(LogoutUser, self).get(request, *args, **kwargs)
