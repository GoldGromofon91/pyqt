import subprocess
import unittest
import time

from function import get_template_message, check_message_on_server, create_ip_port
import CONFIGS


class TestServerSide(unittest.TestCase):
    def setUp(self):
        self.true_message = get_template_message(role='Guest')
        self.false_message = {
            "action": "presence",
            "time": time.time(),
            "user": 'Smth'
        }

    def test_check_response_true_message(self):
        self.assertEqual(check_message_on_server(self.true_message),
                         {CONFIGS.CONFIG_PROJECT['DEFAULT_CONF'].get('RESPONSE'): CONFIGS.CONFIG_PROJECT['STATUS'].get(
                             'OK')})

    def test_check_response_false_message(self):
        self.assertEqual(check_message_on_server(self.false_message),
                         {CONFIGS.CONFIG_PROJECT['DEFAULT_CONF'].get('RESPONSE'): CONFIGS.CONFIG_PROJECT['STATUS'].get(
                             'BAD_REQUEST')})
