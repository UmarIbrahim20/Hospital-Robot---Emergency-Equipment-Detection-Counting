import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # 1. Setup Paths for all packages involved
    pkg_hospital_sim = get_package_share_directory('hospital_simulation')
    pkg_limo_nav = get_package_share_directory('limo_navigation')
    
    # Define Launch Configurations
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
    # Path to Cartographer configuration (lua files) inside limo_navigation
    cartographer_config_dir = LaunchConfiguration('cartographer_config_dir', 
                                                  default=os.path.join(pkg_limo_nav, 'params'))
    configuration_basename = LaunchConfiguration('configuration_basename',
                                                 default='limo_lds_2d.lua')

    # Grid and publishing parameters
    resolution = LaunchConfiguration('resolution', default='0.05')
    publish_period_sec = LaunchConfiguration('publish_period_sec', default='1.0')

    # Path to the RViz configuration for visualization
    rviz_config_dir = os.path.join(pkg_limo_nav, 'rviz', 'limo_navigation.rviz')

    return LaunchDescription([
        # Declare arguments for the launch system
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'),

        # --- 1. THE SIMULATION NODE (Included from your simulation package) ---
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_hospital_sim, 'launch', 'hospital_world.launch.py')
            ),
            # Passing use_sim_time ensures all robot sensors sync with Gazebo
            launch_arguments={'use_sim_time': use_sim_time}.items()
        ),

        # --- 2. THE SLAM (CARTOGRAPHER) NODE ---
        Node(
            package='cartographer_ros',
            executable='cartographer_node',
            name='cartographer_node',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
            arguments=['-configuration_directory', cartographer_config_dir,
                       '-configuration_basename', configuration_basename],
            ),

        # --- 3. THE OCCUPANCY GRID NODE (Required to turn SLAM data into a 2D map) ---
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_limo_nav, 'launch', 'occupancy_grid.launch.py')
            ),
            launch_arguments={'use_sim_time': use_sim_time, 
                              'resolution': resolution,
                              'publish_period_sec': publish_period_sec}.items(),
        ),

        # --- 4. THE VISUALIZATION NODE (RViz2) ---
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_dir],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen'),
    ])