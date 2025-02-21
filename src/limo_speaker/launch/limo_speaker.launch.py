from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='limo_speaker',
            executable='play_audio',
            name='play_audio',
            output='screen'
        ),
        Node(
            package='limo_speaker',
            executable='play_tts',
            name='play_tts',
            output='screen'
        ),
    ])