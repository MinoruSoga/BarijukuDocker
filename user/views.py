from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

# from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from django.views.generic import View, FormView, CreateView
from .forms import RegisterForm
from student.models import Student


class GuestOnlyView(View):
    def dispatch(self, request, *args, **kwargs):
        # Redirect to the index page if the user already authenticated
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    template_name = "user/login.html"

    def form_valid(self, form):
        user = form.get_user()
        # ユーザータイプに応じたリダイレクト先を設定します。
        login(self.request, user)
        if user.user_type == "STUDENT":
            try:
                student = Student.objects.get(user=user)
                if student.stripe_data is not None:
                    return redirect("/student/")
                else:
                    return redirect("/student/prof/")
            except Student.DoesNotExist:
                return redirect("/student/prof/")
            # if Student.objects.filter(user=user).exists():
            #     return redirect("/student/")
            # else:
            #     return redirect("/student/prof/")
        elif user.user_type == "TRAINER":
            return redirect("/trainer/")
        elif user.user_type == "SHOP":
            return redirect("/shop/")
        else:
            logout(self.request)
        return super().form_valid(form)


class RegisterView(GuestOnlyView, FormView):
    template_name = "user/register.html"
    form_class = RegisterForm

    def form_valid(self, form):
        request = self.request
        user = form.save(commit=False)
        user.is_active = True
        user.user_type = "STUDENT"
        user.save()

        # user_status = UserStatus()
        # user_status.status = 0 # Student
        # user_status.user = user
        # user_status.save()

        raw_password = form.cleaned_data["password1"]

        user = authenticate(username=user.username, password=raw_password)
        login(request, user)

        messages.success(request, "登録できました。")

        return redirect("student:prof")

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('/student/')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'user/register.html', {'form': form})
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/user/login/")
