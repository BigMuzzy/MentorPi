# MentorPi M1

[English](https://github.com/Hiwonder/MentorPi/blob/MentorPi-M1/README.md) | 中文

<p align="center">
  <img src="./sources/images/image.webp" alt="MentorPi M1 Logo" width="400"/>
</p>

## 产品介绍

MentorPi是一款基于树莓派5开发的ROS2机器人小车，它支持麦克纳姆轮、阿克曼和履带三种底盘配置。它的机身搭载了高速闭环编码电机、高精度激光雷达、3D深度相机、大扭矩舵机、赛事级轮胎等高性能硬件，可以轻松实现SLAM建图导航、路径规划、视觉识别、目标追踪、MediaPipe人机交互等高阶AI功能。通过机器学习YOLO v5模型，MentorPi还能实现路标识别、红绿灯识别等自动驾驶场景功能。

MentorPi还部署了多模态AI大模型，能够在线调用OpenAI的API接口，可以更好地理解环境、规划行动并执行任务，实现更多高阶具身智能应用。

## 主要功能

### AI视觉与导航
- **SLAM建图** - 实时同步定位与建图
- **路径规划** - 智能路线规划和导航
- **自动驾驶** - 具备避障功能的自动驾驶能力
- **YOLOv5识别** - 先进的路标和交通信号灯目标检测
- **3D深度感知** - 深度相机集成的立体视觉

### 智能控制
- **模块化底盘设计** - 支持麦克纳姆轮、阿克曼和履带三种底盘配置
- **闭环电机控制** - 高精度编码器反馈控制
- **舵机控制** - 高扭矩舵机系统精确运动
- **多传感器融合** - 集成传感器数据处理

### 编程接口
- **ROS2集成** - 完整的机器人操作系统2支持
- **Python编程** - 全面的Python SDK
- **多模态AI模型** - 先进的具身AI能力
- **机器学习** - YOLOv5训练和推理支持

## 硬件配置
- **处理器**: 树莓派5
- **操作系统**: ROS2兼容Linux系统
- **电机**: 高速闭环编码器电机
- **视觉系统**: 3D深度相机 + 激光雷达传感器
- **执行器**: 高扭矩舵机
- **底盘**: 支持麦克纳姆轮、阿克曼和履带三种底盘配置

## 项目结构

```
mentorpi/
├── app/                    # 应用模块
├── bringup/               # 系统启动和配置
├── calibration/           # 传感器标定工具
├── driver/                # 硬件驱动
├── example/               # 示例应用和演示
├── interfaces/            # ROS2消息定义
├── large_models/          # AI大模型集成
├── multi/                 # 多机器人协调
├── navigation/            # 导航系统
├── peripherals/           # 外设支持
├── simulations/           # 仿真环境
├── slam/                  # SLAM算法
└── yolov5_ros2/          # YOLOv5 ROS2集成
```

## 官方资源

### Hiwonder官方
- **官方网站**: [https://www.hiwonder.net/](https://www.hiwonder.net/)
- **产品页面**: [https://www.hiwonder.com/products/mentorpi](https://www.hiwonder.com/products/mentorpi)
- **官方文档**: [https://docs.hiwonder.com/projects/MentorPi/en/latest/](https://docs.hiwonder.com/projects/MentorPi/en/latest/)
- **技术支持**: support@hiwonder.com

### 相关技术
- [ROS2](https://ros.org/) - 机器人操作系统2
- [OpenCV](https://opencv.org/) - 计算机视觉库
- [YOLOv5](https://github.com/ultralytics/yolov5) - 目标检测框架

## 版本信息
- **当前版本**: MentorPi M1 v1.0.0
- **支持平台**: 树莓派5

---

**注**: 所有程序已预装在MentorPi M1机器人系统中，可直接运行。详细使用教程请参考[官方文档](https://docs.hiwonder.com/projects/MentorPi/en/latest/)。