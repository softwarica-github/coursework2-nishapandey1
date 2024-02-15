
import unittest
import socket

from firewall import start_firewall, stop_firewall, add_rule, allowed_connections, denied_ports

class TestFirewall(unittest.TestCase):
    def test_start_stop_firewall(self):
        # Test starting and stopping the firewall
        start_firewall()
        self.assertTrue(is_firewall_running())
        stop_firewall()
        self.assertFalse(is_firewall_running())

    def test_add_rule(self):
        # Test adding a rule to the allowed connections list
        add_rule('192.168.56.107', 80)
        self.assertIn({'ip': '192.168.56.107', 'port': 80}, allowed_connections)

    def test_handle_connection(self):
        # Test handling a connection
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_address = ('127.0.0.1', 1234)
        connection.connect(client_address)
        handle_connection(connection, client_address)
        connection.close()

        # Test that the connection was allowed or denied based on the rules
        if client_address[1] in denied_ports:
            self.assertFalse(connection.fileno() in [x.fileno() for x in threading.enumerate() if x.name == 'Thread-1'])
        else:
            self.assertTrue(connection.fileno() in [x.fileno() for x in threading.enumerate() if x.name == 'Thread-1'])

def is_firewall_running():
    # Return True if the firewall is running, False otherwise
    global running
    return running

if __name__ == '__main__':
    unittest.main()

