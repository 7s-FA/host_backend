"""ROS integration check; mock voltage is permitted ONLY in isolated domain 149."""
import math
import os
import time
import unittest

if os.environ.get('ROS_DOMAIN_ID') != '149':
    raise RuntimeError('Run only with ROS_DOMAIN_ID=149; never publish mock battery on real domain')

import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import BatteryState
from std_msgs.msg import Float32
from m1_battery_bridge import M1BatteryBridge


class BatteryRelayTest(unittest.TestCase):
    def test_real_ros_delivery_and_no_stale_republishing(self):
        rclpy.init()
        relay = M1BatteryBridge()
        probe = rclpy.create_node('m1_battery_probe')
        executor = SingleThreadedExecutor()
        executor.add_node(relay)
        executor.add_node(probe)
        received = []
        publisher = probe.create_publisher(Float32, '/stm32/battery_voltage', qos_profile_sensor_data)
        subscription = probe.create_subscription(
            BatteryState, '/burger1/battery_state', received.append, qos_profile_sensor_data)

        def spin(seconds):
            deadline = time.monotonic() + seconds
            while time.monotonic() < deadline:
                executor.spin_once(timeout_sec=0.02)

        try:
            spin(1)
            self.assertEqual(received, [], 'No fabricated startup reading')
            publisher.publish(Float32(data=11.8))
            spin(0.5)
            self.assertEqual(len(received), 1)
            sample = received[0]
            self.assertAlmostEqual(sample.voltage, 11.8, places=4)
            self.assertTrue(sample.present)
            self.assertGreater(sample.header.stamp.sec, 0)
            self.assertTrue(math.isnan(sample.percentage))
            self.assertTrue(math.isnan(sample.current))
            for invalid in (0.0, -1.0, math.nan, math.inf):
                publisher.publish(Float32(data=invalid))
                spin(0.1)
            spin(1.2)
            self.assertEqual(len(received), 1, 'Bad samples and silence must not refresh data')
            publisher.publish(Float32(data=11.7))
            spin(0.3)
            self.assertEqual(len(received), 2)
            self.assertAlmostEqual(received[-1].voltage, 11.7, places=4)
        finally:
            executor.shutdown()
            probe.destroy_node()
            relay.destroy_node()
            rclpy.shutdown()


if __name__ == '__main__':
    unittest.main()
