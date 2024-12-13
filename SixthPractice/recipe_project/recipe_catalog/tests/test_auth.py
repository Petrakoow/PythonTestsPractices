from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

class AuthenticationTests(TestCase):

    def setUp(self):
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.registration_url = reverse('registration')
        self.user_credentials = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        self.user = User.objects.create_user(**self.user_credentials)

    def test_login_url_resolves(self):
        """Проверка, что URL для входа соответствует правильному представлению."""
        self.assertEqual(resolve(self.login_url).url_name, 'login')

    def test_logout_url_resolves(self):
        """Проверка, что URL для выхода соответствует правильному представлению."""
        self.assertEqual(resolve(self.logout_url).url_name, 'logout')

    def test_registration_url_resolves(self):
        """Проверка, что URL для регистрации соответствует правильному представлению."""
        self.assertEqual(resolve(self.registration_url).url_name, 'registration')

    def test_login_valid_user(self):
        """Тест входа с правильными учетными данными."""
        response = self.client.post(self.login_url, self.user_credentials)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_invalid_user(self):
        """Тест входа с неправильными учетными данными."""
        response = self.client.post(self.login_url, {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_authenticated_user(self):
        """Тест выхода для авторизованного пользователя."""
        self.client.login(**self.user_credentials)
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_page_renders_correctly(self):
        """Проверка, что страница входа отображается корректно."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Имя пользователя")
        self.assertContains(response, "Пароль")

class RegistrationTests(TestCase):

    def setUp(self):
        self.registration_url = reverse('registration')

    def test_registration_password_mismatch(self):
        """Тест неудачной регистрации из-за несовпадения паролей."""
        invalid_data = {
            'username': 'newuser',
            'password1': 'securepassword123',
            'password2': 'differentpassword123'
        }
        response = self.client.post(self.registration_url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_registration_duplicate_username(self):
        """Тест неудачной регистрации из-за уже существующего имени пользователя."""
        User.objects.create_user(username='existinguser', password='password123')
        duplicate_data = {
            'username': 'existinguser',
            'password1': 'securepassword123',
            'password2': 'securepassword123'
        }
        response = self.client.post(self.registration_url, duplicate_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Пользователь с таким именем уже существует.")

    def test_registration_missing_username(self):
        """Тест неудачной регистрации из-за отсутствия имени пользователя."""
        invalid_data = {
            'username': '',
            'password1': 'securepassword123',
            'password2': 'securepassword123'
        }
        response = self.client.post(self.registration_url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='').exists())

    def test_registration_missing_password(self):
        """Тест неудачной регистрации из-за отсутствия пароля."""
        invalid_data = {
            'username': 'newuser',
            'password1': '',
            'password2': ''
        }
        response = self.client.post(self.registration_url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_registration_page_renders_correctly(self):
        """Проверка, что страница регистрации отображается корректно."""
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Имя пользователя")
        self.assertContains(response, "Электронная почта")
        self.assertContains(response, "Пароль")
        self.assertContains(response, "Подтвердите пароль")
