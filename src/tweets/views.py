from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.db.models import Q
from .forms import TweetModelForm
from .models import Tweet
from .mixins import FormUserNeededMixin, UserOwnerMixin
from django.urls import reverse_lazy as r, reverse
# Create your views here.

# CRUD (Create & Retrieve & Update & Delete )

# Create

class RetweetView(View):
    def get(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        if request.user.is_authenticated:
            new_tweet = Tweet.objects.retweet(request.user, tweet)
            return HttpResponseRedirect("/")
        return HttpResponseRedirect(tweet.get_absolute_url())


class TweetCreateView(LoginRequiredMixin, FormUserNeededMixin, CreateView):
    form_class = TweetModelForm
    template_name = 'tweets/create_view.html'
    #success_url = r('tweet:detail')
    # login_url = '/admin/'


# Retrieve


class TweetDetailView(DetailView):
    queryset = Tweet.objects.all()
    # template_name = "tweets/detail_view.html"


    # def get_object(self):
    #     print(self.kwargs)
    #     pk = self.kwargs.get("pk")
    #     obj = get_object_or_404(Tweet, pk=pk)
    #     return obj


class TweetListView(LoginRequiredMixin, ListView):
    def get_queryset(self, *args, **kwargs):
        q = Tweet.objects.all()
        query = self.request.GET.get("q", None)
        if query is not None:
            q = q.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )
        return q

    def get_context_data(self, *args, **kwargs):
        context = super(TweetListView, self).get_context_data(*args, **kwargs)
        context["create_form"] = TweetModelForm()
        context["create_url"] = r("tweet:create")
        # print(context)
        return context

def tweet_detail_view(request, pk=None):
    obj = get_object_or_404(Tweet, pk=pk)
    print(obj)
    context = {
        "object": obj
    }
    return render(request, 'tweets/detail_view.html', context)


# Update


class TweetUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    queryset = Tweet.objects.all()
    form_class = TweetModelForm
    template_name = 'tweets/update_view.html'
    #success_url = "/tweet/"

# Delete


class TweetDeleteView(LoginRequiredMixin, DeleteView):
    model = Tweet
    template_name = 'tweets/delete_confirm.html'
    success_url = r('tweet:list')




# List / Search


