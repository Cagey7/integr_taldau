from django.test import TestCase
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from .models import Index, Chapter


class DjangoConfigTest(TestCase):
    def test_secret_key_strength(self):
        try:
            validate_password(settings.SECRET_KEY)
        except Exception as e:
            msg = f"Weak secret key {e.messages}"
            self.fail(msg)


class ChapterModelTest(TestCase):
    def setUp(self):
        chapter = Chapter.objects.create(id=700894, name="Статистика национальных счетов", parent=None)
        Chapter.objects.create(id=700895, name="Текущие счета", parent=chapter)

    def test_data(self):
        chapter1 = Chapter.objects.get(name="Статистика национальных счетов")
        chapter2 = Chapter.objects.get(name="Текущие счета")
        test_chapter1 = chapter2.parent
        self.assertEqual(chapter1.id, 700894)
        self.assertEqual(chapter1, test_chapter1)


class IndexModelTest(TestCase):
    def setUp(self):
        chapter = Chapter.objects.create(id=700896, name="Счет товаров и услуг", parent_id=None)
        Index.objects.create(id=700897, name="Валовой выпуск в счете товаров и услуг", chapter=chapter)
        
    def test_data(self):
        index = Index.objects.get(id=700897)
        self.assertEqual(index.name, "Валовой выпуск в счете товаров и услуг")
