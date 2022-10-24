from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


User = get_user_model()


class UserCreateFormTests(TestCase):

    @classmethod
    def setUpClass(cls):
        """Создаем гостевого пользователя"""
        super().setUpClass()
        cls.guest_client = Client()

    def test_create_user(self):
        """Проверка регистрации пользователя"""
        users_count = User.objects.count()

        users = [
            {
                'first_name': 'Leha',
                'last_name': 'Lehin',
                'username': 'leha-_-',
                'email': 'leha@mail.com',
                'password1': 'lehaleha12',
                'password2': 'lehaleha12',
            },
            {
                'first_name': 'Alisa',
                'last_name': 'Alisova',
                'username': 'alisa-_-',
                'email': 'alisa@mail.com',
                'password1': 'alisaalisa12',
                'password2': 'alisaalisa12',
            }
        ]
        for i in users:
            response = self.guest_client.post(
                reverse('users:signup'),
                data=i,
                follow=True
            )
            self.assertRedirects(response, reverse('posts:index'))
            self.assertEqual(User.objects.count(), users_count + 1)
            users_count += 1

        self.assertEqual(User.objects.get(pk=1).username, 'leha-_-')
        self.assertEqual(User.objects.get(pk=2).username, 'alisa-_-')
        self.assertEqual(User.objects.get(pk=1).email, 'leha@mail.com')
        self.assertEqual(User.objects.get(pk=2).email, 'alisa@mail.com')
