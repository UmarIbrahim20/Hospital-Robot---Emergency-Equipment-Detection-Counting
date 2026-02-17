#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Declare arguments
    confidence_arg = DeclareLaunchArgument(
        'confidence',
        default_value='0.7',
        description='Detection confidence threshold (0.0-1.0)'
    )
    
    dedup_radius_arg = DeclareLaunchArgument(
        'dedup_radius',
        default_value='0.15',
        description='Deduplication radius in meters'
    )
    
    camera_topic_arg = DeclareLaunchArgument(
        'camera_topic',
        default_value='/limo/depth_camera_link/depth/image_raw/compressedDepth',
        description='Camera image topic'
    )
    
    # YOLO Detection Node
    # yolo_node = Node(
    #     package='hospital_sim_perception',
    #     executable='yolo_node',
    #     name='yolo_detection',
    #     output='screen',
    #     parameters=[{
    #         'model_path': 'weights/best.pt',
    #         'confidence': LaunchConfiguration('confidence'),
    #         'camera_topic': LaunchConfiguration('camera_topic'),
    #         'process_every_n_frames': 3,
    #         'max_queue_size': 2
    #     }]
    # )
    
    # Detection Counter Node
    counter_node = Node(
        package='hospital_sim_perception',
        executable='detection_counter_node',
        name='detection_counter',
        output='screen',
        parameters=[{
            'deduplication_radius': LaunchConfiguration('dedup_radius'),
            'memory_timeout': 10.0,
            'camera_info_topic': '/limo/depth_camera_link/camera_info',
            'min_confidence': LaunchConfiguration('confidence')
        }]
    )
    
    return LaunchDescription([
        confidence_arg,
        dedup_radius_arg,
        camera_topic_arg,
       ## yolo_node,
        counter_node
    ])