from setuptools import setup
import os
from glob import glob

package_name = 'limo_speaker'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        (os.path.join('share', package_name), ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        # (os.path.join('share/ament_index/resource_index/packages'), [package_name]),
        (os.path.join('share', package_name), ['resource/' + package_name]),
    ],
    install_requires=[
        'setuptools',
        'sounddevice',
    ],
    zip_safe=True,
    maintainer='cooperj',
    maintainer_email='cooperj@example.com',
    description='Package description',
    license='License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'play_audio = limo_speaker.playAudio:main',
            'play_tts = limo_speaker.playTTS:main',
        ],
    },
)