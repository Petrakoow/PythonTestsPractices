from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from recipe_catalog.models import Unit
from django.contrib.messages import get_messages


class UnitTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_add_unit(self):
        url = reverse('add-unit')
        data = {
            'name': 'Cup',
            'conversion_to_grams': 250.0
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Unit.objects.count(), 1) 
        unit = Unit.objects.first()
        self.assertEqual(unit.name, 'Cup')
        self.assertEqual(unit.conversion_to_grams, 250.0)
        self.assertEqual(unit.author, self.user)

    def test_add_unit_duplicate_name(self):
        Unit.objects.create(name='Cup', conversion_to_grams=250.0, author=self.user)
        url = reverse('add-unit')
        data = {
            'name': 'Cup',  
            'conversion_to_grams': 300.0
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200) 
        self.assertFormError(response, 'form', 'name', 'Единица измерения с таким названием уже существует.')

    def test_edit_unit(self):
        unit = Unit.objects.create(name='Cup', conversion_to_grams=250.0, author=self.user)
        url = reverse('edit-unit', kwargs={'pk': unit.pk})
        data = {
            'name': 'Mug',
            'conversion_to_grams': 300.0
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302) 
        unit.refresh_from_db()
        self.assertEqual(unit.name, 'Mug')
        self.assertEqual(unit.conversion_to_grams, 300.0)

    def test_delete_unit(self):
        unit = Unit.objects.create(name='Cup', conversion_to_grams=250.0, author=self.user)
        url = reverse('delete-unit', kwargs={'pk': unit.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(Unit.objects.count(), 0) 

    def test_manage_units_no_units(self):
        url = reverse('manage-units')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Единицы измерения отсутствуют.")

    def test_manage_units_not_logged_in(self):
        self.client.logout()
        url = reverse('manage-units')
        response = self.client.get(url)
        self.assertRedirects(response, '/login/?next=/manage-units/')
