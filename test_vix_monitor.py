import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import os
import json

import vix_monitor

class TestVixMonitor(unittest.TestCase):
    def test_calculate_buy_amount(self):
        self.assertEqual(vix_monitor.calculate_buy_amount(24), 0)
        self.assertEqual(vix_monitor.calculate_buy_amount(25), 0.5)
        self.assertEqual(vix_monitor.calculate_buy_amount(30), 1.0)
        self.assertEqual(vix_monitor.calculate_buy_amount(40), 2.0)
        self.assertEqual(vix_monitor.calculate_buy_amount(50), 3.0)

    @patch('vix_monitor.yf.Ticker')
    def test_get_vix(self, mock_ticker):
        mock_instance = MagicMock()
        mock_instance.history.return_value = MagicMock(empty=False, __getitem__=lambda s, k: MagicMock(iloc=[None, 20.5]))
        mock_ticker.return_value = mock_instance
        self.assertEqual(vix_monitor.get_vix(), 20.5)

    def test_is_cooldown_active(self):
        # Save a purchase date 10 days ago
        test_date = datetime.now() - timedelta(days=10)
        with open(vix_monitor.LAST_PURCHASE_FILE, 'w') as f:
            json.dump({'date': test_date.isoformat()}, f)
        self.assertTrue(vix_monitor.is_cooldown_active())
        # Save a purchase date 40 days ago
        test_date = datetime.now() - timedelta(days=40)
        with open(vix_monitor.LAST_PURCHASE_FILE, 'w') as f:
            json.dump({'date': test_date.isoformat()}, f)
        self.assertFalse(vix_monitor.is_cooldown_active())
        # Remove file
        if os.path.exists(vix_monitor.LAST_PURCHASE_FILE):
            os.remove(vix_monitor.LAST_PURCHASE_FILE)

    def test_get_last_purchase_date_and_save(self):
        vix_monitor.save_purchase_date()
        date = vix_monitor.get_last_purchase_date()
        self.assertIsInstance(date, datetime)
        if os.path.exists(vix_monitor.LAST_PURCHASE_FILE):
            os.remove(vix_monitor.LAST_PURCHASE_FILE)

    @patch('vix_monitor.smtplib.SMTP')
    def test_send_email_notification(self, mock_smtp):
        # Setup environment variables
        os.environ['EMAIL_SENDER'] = 'test@example.com'
        os.environ['EMAIL_PASSWORD'] = 'testpassword'
        os.environ['EMAIL_RECEIVER'] = 'receiver@example.com'
        # Mock SMTP instance
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        # Should succeed
        result = vix_monitor.send_email_notification(30.0, 1.0)
        self.assertTrue(result)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with('test@example.com', 'testpassword')
        mock_server.send_message.assert_called_once()
        mock_server.quit.assert_called_once()
        # Remove environment variables
        del os.environ['EMAIL_SENDER']
        del os.environ['EMAIL_PASSWORD']
        del os.environ['EMAIL_RECEIVER']

if __name__ == '__main__':
    unittest.main()
