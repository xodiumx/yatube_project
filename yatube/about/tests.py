from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from http import HTTPStatus

User = get_user_model()
URL_PLUS_TEMPLATE = {
    '/about/author/': 'about/author.html',
    '/about/tech/': 'about/tech.html',
}


class StaticURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        """Создаем гостевого пользователя"""
        super().setUpClass()
        cls.guest_client = Client()

    def test_urls_in_about(self):
        """Проверяем статичные страницы"""
        for address in URL_PLUS_TEMPLATE.keys():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_templates(self):
        """Проверяем шаблоны статичных страниц"""
        for address, template in URL_PLUS_TEMPLATE.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)
