import unittest
from unittest.mock import MagicMock, patch
from src.Ingredients.models.provider_model import Provider

class TestProviderModel(unittest.TestCase):
    def setUp(self):
        self.provider = Provider("test_provider", "test_address", "test_email", "test_phone")
        self.provider.create(self.provider.get_session())

    def tearDown(self):
        self.provider.delete(self.provider.get_session())

    def test_create(self):
        session = self.provider.get_session()
        provider = self.provider.read(session)
        self.assertIsNotNone(provider)
        self.assertEqual(provider.nombre_proveedor, "test_provider")
        self.assertEqual(provider.direccion, "test_address")
        self.assertEqual(provider.email, "test_email")
        self.assertEqual(provider.telefono, "test_phone")
        session.close()

    def test_read(self):
        session = self.provider.get_session()
        provider = self.provider.read(session)
        self.assertIsNotNone(provider)
        self.assertEqual(provider.nombre_proveedor, "test_provider")
        self.assertEqual(provider.direccion, "test_address")
        self.assertEqual(provider.email, "test_email")
        self.assertEqual(provider.telefono, "test_phone")
        session.close()

    def test_update(self):
        session = self.provider.get_session()
        self.provider.update(session, nombre_proveedor="updated_provider", direccion="updated_address", email="updated_email", telefono="updated_phone")
        provider = self.provider.read(session)
        self.assertIsNotNone(provider)
        self.assertEqual(provider.nombre_proveedor, "updated_provider")
        self.assertEqual(provider.direccion, "updated_address")
        self.assertEqual(provider.email, "updated_email")
        self.assertEqual(provider.telefono, "updated_phone")
        session.close()

    def test_delete(self):
        session = self.provider.get_session()
        self.provider.delete(session)
        provider = self.provider.read(session)
        self.assertIsNone(provider)
        session.close()