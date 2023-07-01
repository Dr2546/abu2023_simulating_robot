# ABU2023_Simulating_Robot

This is 4 mecanum wheel robot simulating in Gazebo for [Robocon2023 Simulating Stage](https://github.com/Dr2546/abu2023_simulating_stage).


# How to build package
1.Create your workspace with a ```src``` sub-directory.

2.Inside a ```src``` ,clone this git with ```git clone https://github.com/Dr2546/abu2023_simulating_robot.git```.

3.In the root of your workspace,run ```rosdep install -i --from-path src --rosdistro foxy -y``` to check dependencies.

> Note:Ros distro may vary depends on you,this project use Ros2 foxy.

4.Run ```colcon build``` or ```colcon build --packages-select abu2023_simulating_robot``` if your workspace has many packages and you only want to build this package.

5.In your root workspace , go inside  ```install/abu2023_simulating_robot/lib```. If there is no ```abu2023_simulating_robot``` directory, create it,then copy ```getpos.py``` ```controller.py``` from ```install/abu2023_simulating_robot/bin``` and paste under ```abu2023_simulating_robot```.

# How to use/run package
1.Open up your workspace in terminal.

2.Run ```. install/setup.bash```

3.Run ```ros2 launch abu2023_simulating_stage launch_sim.launch.py``` first from [Robocon2023 Simulating Stage](https://github.com/Dr2546/abu2023_simulating_stage).

## Controlling Robot

### Use keyboard

controller node is for controlling robot with a joystick that create for this only so I will not talk about it,so alternative way is use ```teleop_twist_keyboard```

### Use Joystick

as now the only joystick that can control this robot is Logitech Extreme 3d pro

1.With Gazebo is running , run ```ros2 run abu2023_simulating_robot joy_launch.py``` in another terminal.

## Position between Robot and Pole

getpos node is for get distance between pole and robot

1.With Gazebo is running , run ```ros2 run abu2023_simulating_robot getpos pole_number``` in another terminal.
