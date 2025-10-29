# MentorPi M1

English | [中文](https://github.com/Hiwonder/MentorPi/blob/MentorPi-M1/README_cn.md)

<p align="center">
  <img src="./sources/images/image.webp" alt="MentorPi M1 Logo" width="400"/>
</p>

## Product Overview

Our vision for MentorPi is straightforward: as AI technology continues to advance, we aim to create a cost-effective educational robotics platform that combines the latest AI large language models with ROS 2, enabling AI enthusiasts, students, developers, and innovators to easily learn advanced AI robotics technology and build exciting AI-driven creative projects.

MentorPi features robust hardware configuration, powered by an STM32 controller combined with Raspberry Pi 5 as the control system, offering three chassis options to choose from—Mecanum wheels, Ackermann steering, and tank treads—allowing you to select the chassis that best suits your needs.

MentorPi's compact body integrates high-speed encoder motors, LiDAR, 3D depth cameras, AI voice modules, and other high-performance hardware that enables complex AI behaviors, including SLAM-based navigation, real-time object tracking, and even traffic sign recognition using YOLOv11 for autonomous driving capabilities.

As an open-source platform, MentorPi encourages customization and extension. This year, we not only launched multi-chassis support but also deployed multimodal AI large language models with natural voice interaction capabilities, enabling robots to perform more complex embodied AI tasks.

Whether you're building autonomous driving projects or exploring human-robot interaction, we welcome you to join our community and help shape the future of MentorPi. Additionally, you can check out the MentorPi tutorials to get started quickly!

## Official Resources

### Official Hiwonder
- **Official Website**: [https://www.hiwonder.net/](https://www.hiwonder.net/)
- **Product Page**: [https://www.hiwonder.com/products/mentorpi](https://www.hiwonder.com/products/mentorpi)
- **Official Documentation**: [https://docs.hiwonder.com/projects/MentorPi/en/latest/](https://docs.hiwonder.com/projects/MentorPi/en/latest/)
- **Technical Support**: support@hiwonder.com

## Key Features

### AI Vision & Navigation
- **SLAM Mapping** - Real-time simultaneous localization and mapping
- **Path Planning** - Intelligent route planning and navigation
- **Autonomous Driving** - Self-driving capabilities with obstacle avoidance
- **YOLOv5 Recognition** - Advanced object detection for road signs and traffic lights
- **3D Depth Perception** - Stereo vision with depth camera integration

### Intelligent Control
- **Modular Chassis Design** - Support for three chassis configurations: Mecanum wheels, Ackermann, and tank tracks
- **Closed-loop Motor Control** - High-precision encoder feedback control
- **Servo Control** - High-torque servo systems for precise movements
- **Multi-sensor Fusion** - Integrated sensor data processing

### Programming Interface
- **ROS2 Integration** - Full Robot Operating System 2 support
- **Python Programming** - Comprehensive Python SDK
- **Multimodal AI Model** - Advanced embodied AI capabilities
- **Machine Learning** - YOLOv5 training and inference support

## Hardware Configuration
- **Processor**: Raspberry Pi 5
- **Operating System**: ROS2 compatible Linux
- **Motors**: High-speed closed-loop encoder motors
- **Vision System**: 3D depth camera + Lidar sensor
- **Actuators**: High-torque servos
- **Chassis**: Supports three chassis configurations: Mecanum wheels, Ackermann, and tank tracks

## Project Structure

```
mentorpi/
├── app/                    # Application modules
├── bringup/               # System startup and configuration
├── calibration/           # Sensor calibration utilities
├── driver/                # Hardware drivers
├── example/               # Example applications and demos
├── interfaces/            # ROS2 message definitions
├── large_models/          # AI large model integration
├── multi/                 # Multi-robot coordination
├── navigation/            # Navigation stack
├── peripherals/           # Peripheral device support
├── simulations/           # Simulation environments
├── slam/                  # SLAM algorithms
└── yolov5_ros2/          # YOLOv5 ROS2 integration
```

## Version Information
- **Current Version**: MentorPi M1 v1.0.0
- **Supported Platform**: Raspberry Pi 5

### Related Technologies
- [ROS2](https://ros.org/) - Robot Operating System 2
- [OpenCV](https://opencv.org/) - Computer Vision Library
- [YOLOv5](https://github.com/ultralytics/yolov5) - Object Detection Framework

---

**Note**: This program is pre-installed on the MentorPi M1 robot system and can be run directly. For detailed tutorials, please refer to the [Official Documentation](https://docs.hiwonder.com/projects/MentorPi/en/latest/).