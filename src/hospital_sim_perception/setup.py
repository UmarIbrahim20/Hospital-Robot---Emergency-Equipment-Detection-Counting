from setuptools import setup
import os
from glob import glob

package_name = 'hospital_sim_perception'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'config'), glob('hospital_sim_perception/config/*.yaml')),
        (os.path.join('share', package_name, 'weights'), glob('hospital_sim_perception/weights/*.pt')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your@email.com',
    description='YOLO-based perception for hospital simulation',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'yolo_node = hospital_sim_perception.yolo_node:main',
            'detection_counter_node = hospital_sim_perception.detection_counter_node:main',
            'waypoint_node = hospital_sim_perception.waypoint_follower:main'
        ],
    },
)
