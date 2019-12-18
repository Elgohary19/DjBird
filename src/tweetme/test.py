from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from .models import Update


User = get_user_model()


class UpdateModelTestCase(TestCase):
    def setUp(self):
        random_user = User.objects.create(username='Reema33333')

    def test_update_item(self):
        obj = Update.objects.create(
                user=User.objects.first(),
                content='Some random content'
                )
        self.assertTrue(obj.content == "Some random content")
        self.assertTrue(obj.id == 1)
        absolute_url = reverse('detail', kwargs={"pk": 1})
        self.assertEqual(obj.get_absolute_url(), absolute_url)

    def test_update_url(self):
        obj = Update.objects.create(
            user=User.objects.first(),
            content='Some random content'
        )
        absolute_url = reverse('detail', kwargs={"pk": obj.pk})
        self.assertEqual(obj.get_absolute_url(), absolute_url)
