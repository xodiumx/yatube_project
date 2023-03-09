import tempfile
import shutil

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.core.cache import cache
from django.conf import settings
from django.urls import reverse
from django import forms
from posts.models import Group, Post, Follow
from django.core.files.uploadedfile import SimpleUploadedFile


User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
TESTS_NOTATIONS = 13
INDEX = {reverse('posts:index'): 'posts/index.html'}
GROUP = {reverse('posts:group_list', kwargs={
    'slug': 'test-slug', }): 'posts/group_list.html'}
PROFILE = {reverse('posts:profile', kwargs={
    'username': 'mazar1n1', }): 'posts/profile.html'}
POST_DETAIL = {reverse('posts:post_detail', kwargs={
    'post_id': 1, }): 'posts/post_detail.html'}
POST_CREATE = {reverse('posts:post_create'): 'posts/create_post.html'}
POST_EDIT = {reverse('posts:post_edit', kwargs={
    'post_id': 1, }): 'posts/create_post.html'}
POST_DELETE = {reverse('posts:post_delete', kwargs={
    'post_id': 1, }): 'posts/create_post.html'}
COMMENT = {reverse('posts:add_comment', kwargs={
    'post_id': 1, }): 'includes/comment.html'}
FOLLOW = (reverse('posts:profile_follow', kwargs={
    'username': 'mazar1n1'}))
UNFOLLOW = (reverse('posts:profile_unfollow', kwargs={
    'username': 'mazar1n1'}))
FOLLOW_PAGE = {reverse('posts:follow_index'): 'posts/follow.html'}


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsPagesTestsViews(TestCase):

    @classmethod
    def setUpClass(cls):
        """Создаем тестовые записи"""
        super().setUpClass()
        cls.guest_client = Client()

        cls.user = User.objects.create_user(username='mazar1n1')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.user_second = User.objects.create_user(username='paradox')
        cls.authorized_client_second = Client()
        cls.authorized_client_second.force_login(cls.user_second)

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='test description',
        )
        SMALL_GIF = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=SMALL_GIF,
            content_type='image/gif'
        )
        for _ in range(TESTS_NOTATIONS):
            Post.objects.create(
                text='Тестовый текст',
                author=cls.user,
                group=cls.group,
                image=uploaded,
            )

    def tearDown(self):
        super().tearDown()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        cache.clear()

    def test_pages_uses_correct_namespace(self):
        """URL-адрес использует соответствующий namespace и шаблон."""
        for reverse_name, template in {**INDEX, **GROUP, **PROFILE,
                                       **POST_DETAIL, **POST_CREATE,
                                       **POST_EDIT, **POST_DELETE,
                                       **FOLLOW_PAGE}.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_posts_views_show_correct_context_first(self):
        """Проверяем передаваемый context во view-функциях 1
        ____________________________________________________
        Проверяем передан ли page_obj на страницах
        index, group_list, profile
        """
        for reverse_name in (*INDEX, *GROUP, *PROFILE):
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                resp_object = response.context['page_obj'][0]
                self.assertEqual(resp_object.text, 'Тестовый текст')
                self.assertEqual(resp_object.author.username, 'mazar1n1')
                self.assertEqual(resp_object.group.title, 'Тестовая группа')
                self.assertTrue(resp_object.image)

    def test_posts_views_show_correct_context_second(self):
        """Проверяем передаваемый context во view-функциях 2
        ____________________________________________________
        Проверям передано ли кол. постов автора на страницах:
        profile-а и post_detail
        """
        for reverse_name in (*PROFILE, *POST_DETAIL):
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                if response.context['count_post_of_author']:
                    self.assertEqual(response.context[
                        'count_post_of_author'], TESTS_NOTATIONS)

    def test_posts_views_show_correct_context_third(self):
        """Проверяем передаваемый context во view-функциях 3
        ____________________________________________________
        Проверяем передана ли форма на страницы:
        create, edit
        """
        for reverse_name in (*POST_CREATE, *POST_EDIT):
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                form_fields = {
                    'text': forms.fields.CharField,
                    'group': forms.fields.ChoiceField,
                }
                for value, expected in form_fields.items():
                    with self.subTest(value=value):
                        form_field = response.context.get(
                            'form').fields.get(value)
                        self.assertIsInstance(form_field, expected)

    def test_first_page_contains_ten_posts(self):
        """Paginator на первой странице выдает 10 записей"""
        response = self.authorized_client.get(*INDEX)
        self.assertEqual(
            len(response.context['page_obj']), TESTS_NOTATIONS - 3)

    def test_second_page_contains_three_posts(self):
        """Paginator на второй странице выдает оставшиеся записи"""
        response = self.authorized_client.get(str(*INDEX) + '?page=2')
        self.assertEqual(
            len(response.context['page_obj']), TESTS_NOTATIONS - 10)

    def test_cache_on_pages_with(self):
        """Проверяем кеширование на страницах
        _____________________________________
        index, group
        """
        index = 0
        for reverse_name in (*INDEX, *GROUP):
            with self.subTest(reverse_name=reverse_name):
                index += 1
                response = self.authorized_client.get(reverse_name)
                cached_content = response.content
                Post.objects.get(pk=index).delete()
                self.assertEqual(response.content, cached_content)

    def test_auth_user_can_subscribe_on_authors(self):
        """Авторизированный пользователь может подписаться на автора"""
        self.authorized_client_second.get(FOLLOW)
        self.assertEqual(Follow.objects.get(user_id=2).author_id, 1)

    def test_auth_user_can_unsubscribe_from_authors(self):
        """Авторизированный пользователь может отписаться от автора"""
        self.authorized_client_second.get(FOLLOW)
        self.authorized_client_second.get(UNFOLLOW)
        self.assertFalse(Follow.objects.filter(user_id=2).exists())

    def test_only_follower_can_see_posts_of_following_author(self):
        """Только подписчик может видеть посты автора, на странице подписок"""
        self.authorized_client_second.get(FOLLOW)
        response = self.authorized_client.get(*FOLLOW_PAGE)
        response_second = self.authorized_client_second.get(*FOLLOW_PAGE)
        self.assertFalse(response.context['page_obj'])
        self.assertTrue(response_second.context['page_obj'])
