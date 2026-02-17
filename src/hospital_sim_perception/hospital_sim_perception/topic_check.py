#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from hospital_sim_msgs.msg import DetectionArray

import message_filters


def stamp_to_sec(stamp):
    return float(stamp.sec) + float(stamp.nanosec) * 1e-9


class SyncChecker(Node):
    def __init__(self):
        super().__init__('sync_checker')

        # Params (tune slop)
        self.declare_parameter('rgb_topic', '/limo/depth_camera_link/image_raw')
        self.declare_parameter('depth_topic', '/limo/depth_camera_link/depth/image_raw')
        self.declare_parameter('det_topic', '/hospital/detections')
        self.declare_parameter('queue_size', 30)
        self.declare_parameter('slop', 0.10)  # seconds

        rgb_topic = self.get_parameter('rgb_topic').value
        depth_topic = self.get_parameter('depth_topic').value
        det_topic = self.get_parameter('det_topic').value
        queue_size = int(self.get_parameter('queue_size').value)
        slop = float(self.get_parameter('slop').value)

        self.get_logger().info(f"RGB:   {rgb_topic}")
        self.get_logger().info(f"DEPTH: {depth_topic}")
        self.get_logger().info(f"DET:   {det_topic}")
        self.get_logger().info(f"Approx sync slop={slop}s queue={queue_size}")

        # message_filters subscribers
        self.rgb_sub = message_filters.Subscriber(self, Image, rgb_topic)
        self.depth_sub = message_filters.Subscriber(self, Image, depth_topic)
        self.det_sub = message_filters.Subscriber(self, DetectionArray, det_topic)

        # Approximate sync: (detections <-> depth <-> rgb)
        ats = message_filters.ApproximateTimeSynchronizer(
            [self.rgb_sub, self.depth_sub, self.det_sub],
            queue_size=queue_size,
            slop=slop
        )
        ats.registerCallback(self.cb)

        self.last_print = 0.0

    def cb(self, rgb_msg: Image, depth_msg: Image, det_msg: DetectionArray):
        t_rgb = stamp_to_sec(rgb_msg.header.stamp)
        t_depth = stamp_to_sec(depth_msg.header.stamp)
        t_det = stamp_to_sec(det_msg.header.stamp)

        dt_depth_rgb = t_depth - t_rgb
        dt_det_rgb = t_det - t_rgb
        dt_det_depth = t_det - t_depth

        # Throttle prints a bit
        now = self.get_clock().now().nanoseconds * 1e-9
        if now - self.last_print > 1.0:
            self.last_print = now
            self.get_logger().info(
                f"frame_id(rgb/depth/det)=({rgb_msg.header.frame_id}, {depth_msg.header.frame_id}, {det_msg.header.frame_id}) | "
                f"dt(depth-rgb)={dt_depth_rgb:+.4f}s dt(det-rgb)={dt_det_rgb:+.4f}s dt(det-depth)={dt_det_depth:+.4f}s | "
                f"det_count={det_msg.num_detections}"
            )


def main():
    rclpy.init()
    node = SyncChecker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
