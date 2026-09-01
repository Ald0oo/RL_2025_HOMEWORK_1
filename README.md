# RL_2025_HOMEWORK_1
Bring up your robot

## Available Packages in this Repository
* `armando_description`
* `armando_gazebo`
* `armando_controller`
  
## Getting Started
``` bash
git clone https://github.com/Ald0oo/RL_2025_HOMEWORK_1.git
colcon build 
source install/setup.bash
```
## Usage
# 1. Launch the Manipulator in Rviz
To start the manipulator simulation in Rviz run the command:
``` bash
ros2 launch armando_description armando_display.launch.py
```
rviz will be started.

# 2. Launch the Manipulator in Gazebo
To start the manipulator simulation in Gazebo run the command:
``` bash
ros2 launch armando_gazebo armando_world.launch.py
```
# 3. Camera Sensor
After launching the manipulator in Gazebo, open another terminal and run:
``` bash
ros2 run rqt_image_view rqt_image_view
``` 
# 4. Controller
There are two controllers available, position controller and trajectory controller. To active a controller you have to tun this command:
``` bash
ros2 launch armando_gazebo armando_world.launch.py controller_type:=<type>
```
where <type> can be position or trajectory, by defult is set to position.

# 5. Subscriber and Publisher node
To launch the subscriber and the publisher node you have to run:
``` bash
ros2 run armando_controller arm_controller_node --ros-args -p controller_type:=<value>
```
where <value> can be true for the position controller, or false for the trajectory controller.
