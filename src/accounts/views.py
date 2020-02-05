from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.views import View
from .models import UserProfile
from django.views.generic.edit import FormView
# Create your views here.
from .forms import UserRegisterForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate
from django.utils.text import slugify




# User = get_user_model()

class UserRegisterView(FormView):
    template_name = 'accounts/user_register_form.html'
    form_class = UserRegisterForm
    success_url = '/login'

    def form_valid(self, form):
        context = self.get_context_data()
        form = context['form']
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            new_user = UserProfile.objects.create(username=username, email=email)
            new_user.set_password(password)
            new_user.avatar = form.cleaned_data.get("avatar")
            print("avatar => ", form.cleaned_data.get("avatar"))
            new_user.save()
            return super(UserRegisterView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(UserRegisterView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = UserRegisterForm(self.request.POST, self.request.FILES)
        else:
            context['form'] = UserRegisterForm()
        return context
# def tweet_detail_view(request, pk=None):
#     obj = get_object_or_404(Tweet, pk=pk)
#     print(obj)
#     context = {
#         "object": obj
#     }
#     return render(request, 'tweets/detail_view.html', context)

#
# def profileData(request, slug):
#         obj = get_object_or_404(UserData, slug=slug)
#         print(obj)
#         context = {
#             'object': obj
#         }
#         return render(request, 'accounts/profile.html', context)


# class UserDataDetailView(DetailView):
#     queryset = UserData.objects.all()
#     print(queryset)
#     # for query in queryset:
#     #     queryset_country = query.country
#     #     if queryset_country:
#     #         print(query.country)
#     #     else:
#     #         print("No Country for this user")
#     template_name = "registration/profile.html"
#
#     def get_object(self):
#         return get_object_or_404(
#             User,
#             username__iexact=self.kwargs.get("username"),
#
#         )
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(UserDataDetailView, self).get_context_data(*args, **kwargs)
#         return context





class UserDetailView(DetailView):
    template_name = "accounts/user_detail.html"
    queryset = UserProfile.objects.all()

    def get_object(self):
        return get_object_or_404(
            UserProfile,
            username__iexact=self.kwargs.get("username"),

        )

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailView, self).get_context_data(*args, **kwargs)
        following = UserProfile.objects.is_following(self.request.user, self.get_object())
        context['following'] = following
        context['recommended'] = UserProfile.objects.recommended(self.request.user)
        return context






class UserFollowView(View):
    def get(self, request, username, *args, **kwargs):
        toggle_user = get_object_or_404(UserProfile, username__iexact=username)
        if request.user.is_authenticated:
            is_following = UserProfile.objects.toggle_follow(request.user, toggle_user)
        return redirect("profiles:detail", username=username)  #HttpResponseRedirect()