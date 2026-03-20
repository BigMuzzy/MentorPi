#!/usr/bin/python3
# coding=utf8
# Ackermann wheel chassis kinematics
import math
from ros_robot_controller_msgs.msg import MotorState, MotorsState


class AckermannChassis:
    def __init__(self, wheelbase=0.145, track_width=0.133, wheel_diameter=0.067):
        self.wheelbase = wheelbase        # L: front-to-rear axle distance [m]
        self.track_width = track_width    # W: left-to-right wheel centre distance [m]
        self.wheel_diameter = wheel_diameter

    def speed_covert(self, speed):
        """Convert linear speed [m/s] to wheel rotation rate [rps]."""
        return speed / (math.pi * self.wheel_diameter)

    def set_velocity(self, linear_speed, angular_speed, reset_servo=True):
        """
        Compute Ackermann steering and rear-wheel differential from velocity command.

        linear_speed  [m/s]    : forward speed; negative = reverse
        angular_speed [rad/s]  : CCW positive (ROS convention); left turn = positive

        Motor layout (from hardware):
            front:  motor 1 (left, unpowered)   motor 3 (right, unpowered)
            rear:   motor 2 (right)              motor 4 (left)
        Sign convention:
            motor 2 (right rear): positive rps = forward
            motor 4 (left  rear): negative rps = forward

        Returns (servo_angle, MotorsState):
            servo_angle  : PWM pulse width [μs]; 1500 = straight, range 1000–2000
            MotorsState  : motor speeds for all four motor IDs
        """
        servo_angle = 1500  # neutral / straight ahead
        motor_speeds = [0.0, 0.0, 0.0, 0.0]

        if abs(linear_speed) >= 1e-8:
            # --- Steering angle ---
            # Turn radius (rear axle centre): R = v / ω
            # Front-wheel steer angle:        θ = atan(L / R) = atan(L·ω / v)
            # Using abs(v) keeps steering direction stable during reverse.
            if abs(angular_speed) >= 1e-8:
                steering_angle = math.atan(
                    self.wheelbase * angular_speed / abs(linear_speed)
                )
                # Clamp to mechanical limit while preserving sign
                max_angle = math.radians(45)
                if abs(steering_angle) > max_angle:
                    steering_angle = math.copysign(max_angle, steering_angle)
            else:
                steering_angle = 0.0

            # Map steering angle to servo pulse width
            # ±90° spans the full 1000–2000 μs range (gain = 2000/180)
            servo_angle = 1500 + 2000 * math.degrees(steering_angle) / 180

            # --- Rear-wheel differential ---
            # Each rear wheel travels its own arc at radius R ± W/2:
            #   v_right = ω · (R + W/2) = v + ω·W/2   (outer for left turn going forward)
            #   v_left  = ω · (R − W/2) = v − ω·W/2   (inner for left turn going forward)
            # When reversing, the centre of curvature flips side relative to the car body,
            # so the differential contribution is negated (multiply by sign of linear_speed).
            sign = math.copysign(1.0, linear_speed)
            v_right = linear_speed + sign * angular_speed * self.track_width / 2
            v_left  = linear_speed - sign * angular_speed * self.track_width / 2

            motor_speeds = [
                0.0,                            # motor 1: front-left  (unpowered)
                self.speed_covert(v_right),     # motor 2: right rear  (+rps = fwd)
                0.0,                            # motor 3: front-right (unpowered)
                -self.speed_covert(v_left),     # motor 4: left rear   (-rps = fwd)
            ]

        data = []
        for i, rps in enumerate(motor_speeds):
            msg = MotorState()
            msg.id = i + 1
            msg.rps = float(rps)
            data.append(msg)

        msg = MotorsState()
        msg.data = data
        return servo_angle, msg
