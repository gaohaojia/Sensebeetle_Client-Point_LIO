from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription, LaunchContext
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


def declare_cfg_dir(context: LaunchContext, point_lio_dir, lidar_type):
    lidar_type_str = context.perform_substitution(lidar_type)
    return [DeclareLaunchArgument(
        "point_lio_cfg_dir",
        default_value=PathJoinSubstitution(
            [point_lio_dir, "config", lidar_type_str + ".yaml"]
        ),
        description="Path to the Point-LIO config file",
    )]


def generate_launch_description():
    lidar_type = LaunchConfiguration("lidar_type")

    use_rviz = LaunchConfiguration("rviz")
    point_lio_cfg_dir = LaunchConfiguration("point_lio_cfg_dir")

    point_lio_dir = get_package_share_directory("point_lio")

    declare_lidar_type = DeclareLaunchArgument(
        "lidar_type",
        default_value="mid360",
        description="Type of LIDAR used for mapping.",
    )

    declare_rviz = DeclareLaunchArgument(
        "rviz", default_value="False", description="Flag to launch RViz."
    )

    start_point_lio_node = Node(
        package="point_lio",
        executable="pointlio_mapping",
        parameters=[point_lio_cfg_dir],
        output="screen",
    )

    start_rviz_node = Node(
        condition=IfCondition(use_rviz),
        package="rviz2",
        executable="rviz2",
        name="rviz",
        arguments=[
            "-d",
            PathJoinSubstitution([point_lio_dir, "rviz_cfg", "loam_livox"]),
            ".rviz",
        ],
    )

    ld = LaunchDescription()

    ld.add_action(declare_rviz)
    ld.add_action(declare_lidar_type)
    ld.add_action(
        OpaqueFunction(function=declare_cfg_dir, args=[point_lio_dir, lidar_type])
    )
    ld.add_action(start_point_lio_node)
    ld.add_action(start_rviz_node)

    return ld
