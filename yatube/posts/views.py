from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, Follow, User
from .forms import CommentForm, PostForm
from .utils import pagination


def index(request):
    """Главная страница сайта"""
    template = 'posts/index.html'
    about_page = 'Последние обновления на сайте'
    posts_list = Post.objects.select_related(
        'author'
    ).order_by('-created').all()

    context = {
        'about_page': about_page,
        'page_obj': pagination(request, posts_list),
    }
    return render(request, template, context)


def group_posts(request, slug):
    """Страница групп сайта"""
    group = get_object_or_404(Group, slug=slug)
    template = 'posts/group_list.html'
    posts_list = group.posts.all().order_by('-created')

    context = {
        'group': group,
        'page_obj': pagination(request, posts_list),
    }
    return render(request, template, context)


def profile(request, username):
    """Страница профиля пользователя"""
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    user = request.user

    posts_list = Post.objects.filter(author=author).select_related(
        'author'
    ).order_by('-created').all()

    context = {
        'author': author,
        'count_post_of_author': posts_list.count(),
        'page_obj': pagination(request, posts_list),
        'followed': Follow.objects.filter(
            user=user.id, author=author.id).exists(),
    }
    return render(request, template, context)


def post_detail(request, post_id):
    """Страница поста"""
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)

    comments = post.comments.all()
    form = CommentForm()

    context = {
        'post': post,
        'count_post_of_author': post.author.posts.count(),
        'form': form,
        'page_obj': pagination(request, comments),
    }
    return render(request, template, context)


@login_required
@require_http_methods(["GET", "POST"])
def post_create(request):
    """Страница создания поста"""
    template = 'posts/create_post.html'
    nickname = request.user.get_username()
    if request.method == 'POST':
        form = PostForm(request.POST or None,
                        files=request.FILES or None,)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect(f'/profile/{nickname}/')
        return render(request, template, {'form': form})
    form = PostForm()
    return render(request, template, {'form': form})


@login_required
@require_http_methods(["GET", "POST"])
def post_edit(request, post_id):
    """Страница редактирования поста, если пользователь не явлется создателем,
    он не может редатировать пост"""
    post = get_object_or_404(Post, id=post_id)

    template = 'posts/create_post.html'
    user_obj = request.user

    if user_obj.id != post.author.id:
        return redirect(f'/posts/{post.id}/')

    form = PostForm(request.POST or None,
                    instance=post,
                    files=request.FILES or None,
                    )
    context = {
        'form': form,
        'post': post,
        'is_edit': True,
    }

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(f'/posts/{post.id}/')
    return render(request, template, context)


@login_required
@require_http_methods(["GET", "POST"])
def post_delete(request, post_id):
    """Страница удаления поста, если пользователь не явлется создателем,
    он не может удалить пост"""
    template = 'posts/create_post.html'

    post = get_object_or_404(Post, id=post_id)
    user_obj = request.user

    context = {
        'post': post,
        'is_delete': True,
    }
    if user_obj.id != post.author.id:
        return redirect(f'/posts/{post.id}/')

    if request.method == 'POST':
        Post.objects.get(id=post_id).delete()
        return redirect(f'/profile/{user_obj}/')

    return render(request, template, context)


@login_required
@require_http_methods(["POST"])
def add_comment(request, post_id):
    """Добавление комментария к посту"""
    form = CommentForm(request.POST or None,)
    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post_id = post_id
            comment.save()
        return redirect(f'/posts/{post_id}/')


@login_required
def follow_index(request):
    """Лента подписок"""
    template = 'posts/follow.html'
    user = request.user

    follows_id_list = user.follower.all().values_list(
        'author_id', flat=True
    )

    follows_posts = Post.objects.filter(
        author_id__in=follows_id_list
    ).order_by('-created').all()

    context = {
        'page_obj': pagination(request, follows_posts),
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    """Лайк, подписка"""
    user = request.user
    author = get_object_or_404(User, username=username)

    if user == author:
        return redirect(f'/profile/{author}/')

    if not Follow.objects.filter(user=user.id, author=author.id).exists():
        Follow.objects.create(user=user, author=author)
        return redirect(f'/profile/{author}/')

    return redirect(f'/profile/{author}/')


@login_required
def profile_unfollow(request, username):
    """Дизлайк, отписка"""
    user = request.user
    author = get_object_or_404(User, username=username)

    if Follow.objects.filter(user=user.id, author=author.id).exists():

        Follow.objects.filter(user=user.id, author=author.id).delete()
        return redirect(f'/profile/{author}/')


@login_required
def subscribers(request, username):
    """Страница с подписчиками пользователя"""
    template = 'posts/subscribers.html'
    author = get_object_or_404(User, username=username)

    subscribers_of_author_page = author.following.select_related('user')
    context = {
        'page_obj': pagination(request, subscribers_of_author_page),
        'count_of_subs': len(subscribers_of_author_page),
        'author': author,
    }
    return render(request, template, context)


@login_required
def subscriptions(request, username):
    """Страница с подписками пользователя"""
    template = 'posts/subscriptions.html'
    author = get_object_or_404(User, username=username)

    subscriptions_of_author_page = author.follower.select_related('author')
    context = {
        'page_obj': pagination(request, subscriptions_of_author_page),
        'count_of_subp': len(subscriptions_of_author_page),
        'author': author,
    }
    return render(request, template, context)
