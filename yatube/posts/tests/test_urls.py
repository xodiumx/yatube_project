from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from posts.models import Post, Group
from http import HTTPStatus

User = get_user_model()


ONLY_CREATORS = 5
URL_PLUS_TEMPLATE_FOR_ALL = {
    '/': 'posts/index.html',
    '/group/test-slug/': 'posts/group_list.html',
    '/profile/mazar1n1/': 'posts/profile.html',
    '/posts/1/': 'posts/post_detail.html',
}
URL_PLUS_TEMPLATE_FOR_AUTH = {
    '/create/': 'posts/create_post.html',
    '/posts/1/edit/': 'posts/create_post.html',
    '/posts/1/delete/': 'posts/create_post.html',
}
COMMENT = {'/posts/1/comment/': 'includes/comment.html'}
PAGE_NOT_FOUND = {
    '/whereami/': 'core/404.html',
}


class StaticURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        """Создаем тестовые записи"""
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='mazar1n1')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
        )
        Group.objects.create(
            title='Тестовый заголовок',
            slug='test-slug',
            description='test description',
        )

    def test_public_pages(self):
        """Проверяем страницы доступные для всех
        и перенаправления для не авторизированных"""
        for address in URL_PLUS_TEMPLATE_FOR_ALL:
            with self.subTest(address=address):
                response = self.guest_client.get(address, follow=True)
                self.assertEqual(response.status_code, HTTPStatus.OK)

        for address in URL_PLUS_TEMPLATE_FOR_AUTH.keys():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertRedirects(
                    response, (f'/auth/login/?next={address}'))

    def test_comments_for_auth(self):
        """Комментарии может оставлять только, авторизированный пользователь"""
        response = self.guest_client.get(*COMMENT)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_pages_for_auth(self):
        """Проверяем страницы доступные для авторизированных"""
        for address in URL_PLUS_TEMPLATE_FOR_AUTH:
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_private_pages_for_creators(self):
        """Проверяем страницы доступные для авторов"""
        for address in [*URL_PLUS_TEMPLATE_FOR_AUTH][ONLY_CREATORS:]:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_urls_uses_correct_template(self):
        """Проверяем шаблоны страниц"""
        for address, template in {**URL_PLUS_TEMPLATE_FOR_ALL,
                                  **URL_PLUS_TEMPLATE_FOR_AUTH,
                                  **PAGE_NOT_FOUND,
                                  }.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
