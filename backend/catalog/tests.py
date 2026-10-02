from django.test import TestCase

from .models import MasterCategory


class MasterCategoryModelTests(TestCase):
    def test_master_category_creation(self):
        category = MasterCategory.objects.create(
            name="Groceries",
            slug="groceries",
            description="Platform-wide grocery category",
        )

        self.assertEqual(str(category), "Groceries")
        self.assertTrue(category.is_active)
        self.assertEqual(category.slug, "groceries")
