from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect


# Create your views here.
class HomePageView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'all_posts_list'

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    success_url = reverse_lazy('home')
    fields = ['text']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('home')

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        super().delete(*args, **kwargs)
        return HttpResponseRedirect(reverse('home'))

class PostUpdateView(UpdateView):
    model = Post
    fields = ['text']
    template_name = 'post_form.html'
    success_url = reverse_lazy('home')
    initial = {}

    def get_initial(self):
        """initialize your's form values here"""

        base_initial = super().get_initial()
        # So here you're initiazing you're form's data
        base_initial['dataset_request'] = Post.objects.filter(
            text=self.request.user
        )
        return base_initial

    def form_valid(self, form):

        form.instance.user = self.request.user
        return super().form_valid(form)




