"""Offline boot-race regression; no ROS graph or network changes."""
import tempfile
import unittest
from pathlib import Path
from wait_m1_battery_network import active_addresses, wait_ready


def interface(address='192.0.2.104', state='UP'):
    return [dict(operstate=state, flags=['UP'],
                 addr_info=[dict(family='inet', local=address)])]


class BatteryNetworkTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.profile = Path(self.temp.name)/'dds.xml'
        self.profile.write_text('''<profiles xmlns="http://www.eprosima.com/XMLSchemas/fastRTPS_Profiles">
<transport_descriptors><transport_descriptor><type>UDPv4</type><interfaceWhiteList>
<address>192.0.2.104</address></interfaceWhiteList></transport_descriptor></transport_descriptors></profiles>''')
        self.clock = 0.

    def wait(self, read):
        def sleep(dt):
            self.clock += dt
        return wait_ready(self.profile, 3., read=read, clock=lambda: self.clock,
                          sleep=sleep, log=lambda *a, **kw: None)

    def test_ready_address_starts_immediately(self):
        self.assertTrue(self.wait(interface))
        self.assertEqual(self.clock, 0.)

    def test_boot_without_wifi_waits_until_correct_address(self):
        self.assertTrue(self.wait(lambda: [] if self.clock < 2 else interface()))
        self.assertEqual(self.clock, 2.)

    def test_other_address_does_not_open_transport(self):
        self.assertFalse(self.wait(lambda: interface('192.0.2.1')))
        self.assertEqual(self.clock, 3.)

    def test_address_on_disconnected_interface_is_not_ready(self):
        self.assertEqual(active_addresses(interface(state='DOWN')), set())

    def test_missing_profile_retries_instead_of_unrestricted_fallback(self):
        self.profile.unlink()
        self.assertFalse(self.wait(interface))

    def test_empty_whitelist_does_not_start(self):
        self.profile.write_text('<profiles/>')
        self.assertFalse(self.wait(interface))


if __name__ == '__main__':
    unittest.main()
