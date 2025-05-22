import unittest
from unittest.mock import MagicMock
from src.Costs.controller import CostController
from src.Costs.model import Costos
from sqlalchemy.orm import Session

## Class TestCostController
## This class contains unit tests for the CostController class.
class TestCostController(unittest.TestCase):
    ## This method sets up the test environment before each test case.
    def setUp(self):
        self.session = MagicMock(spec=Session)
    ## This method tears down the test environment after each test case.
    def test_create_cost(self):
        # Arrange
        name = "Test Cost"
        price = 100
        provider_id = 1

        # Act
        new_cost = CostController.create_cost(self.session, name, price, provider_id)


        # Assert
        self.assertIsInstance(new_cost, Costos)
        self.assertEqual(new_cost.nombre, name)
        self.assertEqual(new_cost.precio, price)
        self.assertEqual(new_cost.id_proveedor, provider_id)
        self.session.add.assert_called_once_with(new_cost)
        self.session.commit.assert_called_once()

    ## Test for get_cost_by_name
    def test_get_cost_by_name(self):
        # Arrange
        name = "Test Cost"
        mock_cost = MagicMock(spec=Costos, nombre=name)
        self.session.query.return_value.filter.return_value.first.return_value = mock_cost

        # Act
        cost = CostController.get_cost_by_name(self.session, name)

        # Assert
        self.assertEqual(cost.nombre, name)
        self.session.query.assert_called_once()
        self.session.query.return_value.filter.assert_called_once()
        self.session.query.return_value.filter.return_value.first.assert_called_once()

    ## Test for get_cost_by_id
    def test_get_cost_by_id(self):
        # Arrange
        cost_id = 1
        mock_cost = MagicMock(spec=Costos, id_costo=cost_id)
        self.session.query.return_value.filter.return_value.first.return_value = mock_cost

        # Act
        cost = CostController.get_cost_by_id(self.session, cost_id)

        # Assert
        self.assertEqual(cost.id_costo, cost_id)
        self.session.query.assert_called_once()
        self.session.query.return_value.filter.assert_called_once()
        self.session.query.return_value.filter.return_value.first.assert_called_once()

    ## Test for update_cost
    def test_update_cost(self):
        # Arrange
        cost_id = 1
        initial_name = "Old Name"
        initial_price = 50
        new_name = "New Name"
        new_price = 100

        mock_cost = MagicMock(spec=Costos, id_costo=cost_id, nombre=initial_name, precio=initial_price)
        self.session.query.return_value.filter.return_value.first.return_value = mock_cost

        # Act
        updated_cost = CostController.update_cost(self.session, cost_id, new_name, new_price)

        # Assert
        self.assertEqual(updated_cost.nombre, new_name)
        self.assertEqual(updated_cost.precio, new_price)

    ## Test for delete_cost
    def test_delete_cost(self):
        # Arrange
        cost_id = 1
        mock_cost = MagicMock(spec=Costos, id_costo=cost_id)
        self.session.query.return_value.filter.return_value.first.return_value = mock_cost

        # Act
        result = CostController.delete_cost(self.session, cost_id)

        # Assert
        self.assertTrue(result)
        
    ## Test for create_costs
    def test_create_costs(self):
        # Arrange
        costs = [
            MagicMock(spec=Costos, nombre="Cost 1", precio=50, id_proveedor=1),
            MagicMock(spec=Costos, nombre="Cost 2", precio=75, id_proveedor=2)
        ]

        # Act
        CostController.create_costs(self.session, costs)

        # Assert
        self.session.add_all.assert_called_once_with(costs)
        self.session.commit.assert_called_once()
    ## Test for get_all_costs
    def test_get_all_costs(self):
        # Arrange
        mock_costs = [
            MagicMock(spec=Costos, nombre="Cost 1", precio=50, id_proveedor=1),
            MagicMock(spec=Costos, nombre="Cost 2", precio=75, id_proveedor=2)
        ]
        self.session.query.return_value.all.return_value = mock_costs

        # Act
        costs = CostController.get_all_costs(self.session)

        # Assert
        self.assertEqual(len(costs), len(mock_costs))
        self.session.query.assert_called_once()
        self.session.query.return_value.all.assert_called_once()
    ## Test for fetch_costs_by_provider
    def test_fetch_costs_by_provider(self):
        # Arrange
        provider_id = 1
        mock_costs = [
            MagicMock(spec=Costos, nombre="Cost 1", precio=50, id_proveedor=provider_id),
            MagicMock(spec=Costos, nombre="Cost 2", precio=75, id_proveedor=provider_id)
        ]
        self.session.query.return_value.filter.return_value.all.return_value = mock_costs

        # Act
        costs = CostController.fetch_costs_by_provider(self.session, provider_id)

        # Assert
        self.assertEqual(len(costs), len(mock_costs))
        self.session.query.assert_called_once()
        self.session.query.return_value.filter.assert_called_once()
        self.session.query.return_value.filter.return_value.all.assert_called_once()
    ## Test for fetch_costs_by_provider_empty
    def test_fetch_costs_by_provider_empty(self):
        # Arrange
        provider_id = 1
        self.session.query.return_value.filter.return_value.all.return_value = []

        # Act
        costs = CostController.fetch_costs_by_provider(self.session, provider_id)

        # Assert
        self.assertEqual(len(costs), 0)
        self.session.query.assert_called_once()
        self.session.query.return_value.filter.assert_called_once()
        self.session.query.return_value.filter.return_value.all.assert_called_once()
    ## Test for fetch_costs_by_name
    def test_fetch_costs_by_name(self):
        # Arrange
        name = "Test Cost"
        mock_costs = [
            MagicMock(spec=Costos, nombre=name, precio=50, id_proveedor=1),
            MagicMock(spec=Costos, nombre=name, precio=75, id_proveedor=2)
        ]
        self.session.query.return_value.filter.return_value.all.return_value = mock_costs

        # Act
        costs = CostController.fetch_costs_by_name(self.session, name)

        # Assert
        self.assertEqual(len(costs), len(mock_costs))
        self.session.query.assert_called_once()
        self.session.query.return_value.filter.assert_called_once()
        self.session.query.return_value.filter.return_value.all.assert_called_once()
    ## Test for search_costs
    def test_search_costs(self):
        # Arrange
        name = "Test"
        mock_costs = [
            MagicMock(spec=Costos, nombre="Test Cost 1", precio=50, id_proveedor=1),
            MagicMock(spec=Costos, nombre="Another Test Cost", precio=75, id_proveedor=2)
        ]
        self.session.query.return_value.filter.return_value.all.return_value = mock_costs

        # Act
        costs = CostController.search_costs(self.session, name)

        # Assert
        self.assertEqual(len(costs), len(mock_costs))
        self.session.query.assert_called_once()
        self.session.query.return_value.filter.assert_called_once()
        self.session.query.return_value.filter.return_value.all.assert_called_once()

if __name__ == '__main__':
    unittest.main()