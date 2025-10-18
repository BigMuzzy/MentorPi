from launch_ros.actions import Node
from launch import LaunchDescription, LaunchService
from launch.substitutions import LaunchConfiguration
from launch.actions import OpaqueFunction, DeclareLaunchArgument

def launch_setup(context, *args, **kwargs):
    # 配置参数
    mode = LaunchConfiguration('mode', default=1)
    enable_wakeup = LaunchConfiguration('enable_wakeup', default='true')
    awake_method = LaunchConfiguration('awake_method', default='xf')
    chinese_awake_words = LaunchConfiguration('chinese_awake_words', default='xiao3 huan4 xiao3 huan4')
    enable_setting = LaunchConfiguration('enable_setting', default='false')
    
    # 声明启动参数
    mode_arg = DeclareLaunchArgument('mode', default_value=mode)
    enable_wakeup_arg = DeclareLaunchArgument('enable_wakeup', default_value=enable_wakeup) 
    awake_method_arg = DeclareLaunchArgument('awake_method', default_value=awake_method)
    awake_words_arg = DeclareLaunchArgument('chinese_awake_words', default_value=chinese_awake_words)
    enable_setting_arg = DeclareLaunchArgument('enable_setting', default_value=enable_setting)

    # 配置 KWS 节点
    vocal_detect_node = Node(
        package='large_models',
        executable='vocal_detect',
        output='screen',
        parameters=[
            {
                "awake_method": awake_method,  # 唤醒方式
                "awake_word": chinese_awake_words,  # 唤醒关键词
                "enable_setting": enable_setting,  # 是否启用设置
                "enable_wakeup": enable_wakeup,  # 是否启用唤醒
                "mode": mode  # 模式
            }
        ]
    )

    return [
        mode_arg,
        enable_wakeup_arg,
        awake_method_arg,
        awake_words_arg,
        enable_setting_arg,
        vocal_detect_node,
    ]

def generate_launch_description():
    return LaunchDescription([
        OpaqueFunction(function=launch_setup)
    ])

if __name__ == '__main__':
    # 创建一个LaunchDescription对象
    ld = generate_launch_description()

    # 创建并运行 LaunchService
    ls = LaunchService()
    ls.include_launch_description(ld)
    ls.run()
