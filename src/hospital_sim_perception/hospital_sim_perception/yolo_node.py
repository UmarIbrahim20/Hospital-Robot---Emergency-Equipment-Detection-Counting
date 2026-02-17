#!/usr/bin/env python3

import os
os.environ['TORCH_LOAD_WEIGHTS_ONLY'] = 'False'

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import Image, CompressedImage
from hospital_sim_msgs.msg import Detection, DetectionArray
from cv_bridge import CvBridge
import cv2
import numpy as np
from ultralytics import YOLO
import torch
import threading
import queue
import time

from rclpy.qos import qos_profile_sensor_data


class YOLODetectionNode(Node):
    def __init__(self):
        super().__init__('yolo_detection_node')
        
        # Parameters
        self.declare_parameter('model_path', 'weights/best.pt')
        self.declare_parameter('confidence', 0.7)
        self.declare_parameter('camera_topic', '/limo/depth_camera_link/image_raw')
        self.declare_parameter('process_every_n_frames', 3)  # Skip more frames
        self.declare_parameter('max_queue_size', 2)  # Limit queue buildup
        
        # GPU setup
        
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        if torch.cuda.is_available():
            self.get_logger().info(f'✓ GPU: {torch.cuda.get_device_name(0)}')
        else:
            self.get_logger().warn('⚠ No GPU - using CPU (slower)')
        
        # Load model
        model_path = self.get_parameter('model_path').value
        self.get_logger().info(f'Loading model: {model_path}')
        self.model = YOLO(model_path)
        self.model.to(self.device)
        
        # Config
        self.confidence = self.get_parameter('confidence').value
        self.process_every_n = self.get_parameter('process_every_n_frames').value
        self.max_queue_size = self.get_parameter('max_queue_size').value
        
        self.bridge = CvBridge()
        self.frame_counter = 0
        self.processed_count = 0

        ## for debug of frame
        self.dropped = 0

        
        # Thread-safe queue for images (prevents blocking)
        self.image_queue = queue.Queue(maxsize=self.max_queue_size)
        
        # QoS: BEST_EFFORT prevents message buildup
        qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=1  # Only keep latest message
        )
        
        
        # Subscribe
        camera_topic = self.get_parameter('camera_topic').value
        if camera_topic.endswith('/compressed'):
            self.sub = self.create_subscription(
                CompressedImage, camera_topic, 
                self.compressed_callback, qos)
        else:
            self.sub = self.create_subscription(
                Image, camera_topic, 
                self.image_callback, qos)
        
        viz_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            #reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=2
        )

        det_qos = QoSProfile(
          # reliability=ReliabilityPolicy.BEST_EFFORT,
           reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=5
        )
        # Publishers
        self.detection_pub = self.create_publisher(DetectionArray, '/hospital/detections', det_qos)

        self.viz_pub = self.create_publisher(Image, '/hospital/detections/image',  viz_qos)
        
        # Start processing thread (non-blocking)
        self.running = True
        self.process_thread = threading.Thread(target=self._process_loop, daemon=True)
        self.process_thread.start()
        
        self.get_logger().info('=' * 50)
        self.get_logger().info(f'YOLO Node Ready | Device: {self.device}')
        self.get_logger().info(f'Processing every {self.process_every_n} frames')
        self.get_logger().info(f'Confidence: {self.confidence:.0%}')
        self.get_logger().info('=' * 50)
    
    def image_callback(self, msg):
        """Lightweight callback - just queue the image"""

        ## debugg frame freezed
        self.frame_counter += 1
        if self.frame_counter % 30 == 0:
            self.get_logger().info(f"RX frame {self.frame_counter} enc={msg.encoding} {msg.width}x{msg.height}")

        self.frame_counter += 1
        
        # Skip frames
        if self.frame_counter % self.process_every_n != 0:
            return
        
        try:
            # Quick validation
            if msg.encoding not in ['rgb8', 'bgr8', 'mono8']:
                return
            
            # Convert quickly
            height, width = msg.height, msg.width
            channels = 3 if msg.encoding in ['rgb8', 'bgr8'] else 1
            img_array = np.frombuffer(bytes(msg.data), dtype=np.uint8)
            
            if channels == 3:
                cv_image = img_array.reshape((height, width, 3))
            else:
                cv_image = img_array.reshape((height, width))
                cv_image = cv2.cvtColor(cv_image, cv2.COLOR_GRAY2BGR)
            
            if msg.encoding == 'rgb8':
                cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
            
            # Make contiguous
            cv_image = np.ascontiguousarray(cv_image)
            
            # Try to queue (non-blocking)
            try:
                self.image_queue.put_nowait((cv_image, msg.header))
            except queue.Full:
                # Skip if queue full (prevents buildup)
                pass
                
        except Exception as e:
            self.get_logger().error(f'Callback error: {e}')
        except queue.Full:
            self.dropped += 1
            if self.dropped % 50 == 0:
                self.get_logger().warn(f"Dropping frames; queue full. dropped={self.dropped}")

    
    def compressed_callback(self, msg):
        """Handle compressed images"""
        self.frame_counter += 1
        
        if self.frame_counter % self.process_every_n != 0:
            return
        
        try:
            np_arr = np.frombuffer(bytes(msg.data), np.uint8)
            cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            
            if cv_image is None:
                return
            
            cv_image = np.ascontiguousarray(cv_image)
            
            try:
                self.image_queue.put_nowait((cv_image, msg.header))
            except queue.Full:
                pass
                
        except Exception as e:
            self.get_logger().error(f'Compressed callback error: {e}')
    
    def _process_loop(self):
        """Background thread - processes images without blocking callbacks"""
        self.get_logger().info("Process loop started")

        while self.running:
            try:
                # Get image from queue (timeout prevents hanging)
                cv_image, header = self.image_queue.get(timeout=0.1)
                
                # Run inference
                start = time.time()
                results = self.model(
                    cv_image,
                    conf=self.confidence,
                    device=self.device,
                    imgsz=640,
                    verbose=False,
                    half=(self.device != 'cpu')
                )
                inference_time = time.time() - start
                
                # Build detection message
                detections_msg = DetectionArray()
                detections_msg.header = header
                
                img_h, img_w = cv_image.shape[:2]
                
                for result in results:
                    for box in result.boxes:
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        conf = float(box.conf[0])
                        cls_id = int(box.cls[0])
                        
                        det = Detection()
                        det.class_id = cls_id
                        det.class_name = str(self.model.names.get(cls_id, f"class_{cls_id}"))
                        det.confidence = conf
                        
                        det.x_center = float((x1 + x2) / 2 / img_w)
                        det.y_center = float((y1 + y2) / 2 / img_h)
                        det.width = float((x2 - x1) / img_w)
                        det.height = float((y2 - y1) / img_h)
                        
                        det.x_min = int(x1)
                        det.y_min = int(y1)
                        det.x_max = int(x2)
                        det.y_max = int(y2)
                        
                        detections_msg.detections.append(det)
                
                detections_msg.num_detections = len(detections_msg.detections)
                self.processed_count += 1
                
                # Publish
                self.detection_pub.publish(detections_msg)
                
                # Visualize
                viz = self._draw_detections(cv_image, detections_msg)
                viz_msg = self.bridge.cv2_to_imgmsg(viz, encoding='bgr8')
                viz_msg.header = header
                self.viz_pub.publish(viz_msg)
                
                # Log
                fps = 1.0 / inference_time if inference_time > 0 else 0
                if detections_msg.num_detections > 0:
                    det_str = ', '.join([f"{d.class_name}({d.confidence:.2f})" 
                                        for d in detections_msg.detections])
                    self.get_logger().info(
                        f'#{self.processed_count}: {det_str} '
                        f'[{inference_time*1000:.0f}ms, {fps:.1f}fps]'
                    )
                
            except queue.Empty:
                continue
            except Exception as e:
                self.get_logger().error(f'Processing error: {e}')
    
    def _draw_detections(self, image, detections_msg):
        """Draw bounding boxes"""
        viz = image.copy()
        
        colors = {
            'exit_door': (0, 255, 0),
            'fire_extinguisher': (0, 0, 255),
            'first_aid_kit': (255, 0, 0)
        }
        
        for det in detections_msg.detections:
            color = colors.get(det.class_name, (255, 255, 255))
            
            cv2.rectangle(viz, (det.x_min, det.y_min), 
                         (det.x_max, det.y_max), color, 2)
            
            label = f'{det.class_name} {det.confidence:.0%}'
            cv2.putText(viz, label, (det.x_min, det.y_min - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Stats
        cv2.putText(viz, f'Detections: {detections_msg.num_detections}', 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return viz
    
    def destroy_node(self):
        """Clean shutdown"""
        self.running = False
        if hasattr(self, 'process_thread'):
            self.process_thread.join(timeout=2.0)
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = YOLODetectionNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.get_logger().info(f'Processed {node.processed_count} frames')
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

