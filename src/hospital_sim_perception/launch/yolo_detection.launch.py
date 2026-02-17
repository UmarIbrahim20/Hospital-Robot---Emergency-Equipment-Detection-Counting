#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    # Get package directory
    pkg_dir = get_package_share_directory('hospital_sim_perception')
    
    # Config file path
    config_file = os.path.join(pkg_dir, 'config', 'yolo.yaml')
    
    # Declare arguments
    config_arg = DeclareLaunchArgument(
        'config_file',
        default_value=config_file,
        description='Path to YOLO config file'
    )
    
    # YOLO detection node
    yolo_node = Node(
        package='hospital_sim_perception',
        executable='yolo_node',
        name='yolo_detection',
        output='screen',
        parameters=[{
                'model_path': '/workspaces/cmp9767-MdUmarIbrahim-module/src/hospital_sim_perception/hospital_sim_perception/weights/best.pt',
                'confidence': 0.7,
                'process_every_n_frames': 3,
               ## 'camera_topic': '/limo/depth_camera_link/image_raw/compressed'
                'camera_topic': '/limo/depth_camera_link/image_raw'
            }],
        emulate_tty=True
    )
    
    return LaunchDescription([
        config_arg,
        yolo_node
    ])

