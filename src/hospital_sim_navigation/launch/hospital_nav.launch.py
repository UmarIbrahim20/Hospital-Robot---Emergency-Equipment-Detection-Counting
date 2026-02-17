import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkg_hospital_nav = get_package_share_directory('hospital_sim_navigation')
    pkg_hospital_sim = get_package_share_directory('hospital_simulation')
    pkg_limo_nav = get_package_share_directory('limo_navigation')

    # Define the paths
    map_file = os.path.join(pkg_hospital_nav, 'maps', 'hospital_map_first.yaml')
    
    # NEW: We must point to the params file so RewrittenYaml doesn't crash
    hosp_params_file = os.path.join(pkg_hospital_nav, 'params', 'nav2_params.yaml')

    return LaunchDescription([
        # 1. Simulation
        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource(
        #         os.path.join(pkg_hospital_sim, 'launch', 'hospital_world.launch.py')
        #     ),
        #     launch_arguments={'use_sim_time': 'true'}.items()
        # ),

        # 2. Localization (Passing the missing params_file)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_limo_nav, 'launch', 'limo_localization.launch.py')
            ),
            launch_arguments={
                'use_sim_time': 'true',
                'map': map_file,
                'params_file': hosp_params_file,  # FIXED: Adding this argument
                'use_rviz': 'false'                # Optional: opens RViz for you
            }.items()
        ),

        # 3. Controller
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_limo_nav, 'launch', 'limo_controller.launch.py')
            ),
            launch_arguments={'use_sim_time': 'true'}.items()
        )
    ])