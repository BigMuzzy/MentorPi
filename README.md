# MentorPi T1

English | [中文](https://github.com/Hiwonder/MentorPi/blob/MentorPi-T1/README_cn.md)

<p align="center">
  <img src="./sources/images/image.webp" alt="MentorPi T1 Logo" width="400"/>
</p>

## Product Overview

**MentorPi: Bridging Theory and Practice in Robotics Learning**

MentorPi is designed to close the gap between robotics theory and hands-on experimentation. As a versatile platform built for academic and research environments, it combines cutting-edge AI capabilities with the full power of the ROS 2 framework—giving students a tangible, programmable system for learning, and researchers a reliable platform for rapidly testing and deploying algorithms.

**Adaptable, Intelligent, and Open**

Built with adaptability and intelligence in mind, MentorPi supports Ackermann chassis and Mecanum wheels, enabling operation across diverse terrains and scenarios. Equipped with high-precision LiDAR, 3D depth cameras, closed-loop encoder motors, and other high-performance hardwares, the platform is capable of executing advanced AI tasks such as SLAM-based mapping and navigation, real-time object tracking, and vision-based perception using models like YOLOv11.

**Ready for the Next Frontier in AI Robotics?**

To support cutting-edge research, MentorPi integrates multimodal AI large language models, opening doors to embodied AI and human robot interaction. As an open source platform, MentorPi offers full control and customization, enabling you to modify, extend, and innovate freely.

Explore our MentorPi tutorials to see how you can elevate your AI and robotics projects with a platform built to grow with your ideas.

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
- **Vision Recognition** - Advanced computer vision capabilities

### Intelligent Control
- **Multi-Chassis Design** - Support for three configurations: Mecanum wheels, Ackermann, and tank tracks
- **Closed-loop Motor Control** - High-precision encoder feedback control
- **Large-torque Servos** - High-power servo systems for heavy-duty operations
- **Multi-sensor Fusion** - Integrated sensor data processing

### Programming Interface
- **ROS2 Integration** - Full Robot Operating System 2 support
- **Python Programming** - Comprehensive Python SDK
- **Multimodal AI Model** - Advanced embodied AI capabilities
- **Open Source** - Complete open-source platform for customization

## Hardware Configuration
- **Processor**: Raspberry Pi 5
- **Operating System**: ROS2 compatible Linux
- **Motors**: High-speed closed-loop encoder motors
- **Vision System**: 3D depth camera + Lidar sensor
- **Actuators**: Large-torque servos
- **Chassis**: Supports three chassis configurations: Mecanum wheels, Ackermann, and tank tracks

## Project Structure

```
mentorpi/
├── app/                    # Application modules
├── bringup/               # System startup and configuration
├── driver/                # Hardware drivers
├── example/               # Example applications and demos
├── interfaces/            # ROS2 message definitions
├── large_models/          # AI large model integration
├── large_models_msgs/     # Large model message definitions
├── peripherals/           # Peripheral device support
└── yolov5_ros2/          # YOLOv5 ROS2 integration
```

## Version Information
- **Current Version**: MentorPi T1 v1.0.0
- **Supported Platform**: Raspberry Pi 5

### Related Technologies
- [ROS2](https://ros.org/) - Robot Operating System 2
- [OpenCV](https://opencv.org/) - Computer Vision Library
- [YOLOv5](https://github.com/ultralytics/yolov5) - Object Detection Framework

---

**Note**: This program is pre-installed on the MentorPi T1 robot system and can be run directly. For detailed tutorials, please refer to the [Official Documentation](https://docs.hiwonder.com/projects/MentorPi/en/latest/).