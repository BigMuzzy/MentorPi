# MentorPi T1

English | [中文](https://github.com/Hiwonder/MentorPi/blob/MentorPi-T1/README_cn.md)

<p align="center">
  <img src="./sources/images/image.webp" alt="MentorPi T1 Logo" width="400"/>
</p>

## Product Overview

MentorPi is a ROS2 robot car based on Raspberry Pi 5 that supports three chassis configurations: Mecanum wheels, Ackermann, and tank tracks. It is equipped with high-performance hardware including high-speed closed-loop encoder motors, high-precision LiDAR, 3D depth cameras, high-torque servos, and racing-grade tires, enabling advanced AI functions such as SLAM mapping and navigation, path planning, vision recognition, target tracking, and MediaPipe human-machine interaction. Through machine learning with YOLO v5 models, MentorPi can achieve autonomous driving scenario functions such as road sign recognition and traffic light recognition.

MentorPi also deploys multimodal AI large models that can call OpenAI API interfaces online, allowing better environmental understanding, action planning, and task execution to achieve more advanced embodied intelligence applications.

## Key Features

### AI Vision & Navigation
- **SLAM Mapping** - Real-time simultaneous localization and mapping
- **Path Planning** - Intelligent route planning and navigation
- **Autonomous Driving** - Self-driving capabilities with obstacle avoidance
- **YOLOv5 Recognition** - Advanced object detection for road signs and traffic lights
- **Vision Recognition** - Advanced computer vision capabilities

### Intelligent Control
- **Tank Chassis** - Robust tracked vehicle design for all-terrain navigation
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
- **Chassis**: Tank chassis with tracked wheels for enhanced mobility

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
- **Current Version**: MentorPi T1 v1.0.0
- **Supported Platform**: Raspberry Pi 5

---

**Note**: This program is pre-installed on the MentorPi T1 robot system and can be run directly. For detailed tutorials, please refer to the [Official Documentation](https://docs.hiwonder.com/projects/MentorPi/en/latest/).