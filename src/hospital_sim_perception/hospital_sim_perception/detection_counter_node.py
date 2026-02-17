#!/usr/bin/env python3

import math
import numpy as np
from collections import defaultdict, deque

import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

import message_filters

from hospital_sim_msgs.msg import DetectionArray
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PointStamped

import tf2_ros
from tf2_ros import TransformException
import tf2_geometry_msgs


def stamp_to_sec(stamp) -> float:
    return float(stamp.sec) + float(stamp.nanosec) * 1e-9


class DetectionCounterWorld(Node):
    def __init__(self):
        super().__init__('detection_counter_world')

        # ---------- Topics ----------
        self.declare_parameter('detections_topic', '/hospital/detections')
        self.declare_parameter('depth_topic', '/limo/depth_camera_link/depth/image_raw')
        self.declare_parameter('camera_info_topic', '/limo/depth_camera_link/depth/camera_info')

        # ---------- Sync ----------
        self.declare_parameter('slop', 0.10)
        self.declare_parameter('queue_size', 30)

        # ---------- Depth sampling ----------
        self.declare_parameter('use_median', True)
        self.declare_parameter('median_grid', 7)
        self.declare_parameter('min_depth', 0.05)
        self.declare_parameter('max_depth', 20.0)

        # ---------- De-dupe (WORLD frame) ----------
        self.declare_parameter('xy_threshold_m', 0.3)  # strict
        self.declare_parameter('z_threshold_m', 0.9)    # strict

        # ---------- Robot distance gating ----------
        self.declare_parameter('robot_max_dist_m', 2.0)  # only count if robot is within this XY distance

        # ---------- Frames ----------
        self.declare_parameter('target_frame', 'map')     # try 'map' first; if you don't have map, use 'odom'
        self.declare_parameter('robot_frame', 'base_link')  # robot reference
        self.declare_parameter('tf_timeout_sec', 0.2)

        # ---------- Logs ----------
        self.declare_parameter('log_sync_every_n', 10)
        self.declare_parameter('log_summary_every_n', 20)
        self.declare_parameter('log_new', True)

        # memory cap
        self.declare_parameter('max_points_per_class', 200)

        self.det_topic = self.get_parameter('detections_topic').value
        self.depth_topic = self.get_parameter('depth_topic').value
        self.info_topic = self.get_parameter('camera_info_topic').value

        self.slop = float(self.get_parameter('slop').value)
        self.queue_size = int(self.get_parameter('queue_size').value)

        self.use_median = bool(self.get_parameter('use_median').value)
        self.grid = int(self.get_parameter('median_grid').value)
        if self.grid % 2 == 0:
            self.grid += 1

        self.min_depth = float(self.get_parameter('min_depth').value)
        self.max_depth = float(self.get_parameter('max_depth').value)

        self.xy_th = float(self.get_parameter('xy_threshold_m').value)
        self.z_th = float(self.get_parameter('z_threshold_m').value)

        self.robot_max = float(self.get_parameter('robot_max_dist_m').value)

        self.target_frame = self.get_parameter('target_frame').value
        self.robot_frame = self.get_parameter('robot_frame').value
        self.tf_timeout = float(self.get_parameter('tf_timeout_sec').value)

        self.log_sync_every = int(self.get_parameter('log_sync_every_n').value)
        self.log_summary_every = int(self.get_parameter('log_summary_every_n').value)
        self.log_new = bool(self.get_parameter('log_new').value)

        self.max_points_per_class = int(self.get_parameter('max_points_per_class').value)

        # ---------- QoS ----------
        self.sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )
        self.det_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )

        # ---------- TF ----------
        self.tf_buffer = tf2_ros.Buffer(cache_time=Duration(seconds=10.0))
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # ---------- message_filters Subscribers ----------
        self.det_sub = message_filters.Subscriber(self, DetectionArray, self.det_topic, qos_profile=self.det_qos)
        self.depth_sub = message_filters.Subscriber(self, Image, self.depth_topic, qos_profile=self.sensor_qos)
        self.info_sub = message_filters.Subscriber(self, CameraInfo, self.info_topic, qos_profile=self.sensor_qos)

        self.sync = message_filters.ApproximateTimeSynchronizer(
            [self.det_sub, self.depth_sub, self.info_sub],
            queue_size=self.queue_size,
            slop=self.slop,
            allow_headerless=False
        )
        self.sync.registerCallback(self.cb)

        # ---------- Counters ----------
        self.sync_count = 0
        self.total_unique = 0
        self.per_class_unique = defaultdict(int)
        self.class_points_world = defaultdict(lambda: deque(maxlen=self.max_points_per_class))  # cls -> [(x,y,z),...]

        self.get_logger().info("=======================================")
        self.get_logger().info("3D->WORLD counter node started (YOLO untouched)")
        self.get_logger().info(f"target_frame={self.target_frame} robot_frame={self.robot_frame}")
        self.get_logger().info(f"robot_max_dist_m={self.robot_max}")
        self.get_logger().info(f"STRICT de-dupe: xy<{self.xy_th} AND dz<{self.z_th}")
        self.get_logger().info("=======================================")

    # -------- Depth utilities --------
    def _depth_array(self, depth_msg: Image) -> np.ndarray:
        h, w = depth_msg.height, depth_msg.width
        if depth_msg.encoding == '32FC1':
            return np.frombuffer(depth_msg.data, dtype=np.float32).reshape((h, w))
        if depth_msg.encoding == '16UC1':
            arr = np.frombuffer(depth_msg.data, dtype=np.uint16).reshape((h, w)).astype(np.float32)
            return arr * 0.001
        return np.frombuffer(depth_msg.data, dtype=np.float32).reshape((h, w))

    def _sample_depth(self, depth: np.ndarray, u: int, v: int, bw: int, bh: int) -> float:
        h, w = depth.shape[:2]
        u = int(np.clip(u, 0, w - 1))
        v = int(np.clip(v, 0, h - 1))

        if not self.use_median:
            return float(depth[v, u])

        half = self.grid // 2
        pad_x = max(half, max(1, bw // 10))
        pad_y = max(half, max(1, bh // 10))

        x0 = int(np.clip(u - pad_x, 0, w - 1))
        x1 = int(np.clip(u + pad_x, 0, w - 1))
        y0 = int(np.clip(v - pad_y, 0, h - 1))
        y1 = int(np.clip(v + pad_y, 0, h - 1))

        xs = np.linspace(x0, x1, self.grid).astype(int)
        ys = np.linspace(y0, y1, self.grid).astype(int)

        vals = []
        for yy in ys:
            for xx in xs:
                z = float(depth[yy, xx])
                if math.isfinite(z) and self.min_depth <= z <= self.max_depth:
                    vals.append(z)

        return float(np.median(vals)) if vals else float('nan')

    # -------- De-dupe in WORLD frame --------
    def _is_duplicate_world(self, cls: str, x: float, y: float, z: float) -> bool:
        for (xp, yp, zp) in self.class_points_world[cls]:
            xy = math.hypot(x - xp, y - yp)
            dz = abs(z - zp)
            if xy < self.xy_th and dz < self.z_th:
                return True
        return False

    def _print_summary(self):
        per_class_str = ", ".join([f"{k}:{v}" for k, v in sorted(self.per_class_unique.items())])
        self.get_logger().info(f"[COUNT] total_unique={self.total_unique} | per_class=({per_class_str})")

    # -------- Main callback --------
    def cb(self, det_msg: DetectionArray, depth_msg: Image, info_msg: CameraInfo):
        self.sync_count += 1

        if self.sync_count % self.log_sync_every == 0:
            t_det = stamp_to_sec(det_msg.header.stamp)
            t_depth = stamp_to_sec(depth_msg.header.stamp)
            t_info = stamp_to_sec(info_msg.header.stamp)
            self.get_logger().info(
                f"[SYNC#{self.sync_count}] frame={det_msg.header.frame_id} "
                f"dt(depth-det)={t_depth - t_det:+.4f}s dt(info-det)={t_info - t_det:+.4f}s "
                f"det_count={len(det_msg.detections)}"
            )

        fx, fy = info_msg.k[0], info_msg.k[4]
        cx, cy = info_msg.k[2], info_msg.k[5]
        if fx <= 0.0 or fy <= 0.0:
            return

        depth = self._depth_array(depth_msg)

        # Need transforms:
        # - depth_msg.header.frame_id (depth_link) -> target_frame
        # - robot_frame -> target_frame
        tf_timeout = Duration(seconds=self.tf_timeout)

        # Get robot pose in target frame (translation is enough for distance)
        try:
            tf_robot = self.tf_buffer.lookup_transform(
                self.target_frame,
                self.robot_frame,
                rclpy.time.Time(),
                tf_timeout
            )
            rx = tf_robot.transform.translation.x
            ry = tf_robot.transform.translation.y
            rz = tf_robot.transform.translation.z
        except TransformException as ex:
            # No TF yet, skip counting this cycle
            if self.sync_count % self.log_sync_every == 0:
                self.get_logger().warn(f"[TF] robot transform {self.target_frame}<-{self.robot_frame} not available: {ex}")
            return

        # For each detection: compute camera XYZ -> transform -> world XYZ -> robot distance gate -> de-dupe -> count
        for det in det_msg.detections:
            u = int((det.x_min + det.x_max) / 2)
            v = int((det.y_min + det.y_max) / 2)
            bw = int(det.x_max - det.x_min)
            bh = int(det.y_max - det.y_min)

            z = self._sample_depth(depth, u, v, bw, bh)
            if not math.isfinite(z) or z < self.min_depth or z > self.max_depth:
                continue

            # camera frame (depth_link)
            Xc = (u - cx) * z / fx
            Yc = (v - cy) * z / fy
            Zc = z

            cam_pt = PointStamped()
            cam_pt.header = depth_msg.header
            cam_pt.point.x = float(Xc)
            cam_pt.point.y = float(Yc)
            cam_pt.point.z = float(Zc)

            # transform to target frame (map/odom)
            try:
                world_pt = self.tf_buffer.transform(cam_pt, self.target_frame, timeout=tf_timeout)
            except TransformException as ex:
                if self.sync_count % self.log_sync_every == 0:
                    self.get_logger().warn(f"[TF] point transform to {self.target_frame} failed: {ex}")
                continue

            xw = world_pt.point.x
            yw = world_pt.point.y
            zw = world_pt.point.z  # height in world

            # robot distance in plane
            dxy_robot = math.hypot(xw - rx, yw - ry)

            # gate: only count if robot is near
            if dxy_robot > self.robot_max:
                continue

            cls = det.class_name
            conf = float(det.confidence)

            # de-dupe in world frame
            if self._is_duplicate_world(cls, xw, yw, zw):
                continue

            # count
            self.class_points_world[cls].append((xw, yw, zw))
            self.per_class_unique[cls] += 1
            self.total_unique += 1

            self.get_logger().info(
                f"[NEW] {cls} conf={conf:.2f} | WORLD XYZ=({xw:.2f},{yw:.2f},{zw:.2f}) "
                f"| robot_xy_dist={dxy_robot:.2f}m | total={self.total_unique} class_count={self.per_class_unique[cls]}"
            )

        if self.sync_count % self.log_summary_every == 0:
            self._print_summary()


def main():
    rclpy.init()
    node = DetectionCounterWorld()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            node.destroy_node()
        except Exception:
            pass
        rclpy.shutdown()


if __name__ == '__main__':
    main()
