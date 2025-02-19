from ament_index_python.packages import get_package_share_directory
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
import launch_ros.actions
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.conditions import IfCondition
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
#不知道呢据说可以不用里程计 实现建图 导航
def generate_launch_description():
    
    #bringup_dir：获取turn_on_wheeltec_robot功能包的共享目录路径。
    #launch_dir：构建launch目录的完整路径。
    
    bringup_dir = get_package_share_directory('turn_on_wheeltec_robot')
    launch_dir = os.path.join(bringup_dir, 'launch')


    #启动Wheeltec机器人相关的节点
    wheeltec_robot = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(launch_dir, 'turn_on_wheeltec_robot.launch.py')),
    )
    #启动雷达节点
    wheeltec_lidar = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(launch_dir, 'wheeltec_lidar.launch.py')),
    )

    #slam_toolbox功能包中的async_slam_toolbox_node节点
    #parameters：指定SLAM的配置文件路径（mapper_params_online_async.yaml）
    #package：指定功能包名称（slam_toolbox）
    #executable：指定可执行文件名称（async_slam_toolbox_node）
    #name：指定节点名称（slam_toolbox）
    #output：将节点输出打印到终端（screen）
    #remappings：重映射话题名称（将odom重映射为odom_combined）
    slam_action=launch_ros.actions.Node(
        	parameters=[
        		get_package_share_directory("wheeltec_slam_toolbox") + '/config/mapper_params_online_async.yaml'
        	],
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            remappings=[('odom','odom_combined')]
        )
    return LaunchDescription([
        wheeltec_robot,wheeltec_lidar,
    slam_action
    ])
