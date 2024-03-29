from setuptools import setup, find_packages

setup(
    name='teamfighttactics',
    version='0.1.0',
    description='Teamfight Tactics Gym Environment',
    packages=find_packages(),
    install_requires=[
        'gym>=0.21.0',
        'numpy>=1.13.0',
        'opencv-python>=3.4.2.0',
    ]
)