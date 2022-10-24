from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from http import HTTPStatus

User = get_user_model()

URL_PLUS_TEMPLATE_FOR_ALL = {
    '/auth/logout/': 'users/logged_out.html',
    '/auth/signup/': 'users/signup.html',
    '/auth/login/': 'users/login.html',
    '/auth/password_reset/': 'users/password_reset.html',
    '/auth/password_reset/done/': 'users/password_reset_done.html',
    '/auth/password_reset_complete/': 'users/password_reset_complete.html',
    '/auth/reset/<uidb64>/<token>/': 'users/password_reset_confirm.html',
}
URL_PLUS_TEMPLATE_FOR_AUTH = {
    '/auth/password_change/': 'users/password_change.html',
    '/auth/password_change/done/': 'users/password_change_done.html',
}


class StaticURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        """Создаем тестовые записи"""
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(
            first_name='Leha',
            last_name='Lehin',
            username='leha-_-',
            email='leha@mail.com',
            password='lehaleha12',
        )
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_urls_for_all(self):
        """Проверяем страницы users для всех"""
        for address in URL_PLUS_TEMPLATE_FOR_ALL.keys():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_for_auth(self):
        """Проверяем страницы users для авторизированных"""
        for address in URL_PLUS_TEMPLATE_FOR_AUTH.keys():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """URL-адрес имеет правильный шаблон"""
        for address, template in {**URL_PLUS_TEMPLATE_FOR_AUTH,
                                  **URL_PLUS_TEMPLATE_FOR_ALL}.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
