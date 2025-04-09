import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify
from datetime import datetime
from core.blacklist_service import BlacklistService
from core.models import Blacklist
from extensions.database import db


class BlacklistServiceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        cls.app.secret_key = 'test_secret'
        with cls.app.app_context():
            db.init_app(cls.app)
            db.create_all()

    @patch('core.blacklist_service.BlacklistService.query.filter_by')
    @patch('extensions.database.db.session.add')
    @patch('extensions.database.db.session.commit')
    @patch('extensions.database.db.session.rollback')
    def test_add_to_blacklist_success(self, mock_rollback, mock_commit, mock_add, mock_filter_by):
        mock_filter_by.return_value.first.return_value = None
        email = "test@example.com"
        app_uuid = "app-uuid-123"
        blocked_reason = "Spam"
        ip_address = "192.168.0.1"
        
        with self.app.app_context():  
            response = BlacklistService.add_to_blacklist(email, app_uuid, blocked_reason, ip_address)
        
        self.assertEqual(response[1], 201)
        self.assertIn("El email ha sido agregado a la lista negra", response[0].get_data(as_text=True))
        mock_add.assert_called_once()
        self.assertEqual(mock_add.call_args[0][0].email, email)

    @patch('core.blacklist_service.BlacklistService.query.filter_by')
    def test_check_blacklist_email_in_list(self, mock_filter_by):
        mock_blacklist_entry = MagicMock()
        mock_blacklist_entry.blocked_reason = "Spam"
        mock_filter_by.return_value.first.return_value = mock_blacklist_entry
        email = "test@example.com"
        
        with self.app.app_context():  # Aseguramos que el contexto de la aplicación esté disponible
            response = BlacklistService.check_blacklist(email)
        
        self.assertEqual(response[1], 200)
        self.assertIn("is_blacklisted", response[0].get_data(as_text=True))
        self.assertTrue("is_blacklisted" in response[0].get_json())
        self.assertTrue(response[0].get_json()["is_blacklisted"])

    @patch('core.blacklist_service.BlacklistService.query.filter_by')
    def test_check_blacklist_email_not_in_list(self, mock_filter_by):
        mock_filter_by.return_value.first.return_value = None
        email = "test@example.com"
        
        with self.app.app_context():
            response = BlacklistService.check_blacklist(email)
        
        self.assertEqual(response[1], 200)
        self.assertIn("is_blacklisted", response[0].get_data(as_text=True))
        self.assertFalse(response[0].get_json()["is_blacklisted"])

if __name__ == '__main__':
    unittest.main()
