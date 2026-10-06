# RL_2025_HOMEWORK_1

# Prerequisites
To compile and run the project, it is necessary to have the essential dependencies for ROS 2 and Gazebo installed. After logging into your container or virtual machine, be sure to install:
* `arm_description`
* `armando_controller`
* `armando_gazebo`

# Package update
 ``` bash
sudo apt update
```
# Optional GUI tools for debugging and visualization
``` bash
 sudo apt install ros-humble-joint-state-publisher-gui
 sudo apt install ros-humble-rqt-image-view
```
# BUILD
Cloning the Repository
Clone this repository into the desired folder :
``` bash
 git clone https://github.com/Ald0oo/RL_2025_HOMEWORK_1.git
 colcon build
 source install/setup.bash
``` 
 # HOW TO LAUNCH
Visualization Robot (Rviz2)
To see only the kinematic model of the robot and its frames in RViz2:
``` bash
 ros2 launch arm_description armando_display.launch.py
``` 
Complete Simulation (Gazebo) The main launchfile loads the robot in Gazebo and starts the controllers (ros2_control).

Default Control Mode (Position): Starts the joint position controller.
``` bash
 ros2 launch armando_gazebo armando_world.launch.py
``` 
Position Control Mode (Position): Starts the joint position controller.
``` bash
 ros2 launch armando_gazebo armando_world.launch.py controller_mode:=position.
``` 
Trajectory Mode (requires external node): Starts the joint trajectory controller.
``` bash
 ros2 launch armando_gazebo armando_world.launch.py controller_mode:=trajectory
``` 
 # INTERACTION AND CONTROL
Manual Position Control (Test)
To send a specific position setpoint to the joints (only in position mode), where the values are in the order [j0, j1, j2, j3] in radians: Open a new terminal and run the source command. Send the commands:

# Zero Position (to stabilize the robot)
``` bash
 ros2 topic pub --rate 10 /arm_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.0, 0.0, 0.0, 0.0]}"
``` 
To visualize the real-time video feed from the simulated camera in Gazebo: Launch rqt_image_view (after running source in a new terminal) and select the /camera/image topic:
``` bash
 ros2 run rqt_image_view rqt_image_view
``` 
