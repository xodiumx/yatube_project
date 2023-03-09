from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, View)

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User
from .utils import pagination


class Index(ListView):
    paginate_by = 10
    queryset = Post.objects.select_related('author').all()
    template_name = 'posts/index.html'


class GroupPosts(ListView):
    model = Post
    pagiante_by = 10
    template_name = 'posts/group_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        context['group'] = group
        context['page_obj'] = group.posts.all()
        return context


class Profile(ListView):
    model = Post
    template_name = 'posts/profile.html'

    def get_context_data(self, **kwargs):
        author = get_object_or_404(User, username=self.kwargs.get('username'))
        posts_list = Post.objects.filter(author=author).select_related(
            'author').all()
        context = super().get_context_data(**kwargs)
        context['author'] = author
        context['count_post_of_author'] = posts_list.count()
        context['page_obj'] = pagination(self.request, posts_list)
        context['followed'] = Follow.objects.filter(
            user=self.request.user.id, author=author.id).exists()
        return context


class PostDetail(DetailView):
    model = Post
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'
    template_name = 'posts/post_detail.html'

    def get_context_data(self, **kwargs):
        comments = self.object.comments.all()
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['page_obj'] = pagination(self.request, comments)
        context['count_post_of_author'] = self.object.author.posts.count()
        return context


@method_decorator(login_required, name='dispatch')
class PostCreate(CreateView):
    form_class = PostForm
    http_method_names = ('post', 'get')
    template_name = 'posts/create_post.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('posts:profile',
                       kwargs={'username': self.request.user, })


class CantChangeNotYourPost(DetailView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.id != self.object.author.id:
            return redirect(f'/posts/{self.object.id}/')
        return super().get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class PostEdit(UpdateView, CantChangeNotYourPost):
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    http_method_names = ('post', 'get')
    template_name = 'posts/create_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context

    def get_success_url(self):
        return reverse('posts:post_detail',
                       kwargs={'post_id': self.object.id, })


@method_decorator(login_required, name='dispatch')
class PostDelete(DeleteView, CantChangeNotYourPost):
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    http_method_names = ('post', 'get')
    template_name = 'posts/create_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_delete'] = True
        return context

    def get_success_url(self):
        return reverse('posts:profile',
                       kwargs={'username': self.request.user, })


@method_decorator(login_required, name='dispatch')
class AddComment(CreateView):
    form_class = CommentForm
    http_method_names = ('post', 'get')
    template_name = 'posts/create_post.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.post_id = self.kwargs.get('post_id')
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('posts:post_detail',
                       kwargs={'post_id': self.object.post_id, })


@method_decorator(login_required, name='dispatch')
class FollowIndex(ListView):
    model = Post
    template_name = 'posts/follow.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        follows_id_list = user.follower.all().values_list(
            'author_id', flat=True
        )
        follows_posts = Post.objects.filter(
            author_id__in=follows_id_list).all()
        context = super().get_context_data(**kwargs)
        context['page_obj'] = pagination(self.request, follows_posts)
        return context


@method_decorator(login_required, name='dispatch')
class FollowAndUnfollowProfile(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        author = get_object_or_404(User, username=kwargs.get('username'))
        url_name = self.request.resolver_match.url_name

        if user == author:
            return redirect(f'/profile/{author}/')

        if url_name == 'profile_follow':
            if not Follow.objects.filter(
                    user=user.id, author=author.id
            ).exists():
                Follow.objects.create(user=user, author=author)
                return redirect(f'/profile/{author}/')

        elif url_name == 'profile_unfollow':
            follow_object = Follow.objects.filter(
                user=user.id, author=author.id)
            if follow_object.exists():
                follow_object.delete()
                return redirect(f'/profile/{author}/')


@method_decorator(login_required, name='dispatch')
class Subscribers(ListView):
    model = User
    template_name = 'posts/subscribers.html'

    def get_context_data(self, **kwargs):
        author = get_object_or_404(User, username=self.kwargs.get('username'))
        subscribers = author.following.select_related('user')
        context = super().get_context_data(**kwargs)
        context['author'] = author
        context['count_of_subs'] = len(subscribers)
        context['page_obj'] = pagination(self.request, subscribers)
        return context


@method_decorator(login_required, name='dispatch')
class Subscriptions(ListView):
    model = User
    template_name = 'posts/subscriptions.html'

    def get_context_data(self, **kwargs):
        author = get_object_or_404(User, username=self.kwargs.get('username'))
        subscriptions = author.follower.select_related('author')
        context = super().get_context_data(**kwargs)
        context['author'] = author
        context['count_of_subp'] = len(subscriptions)
        context['page_obj'] = pagination(self.request, subscriptions)
        return context
