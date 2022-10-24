import shutil
import tempfile

from django.contrib.auth import get_user_model
from posts.models import Post, Comment
from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from http import HTTPStatus


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):

    @classmethod
    def setUpClass(cls):
        """Создаем тестовые записи"""
        super().setUpClass()
        cls.user = User.objects.create_user(username='mazar1n1')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        posts_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Тестовый текст 2',
            'image': uploaded,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:profile', kwargs={
            'username': self.user,
        }))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.get(
                text='Тестовый текст 2',
            ).image)

    def test_cant_creating_blank_post(self):
        """Проверяем возможность создания пустого поста"""
        posts_count = Post.objects.count()
        form_data = {
            'text': '',
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertFormError(
            response,
            'form',
            'text',
            'Обязательное поле.'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_editing_posts(self):
        """Проверяем возможность редактирования поста"""
        form_data = {
            'text': 'Новый текст',
        }
        self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': 1}),
            data=form_data,
            follow=True
        )
        self.assertNotEqual(Post.objects.get(pk=1).text, 'Тестовый текст')

    def test_deleting_posts(self):
        """Проверяем возможность удаления поста"""
        form_data = {
            'text': 'Тестовый текст',
        }
        self.authorized_client.post(
            reverse('posts:post_delete', kwargs={'post_id': 1}),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.filter(pk=1).exists(), False)

    def test_adding_comments(self):
        """Валидная форма создает комментарий"""
        comments_count = Comment.objects.count()
        form_data = {
            'text': 'Новый комментарий'
        }
        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': 1}),
            data=form_data,
            follow=True
        )
        self.assertEqual(Comment.objects.count(), comments_count + 1)
        self.assertEqual(Comment.objects.filter(pk=1).exists(), True)
        self.assertRedirects(response, reverse('posts:post_detail', kwargs={
            'post_id': 1,
        }))
