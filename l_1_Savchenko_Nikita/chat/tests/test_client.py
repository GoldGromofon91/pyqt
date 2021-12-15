import subprocess
import unittest
import time

from function import get_template_message, check_message_on_server, create_ip_port, check_message_on_client
import CONFIGS


class TestClientSide(unittest.TestCase):
    def test_check_true_template(self):
        message = get_template_message(role='Guest')
        self.assertEqual(message, {
        CONFIGS.CONFIG_PROJECT['DEFAULT_CONF'].get('ACTION'): CONFIGS.CONFIG_PROJECT['DEFAULT_CONF'].get('PRESENCE'),
        CONFIGS.CONFIG_PROJECT['DEFAULT_CONF'].get('TIME'): round(time.time(),2),
        CONFIGS.CONFIG_PROJECT['DEFAULT_CONF'].get('USER'): "Guest"
    })

    def test_check_200(self):
        response = {CONFIGS.CONFIG_PROJECT['DEFAULT_CONF'].get('RESPONSE'): CONFIGS.CONFIG_PROJECT['STATUS'].get(
                             'OK')}
        self.assertEqual(check_message_on_client(response), {'status': 'Connected', '200': 'OK'})

    def test_check_400(self):
        response = {CONFIGS.CONFIG_PROJECT['DEFAULT_CONF'].get('RESPONSE'): CONFIGS.CONFIG_PROJECT['STATUS'].get(
                             'BAD_REQUEST')}
        self.assertEqual(check_message_on_client(response), {'400': 'error', 'status': 'Canceled'}
)