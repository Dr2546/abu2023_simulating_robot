from setuptools import setup

package_name = 'abu2023_simulating_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Daniel Riyavong',
    maintainer_email='danjan36@gmail.com',
    description='chansey with 4-mecanum wheel robot',
    license='Apache 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
         'getpos = my_gazebo.getpos:main',
         'controller = my_gazebo.controller:main'
        ],
    },
)
