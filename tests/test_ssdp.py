import unittest
from upnp import *

class ssdp_test(unittest.TestCase):
    def setUp(self):
        self.device = Device({

        })
        self.upnp = Annoncer(self.device)

    def test_ssdp_creation(self):
        self.assertIsNotNone(self.upnp)

    def test_ssdp_device(self):
        self.assertEqual(self.device, self.upnp.device)


if __name__ == '__main__':
    unittest.main()
