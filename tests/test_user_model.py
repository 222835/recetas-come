import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add the project root to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Users.model import Usuario, Base
from src.security.password_utils import Security
class TestUsuarioModel(unittest.TestCase):
    def setUp(self):
        """Setup: Create an in-memory SQLite database and session for testing."""
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def tearDown(self):
        """Teardown: Close the session and drop all tables after each test."""
        self.session.close()
        Base.metadata.drop_all(self.engine)

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
        self.assertEqual(new_user.contrasenia, Security.generate_password(hashed_password))
        self.assertEqual(new_user.rol, "user")

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
        self.assertEqual(retrieved_user.contrasenia, Security.generate_password(hashed_password))
        self.assertEqual(retrieved_user.rol, "user")

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
        self.assertEqual(retrieved_user.nombre_usuario, "testuser")
        self.assertEqual(retrieved_user.contrasenia, Security.generate_password(hashed_password))
        self.assertEqual(retrieved_user.rol, "user")

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
        new_user.contrasenia = new_hashed_password
        new_user.rol = "admin"
        self.session.commit()

        # Read the updated user from the database
        updated_user = self.session.query(Usuario).filter_by(numero_usuario=new_user.numero_usuario).first()

        # Assert that the user's information was updated correctly
        self.assertEqual(updated_user.nombre_completo, "New Test User")
        self.assertEqual(updated_user.nombre_usuario, "newtestuser")
        self.assertEqual(updated_user.contrasenia, new_hashed_password)
        self.assertEqual(updated_user.rol, "admin")

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

if __name__ == '__main__':
    unittest.main()