# MentorPi A1

English | [中文](https://github.com/Hiwonder/MentorPi/blob/MentorPi-A1/README_cn.md)

<p align="center">
  <img src="./sources/images/image.webp" alt="MentorPi A1 Logo" width="400"/>
</p>

## Product Overview

MentorPi A1 ROS robot is a smart robot car powered by Raspberry Pi 5 and ROS2. It is engineered for high performance with closed-loop encoder motors, a Lidar sensor, a 3D depth camera, and powerful servos. Masters advanced functions like SLAM mapping, path planning, and autonomous driving—with YOLOv5 training to recognize road signs and traffic lights.

Enhanced by a Multimodal AI large language model, Hiwonder MentorPi car robot is ready for next-gen embodied AI. Tutorials and videos are provided to help you launch your AI projects with confidence.

## Key Features

### AI Vision & Navigation
- **SLAM Mapping** - Real-time simultaneous localization and mapping
- **Path Planning** - Intelligent route planning and navigation
- **Autonomous Driving** - Self-driving capabilities with obstacle avoidance
- **YOLOv5 Recognition** - Advanced object detection for road signs and traffic lights
- **3D Depth Perception** - Stereo vision with depth camera integration

### Intelligent Control
- **Closed-loop Motor Control** - High-precision encoder feedback control
- **Lidar Navigation** - 360-degree laser scanning for mapping and navigation
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
- **Chassis**: Professional robotic platform with Ackermann steering

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

## Official Resources

### Official Hiwonder
- **Official Website**: [https://www.hiwonder.net/](https://www.hiwonder.net/)
- **Product Page**: [https://www.hiwonder.com/products/mentorpi](https://www.hiwonder.com/products/mentorpi)
- **Official Documentation**: [https://docs.hiwonder.com/projects/MentorPi/en/latest/](https://docs.hiwonder.com/projects/MentorPi/en/latest/)
- **Technical Support**: support@hiwonder.com

### Related Technologies
- [ROS2](https://ros.org/) - Robot Operating System 2
- [OpenCV](https://opencv.org/) - Computer Vision Library
- [YOLOv5](https://github.com/ultralytics/yolov5) - Object Detection Framework

## Version Information
- **Current Version**: MentorPi A1 v1.0.0
- **Supported Platform**: Raspberry Pi 5

---

**Note**: This program is pre-installed on the MentorPi A1 robot system and can be run directly. For detailed tutorials, please refer to the [Official Documentation](https://docs.hiwonder.com/projects/MentorPi/en/latest/).