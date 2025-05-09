import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Users.model import Usuario, Base
from src.security.password_utils import Security
from src.Users.auth_service import AuthService

## @brief Test class for the Usuario model, which includes unit tests for CRUD operations and authentication.
class TestUsuarioModel(unittest.TestCase):
    ## @brief Set up the test environment by creating an in-memory SQLite database and session.
    def setUp(self):
        """Setup: Create an in-memory SQLite database and session for testing."""
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    ## @brief Create the Usuario table in the in-memory database
    def tearDown(self):
        """Teardown: Close the session and drop all tables after each test."""
        self.session.close()
        Base.metadata.drop_all(self.engine)
        self.engine.dispose()

    ## @brief Test creating a new user.
    def test_create_usuario(self):
        """Test creating a new Usuario."""
        hashed_password = "password123"
        new_user = Usuario(nombre_completo="Test User", contrasenia=hashed_password, rol="user", nombre_usuario="testuser")
        self.session.add(new_user)
        self.session.commit()

        # Assert that the user was created and has an auto-incremented ID
        self.assertIsNotNone(new_user.numero_usuario)
        self.assertEqual(new_user.nombre_completo, "Test User")
        self.assertEqual(new_user.nombre_usuario, "testuser")
        self.assertTrue(Security.verify_password(hashed_password, new_user.contrasenia))
        self.assertEqual(new_user.rol, "user")

    ## @brief Test reading a user from the database.
    def test_read_usuario(self):
        """Test reading a Usuario from the database."""
        hashed_password = "password123"
        new_user = Usuario(nombre_completo="Test User", contrasenia=hashed_password, rol="user", nombre_usuario="testuser")
        self.session.add(new_user)
        self.session.commit()

        # Read the user from the database
        retrieved_user = self.session.query(Usuario).filter_by(nombre_usuario="testuser").first()

        # Assert that the retrieved user is the same as the created user
        self.assertEqual(retrieved_user.numero_usuario, new_user.numero_usuario)
        self.assertEqual(retrieved_user.nombre_completo, "Test User")
        self.assertEqual(retrieved_user.nombre_usuario, "testuser")
        self.assertEqual(retrieved_user.rol, "user")
        self.assertTrue(Security.verify_password(hashed_password, retrieved_user.contrasenia))

    ## @brief Test reading a user from the database by username.
    def test_read_usuario_by_username(self):
        """Test reading a Usuario from the database by username."""
        hashed_password = "password123"
        new_user = Usuario(nombre_completo="Test User", contrasenia=hashed_password, rol="user", nombre_usuario="testuser")
        self.session.add(new_user)
        self.session.commit()

        # Read the user from the database by username
        retrieved_user = self.session.query(Usuario).filter_by(nombre_usuario="testuser").first()

        # Assert that the retrieved user is the same as the created user
        self.assertEqual(retrieved_user.numero_usuario, new_user.numero_usuario)
        self.assertEqual(retrieved_user.nombre_completo, "Test User")
        self.assertTrue(Security.verify_password(hashed_password, retrieved_user.contrasenia))
        self.assertEqual(retrieved_user.contrasenia, Security.generate_password(hashed_password))
        self.assertEqual(retrieved_user.rol, "user")

    ## @brief Test updating a user in the database.
    def test_update_usuario(self):
        """Test updating a Usuario in the database."""
        hashed_password = "password123"
        new_user = Usuario(nombre_completo="Test User", contrasenia=hashed_password, rol="user", nombre_usuario="testuser")
        self.session.add(new_user)
        self.session.commit()

        # Update the user's information
        new_hashed_password = "new_password"
        new_user.nombre_completo = "New Test User"
        new_user.nombre_usuario = "newtestuser"
        new_user.update(self.session, contrasenia=new_hashed_password)
        new_user.rol = "admin"
        self.session.commit()

        # Read the updated user from the database
        updated_user = self.session.query(Usuario).filter_by(numero_usuario=new_user.numero_usuario).first()

        # Assert that the user's information was updated correctly
        self.assertEqual(updated_user.nombre_completo, "New Test User")
        self.assertEqual(updated_user.nombre_usuario, "newtestuser")
        self.assertTrue(Security.verify_password(new_hashed_password, updated_user.contrasenia))
        self.assertEqual(updated_user.rol, "admin")

    ## @brief Test deleting a user from the database.
    def test_delete_usuario(self):
        """Test deleting a Usuario from the database."""
        hashed_password = "password123"
        new_user = Usuario(nombre_completo="Test User", contrasenia=hashed_password, rol="user", nombre_usuario="testuser")
        self.session.add(new_user)
        self.session.commit()

        # Delete the user from the database
        self.session.delete(new_user)
        self.session.commit()

        # Assert that the user was deleted
        deleted_user = self.session.query(Usuario).filter_by(numero_usuario=new_user.numero_usuario).first()
        self.assertIsNone(deleted_user)

    ## @brief Test the authentication of a user.
    def test_authenticate(self):
        """Test the authentication of a user."""
        hashed_password = "password123"
        new_user = Usuario(nombre_completo="Test User", contrasenia=hashed_password, rol="user", nombre_usuario="testuser")
        self.session.add(new_user)
        self.session.commit()

        # Try to authenticate with the correct credentials
        authenticated_user = AuthService.authenticate(self.session, "testuser", hashed_password)

        # Assert that the authentication was successful and the correct user was returned
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.nombre_usuario, "testuser")
        self.assertTrue(Security.verify_password(hashed_password, authenticated_user.contrasenia))

        # Try to authenticate with the incorrect username
        authenticated_user_invalid_username = AuthService.authenticate(self.session, "invalidtestuser", hashed_password)

        # Assert that authentication failed with incorrect username
        self.assertIsNone(authenticated_user_invalid_username)

        # Try to authenticate with incorrect credentials
        authenticated_user_invalid_password = AuthService.authenticate(self.session, "testuser", "wrongpassword")

        # Assert that authentication failed with incorrect password
        self.assertIsNone(authenticated_user_invalid_password)

    ## @brief Tests that an admin can edit other users information.
    def test_edit_account_info_admin(self):
        """Tests that an admin can edit other users information."""
        new_user_admin = Usuario(nombre_completo="Nombre Admin", contrasenia="admin123", rol="admin", nombre_usuario="adminuser")
        new_user_invitado = Usuario(nombre_completo="Test User", contrasenia="password123", rol="invitado", nombre_usuario="testuser")
        self.session.add_all([new_user_admin, new_user_invitado])
        self.session.commit()

        # Admin modifies another users information
        new_hashed_password = "newpassword"
        Usuario.edit_account_info(new_user_admin, new_user_invitado, self.session, nombre_completo="Updated User", nombre_usuario="updateduser", contrasenia=new_hashed_password)

        updated_user = self.session.query(Usuario).filter_by(numero_usuario=new_user_invitado.numero_usuario).first()

        # Asserts that changes have been made
        self.assertEqual(updated_user.nombre_completo, "Updated User")
        self.assertEqual(updated_user.nombre_usuario, "updateduser")
        self.assertTrue(Security.verify_password(new_hashed_password, updated_user.contrasenia))

    ## @brief Tests that users can edit their own username and password.
    def test_edit_account_info_self(self):
        """Tests that users can edit their own username and password."""
        hashed_password = "password123"
        new_user = Usuario(nombre_completo="Test User", contrasenia=hashed_password, rol="invitado", nombre_usuario="testuser")
        self.session.add(new_user)
        self.session.commit()

        # User edits their own information
        new_hashed_password = "newpassword"
        Usuario.edit_account_info(new_user, new_user, self.session, nombre_usuario="newusername", contrasenia=new_hashed_password)

        updated_user = self.session.query(Usuario).filter_by(numero_usuario=new_user.numero_usuario).first()

        # Asserts that changes have been made
        self.assertEqual(updated_user.nombre_usuario, "newusername")
        self.assertTrue(Security.verify_password(new_hashed_password, updated_user.contrasenia))

    ## @brief Tests that a guest user cannot edit another users info.
    def test_edit_account_info_no_permission(self):
        """Tests that a guest user cannot edit another users info."""
        new_user1 = Usuario(nombre_completo="User1", contrasenia="password123", rol="invitado", nombre_usuario="user1")
        new_user2 = Usuario(nombre_completo="User2", contrasenia="password123", rol="invitado", nombre_usuario="user2")
        self.session.add_all([new_user1, new_user2])
        self.session.commit()

        # User1 tries to modify User2 information, asserts it raises an error
        with self.assertRaises(PermissionError): Usuario.edit_account_info(new_user1, new_user2, self.session, nombre_usuario="newusername")

    ## @brief Tests that an admin can delete a user account.
    def test_delete_account_admin(self):
        """Tests that an admin can delete a user account."""
        new_user_admin = Usuario(nombre_completo="Nombre Admin", contrasenia="admin123", rol="admin", nombre_usuario="adminuser")
        new_user_invitado = Usuario(nombre_completo="Test User", contrasenia="password123", rol="invitado", nombre_usuario="testuser")
        self.session.add_all([new_user_admin, new_user_invitado])
        self.session.commit()

        # Admin deletes guest user
        Usuario.delete_account(new_user_admin, new_user_invitado, self.session)
        deleted_user = self.session.query(Usuario).filter_by(numero_usuario=new_user_invitado.numero_usuario).first()

        # Asserts if user was deleted
        self.assertIsNone(deleted_user)

    ## @brief Tests that a guest user cant delete another user and admin cant delete its own account.
    def test_delete_account_no_permission(self):
        """Tests that a guest user cant delete another user and admin cant delete its own account."""
        new_user_admin = Usuario(nombre_completo="Nombre Admin", contrasenia="admin123", rol="admin", nombre_usuario="adminuser")
        new_user1 = Usuario(nombre_completo="User1", contrasenia="password123", rol="invitado", nombre_usuario="user1")
        new_user2 = Usuario(nombre_completo="User2", contrasenia="password123", rol="invitado", nombre_usuario="user2")
        self.session.add_all([new_user_admin, new_user1, new_user2])
        self.session.commit()

        # Admin tries to delete own account, asserts it raises an error
        with self.assertRaises(PermissionError):
            Usuario.delete_account(new_user_admin, new_user_admin, self.session)

        # User1 tries to delete User2, asserts it raises an error
        with self.assertRaises(PermissionError):
            Usuario.delete_account(new_user1, new_user2, self.session)

    ## @brief Test the authentication of a user with an empty password.
    def test_edit_account_info_existing_username(self):
        """Tests that a guest user cannot update to an existing username."""
        new_user1 = Usuario(nombre_completo="User1", contrasenia="password123", rol="invitado", nombre_usuario="user1")
        new_user2 = Usuario(nombre_completo="User2", contrasenia="password123", rol="invitado", nombre_usuario="user2")
        self.session.add_all([new_user1, new_user2])
        self.session.commit()

        # User1 intenta cambiar su nombre de usuario a "User2", que ya existe
        with self.assertRaises(ValueError):
            Usuario.edit_account_info(new_user1, new_user1, self.session, nombre_usuario="user2")

if __name__ == '__main__':
    unittest.main()
