import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add the project root to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Users.Login.controller import LoginController
from src.Users.model import Usuario
from src.security.password_utils import Security  # Import Security class

class TestLoginController(unittest.TestCase):

    def setUp(self):
        """Setup: Create an in-memory SQLite database and session for testing."""
        self.engine = create_engine('sqlite:///:memory:')
        from src.Users.model import Base  # Import Base here to avoid circular imports
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def tearDown(self):
        """Teardown: Close the session and drop all tables after each test."""
        self.session.close()
        from src.Users.model import Base
        Base.metadata.drop_all(self.engine)

    @patch('src.Users.Login.controller.Usuario')
    def test_login_success(self, MockUsuario):
        """Test successful login."""
        # Mock the Usuario object and its methods
        mock_user = MagicMock()
        mock_user.read_by_username.return_value = mock_user
        # mock_user.generate_password.return_value = "hashed_password"  # No longer needed
        mock_user.contrasenia = "hashed_password"

        # Configure the MockUsuario to return the mock_user
        MockUsuario.return_value = mock_user

        # Create a mock session
        mock_session = MagicMock()
        mock_user.get_session.return_value = mock_session

        # Prepare user data
        user_data = {"nombre_usuario": "testuser", "contrasenia": "password"}

        # Call the login method
        with patch('src.security.password_utils.Security.generate_password', return_value="hashed_password"):
            result = LoginController.login(self, user_data)

        # Assert that the login was successful
        self.assertTrue(result)
        mock_user.read_by_username.assert_called_once_with(mock_session, "testuser")
        # mock_user.generate_password.assert_called_once_with("password")  # No longer needed
        mock_session.close.assert_called_once()

    @patch('src.Users.Login.controller.Usuario')
    def test_login_user_not_found(self, MockUsuario):
        """Test login when the user is not found."""
        # Mock the Usuario object and its methods
        mock_user = MagicMock()
        mock_user.read_by_username.return_value = None

        # Configure the MockUsuario to return the mock_user
        MockUsuario.return_value = mock_user

        # Create a mock session
        mock_session = MagicMock()
        mock_user.get_session.return_value = mock_session

        # Prepare user data
        user_data = {"nombre_usuario": "testuser", "contrasenia": "password"}

        # Call the login method
        result = LoginController.login(self, user_data)

        # Assert that the login failed because the user was not found
        self.assertFalse(result)
        mock_user.read_by_username.assert_called_once_with(mock_session, "testuser")
        mock_session.close.assert_called_once()

    @patch('src.Users.Login.controller.Usuario')
    def test_login_incorrect_password(self, MockUsuario):
        """Test login with an incorrect password."""
        # Mock the Usuario object and its methods
        mock_user = MagicMock()
        mock_user.read_by_username.return_value = mock_user
        # mock_user.generate_password.return_value = "incorrect_password"  # No longer needed
        mock_user.contrasenia = "hashed_password"

        # Configure the MockUsuario to return the mock_user
        MockUsuario.return_value = mock_user

        # Create a mock session
        mock_session = MagicMock()
        mock_user.get_session.return_value = mock_session

        # Prepare user data
        user_data = {"nombre_usuario": "testuser", "contrasenia": "password"}

        # Call the login method
        with patch('src.security.password_utils.Security.generate_password', return_value="incorrect_password"):
            result = LoginController.login(self, user_data)

        # Assert that the login failed because the password was incorrect
        self.assertFalse(result)
        mock_user.read_by_username.assert_called_once_with(mock_session, "testuser")
        # mock_user.generate_password.assert_called_once_with("password")  # No longer needed
        mock_session.close.assert_called_once()