import unittest
from unittest.mock import MagicMock
from src.Providers.controller import ProveedorController
from src.Providers.model import Proveedor

class TestProveedorController(unittest.TestCase):

    def setUp(self):
        self.session = MagicMock()

    def test_create_proveedor(self):
        # Arrange
        name = "Test Provider"
        category = "Test Category"

        # Act
        new_provider = ProveedorController.create_proveedor(self.session, name, category)

        # Assert
        self.assertIsInstance(new_provider, Proveedor)
        self.assertEqual(new_provider.nombre, name)
        self.assertEqual(new_provider.categoria, category)
        self.session.add.assert_called_once_with(new_provider)
        self.session.commit.assert_called_once()

    def test_get_provider_by_name(self):
        # Arrange
        name = "Test Provider"
        mock_provider = MagicMock(spec=Proveedor, nombre=name)
        self.session.query.return_value.filter.return_value.first.return_value = mock_provider

        # Act
        provider = ProveedorController.get_provider_by_name(self.session, name)

        # Assert
        self.assertEqual(provider.nombre, name)
        self.session.query.assert_called_once()
        self.session.query.return_value.filter.assert_called_once()
        self.session.query.return_value.filter.return_value.first.assert_called_once()

    def test_get_provider_by_id(self):
        # Arrange
        provider_id = 1
        mock_provider = MagicMock(spec=Proveedor, id_proveedor=provider_id)
        self.session.query.return_value.filter.return_value.first.return_value = mock_provider

        # Act
        provider = ProveedorController.get_provider_by_id(self.session, provider_id)

        # Assert
        self.assertEqual(provider.id_proveedor, provider_id)
        self.session.query.assert_called_once()
        self.session.query.return_value.filter.assert_called_once()
        self.session.query.return_value.filter.return_value.first.assert_called_once()

    def test_update_proveedor(self):
        # Arrange
        provider_id = 1
        initial_name = "Old Name"
        initial_category = "Old Category"
        new_name = "New Name"
        new_category = "New Category"

        mock_provider = MagicMock(spec=Proveedor, id_proveedor=provider_id, nombre=initial_name, categoria=initial_category)
        self.session.query.return_value.filter.return_value.first.return_value = mock_provider

        # Act
        updated_provider = ProveedorController.update_proveedor(self.session, provider_id, new_name, new_category)

        # Assert
        self.assertEqual(updated_provider.nombre, new_name)
        self.assertEqual(updated_provider.categoria, new_category)

    def test_delete_proveedor(self):
        # Arrange
        provider_id = 1
        mock_provider = MagicMock(spec=Proveedor, id_proveedor=provider_id)
        self.session.query.return_value.filter.return_value.first.return_value = mock_provider

        # Act
        result = ProveedorController.delete_proveedor(self.session, provider_id)

        # Assert
        self.assertTrue(result)

    def test_get_all_providers(self):
        # Arrange
        mock_providers = [
            MagicMock(spec=Proveedor, nombre="Provider 1"),
            MagicMock(spec=Proveedor, nombre="Provider 2")
        ]
        self.session.query.return_value.all.return_value = mock_providers

        # Act
        providers = ProveedorController.get_all_providers(self.session)

        # Assert
        self.assertEqual(len(providers), len(mock_providers))
        self.session.query.assert_called_once()
        self.session.query.return_value.all.assert_called_once()

    def test_get_providers_by_name(self):
        # Arrange
        name = "Test"
        mock_providers = [
            MagicMock(spec=Proveedor, nombre="Test Provider 1"),
            MagicMock(spec=Proveedor, nombre="Test Provider 2")
        ]
        self.session.query.return_value.filter.return_value.all.return_value = mock_providers

        # Act
        providers = ProveedorController.get_providers_by_name(self.session, name)

        # Assert
        self.assertEqual(len(providers), len(mock_providers))
        self.session.query.assert_called_once()
        self.session.query.return_value.filter.assert_called_once()
        self.session.query.return_value.filter.return_value.all.assert_called_once()

    def test_get_providers_by_name_empty(self):
        # Arrange
        name = "Nonexistent Provider"
        self.session.query.return_value.filter.return_value.all.return_value = []

        # Act
        providers = ProveedorController.get_providers_by_name(self.session, name)

        # Assert
        self.assertEqual(len(providers), 0)
        self.session.query.assert_called_once()
        self.session.query.return_value.filter.assert_called_once()
        self.session.query.return_value.filter.return_value.all.assert_called_once()

    

    def test_get_providers_by_category(self):
        # Arrange
        category = "Category"
        mock_providers = [
            MagicMock(spec=Proveedor, categoria="Category 1"),
            MagicMock(spec=Proveedor, categoria="Category 2")
        ]
        self.session.query.return_value.filter.return_value.all.return_value = mock_providers

        # Act
        providers = ProveedorController.get_providers_by_category(self.session, category)

        # Assert
        self.assertEqual(len(providers), len(mock_providers))
        self.session.query.assert_called_once()
        self.session.query.return_value.filter.assert_called_once()
        self.session.query.return_value.filter.return_value.all.assert_called_once()

    def test_get_providers_by_category_empty(self):
        # Arrange
        category = "Nonexistent Category"
        self.session.query.return_value.filter.return_value.all.return_value = []

        # Act
        providers = ProveedorController.get_providers_by_category(self.session, category)

        # Assert
        self.assertEqual(len(providers), 0)
        self.session.query.assert_called_once()
        self.session.query.return_value.filter.assert_called_once()
        self.session.query.return_value.filter.return_value.all.assert_called_once()

    def test_create_proveedor_invalid(self):
        # Arrange
        name = None
        category = "Test Category"

        # Act & Assert
        with self.assertRaises(ValueError):
            ProveedorController.create_proveedor(self.session, name, category)
    

if __name__ == '__main__':
    unittest.main()