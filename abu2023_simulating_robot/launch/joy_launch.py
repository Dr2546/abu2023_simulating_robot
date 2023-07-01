import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():

    # package_name = "abu2023_simulating_stage"
    # pkg_path = os.path.join(get_package_share_directory('abu2023_simulating_stage'))
    # world_file = os.path.join(pkg_path,'world','abu2023.sdf')

    # rsp = IncludeLaunchDescription(
    #             PythonLaunchDescriptionSource([os.path.join(
    #                 get_package_share_directory(package_name),'launch','rsp.launch.py'
    #             )]), launch_arguments={'use_sim_time': 'true'}.items()
    # )

    # # Include the Gazebo launch file, provided by the gazebo_ros package
    # gazebo = IncludeLaunchDescription(
    #             PythonLaunchDescriptionSource([os.path.join(
    #                 get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]), launch_arguments={'world':world_file}.items() #Change Path to where the file is
    #          )

    # # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    # spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
    #                     arguments=['-topic', 'robot_description',
    #                                '-entity', 'my_bot',
    #                                '-x', "5.4",
    #                                '-y', "-0.7",
    #                                '-z', "1",],
    #                     output='screen')

    joy_node = Node(package='joy', executable='joy_node')

    joyconverter = Node(package='abu2023_simulating_robot', executable='joyconverter')
    

    # Launch them all!
    return LaunchDescription([
       joy_node,
       joyconverter
    ])

    # gazebo = IncludeLaunchDescription(
    #             PythonLaunchDescriptionSource([os.path.join(
    #                 get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
    #          )

    # spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
    #                     arguments=['-topic', 'robot_description',
    #                                '-entity', 'my_bot',
    #                                '-x', "5.4",
    #                                '-y', "-0.7",
    #                                '-z', "1",
    #                                '-roll', '0',
    #                                '-pitch', '0',
    #                                '-yaw', '0'],
    #                     output='screen')
