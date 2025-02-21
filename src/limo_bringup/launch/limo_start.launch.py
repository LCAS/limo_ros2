import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Get the launch directory
    limo_base_launch_dir = os.path.join(
        get_package_share_directory('limo_base'), 'launch')
    ydlidar_launch_dir = os.path.join(
        get_package_share_directory('ydlidar_ros2_driver'), 'launch')
    limo_speaker_launch_dir = os.path.join(
        get_package_share_directory('limo_speaker'), 'launch')

    # Create the launch configuration variables
    declare_port_name = DeclareLaunchArgument(
        'port_name',
        default_value='ttyTHS1')

    declare_odom_name = DeclareLaunchArgument(
        name='odom_topic_name',
        default_value='odom')

    declare_use_mcnamu = DeclareLaunchArgument(
        name='use_mcnamu',
        default_value='false')

    start_imu_static_transform_pub_cmd = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='base_link_to_imu',
        arguments="0.0 0.0 0.0 0.0 0.0 0.0 /base_link /imu_link".split(
            ' '))

    launch_limo_base = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(limo_base_launch_dir, 'limo_base.launch.py')),
        launch_arguments={
            'port_name':
                LaunchConfiguration('port_name'),
                'odom_topic_name':
                LaunchConfiguration('odom_topic_name'),
                'use_mcnamu':
                LaunchConfiguration('use_mcnamu')
        }.items())

    launch_yd_lidar = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ydlidar_launch_dir, 'open_ydlidar_launch.py')
        )
    )
    
    launch_limo_speaker = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(limo_speaker_launch_dir, 'limo_speaker.launch.py')
        )
    )

    # Create the launch description and populate
    ld = LaunchDescription()

    # Declare the launch options
    ld.add_action(declare_odom_name)
    ld.add_action(declare_port_name)
    ld.add_action(declare_use_mcnamu)

    ld.add_action(launch_limo_base)
    ld.add_action(launch_yd_lidar)
    ld.add_action(launch_limo_speaker)

    ld.add_action(start_imu_static_transform_pub_cmd)

    return ld