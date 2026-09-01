import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Definisci i percorsi dei pacchetti
    pkg_arm_description = get_package_share_directory('arm_description')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # Percorso al file Xacro del robot
    xacro_file = os.path.join(pkg_arm_description, 'urdf', 'arm.urdf.xacro')

    # Converti il file xacro in URDF tramite il comando 'xacro'
    robot_description_content = ParameterValue(Command(['xacro ', xacro_file]), value_type=str)
    
    # Parametro da passare al robot_state_publisher
    robot_description = {'robot_description': robot_description_content}

    # Nodo Robot State Publisher: pubblica l'URDF sul topic /robot_description
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[
            robot_description,
            {"use_sim_time": True} # IMPORTANTE per Gazebo
        ]
    )

    # Includi il file di lancio principale di Gazebo (ros_gz_sim)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-r empty.sdf'}.items(), # Carica un mondo vuoto e avvia
    )

    # Nodo di spawn del robot in Gazebo usando "create" da ros_gz_sim
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=[
            '-topic', '/robot_description',
            '-name', 'armando',
            '-allow_renaming', 'true'
        ]
    )

    # --- AGGIUNTE DAL PUNTO 2C ---

    # Nodo per avviare il joint_state_broadcaster
    joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )  

    # Nodo per avviare il controller di posizione
    position_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["position_controller", "--controller-manager", "/controller_manager"],  
    ) 

    # Handler per avviare il position_controller DOPO che il robot è stato spawnato
    delay_position_controller = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_entity,
            on_exit=[position_controller],
        )
    )

    # Handler per avviare il joint_state_broadcaster DOPO che il robot è stato spawnato[cite: 3]
    delay_joint_state_broadcaster = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_entity,
            on_exit=[joint_state_broadcaster],
        )
    )

# Nodo Bridge per la telecamera (Punto 3c)
    bridge_camera = Node(
        package='ros_ign_bridge', # Usa 'ros_gz_bridge' se sei su distribuzioni ROS2 più recenti
        executable='parameter_bridge',
        arguments=[
            # Collega il topic di Gazebo a quello di ROS usando i tipi di messaggio corretti
            '/camera@sensor_msgs/msg/Image@gz.msgs.Image',
            '/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo',
        ],
        output='screen'
    )
    
    
    return LaunchDescription([
        robot_state_publisher_node,
        gazebo,
        spawn_entity,
        delay_position_controller,
        delay_joint_state_broadcaster,
        bridge_camera,
    ])
