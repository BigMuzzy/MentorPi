# MentorPi Driver vs RRC Communication Protocol - Review Report

**Date:** 2026-02-21
**Scope:** `vendor/MentorPi/driver/` ROS packages reviewed against `.wiki/hiwonder/RRC_Communication_Protocol_Specification.md`
**Files reviewed:**
- `ros_robot_controller/ros_robot_controller/ros_robot_controller_sdk.py` (SDK / protocol layer)
- `ros_robot_controller/ros_robot_controller/ros_robot_controller_node.py` (ROS2 node)
- `ros_robot_controller_msgs/msg/*.msg` and `srv/*.srv` (message definitions)
- `controller/controller/mecanum.py` (chassis kinematics)
- `sdk/sdk/common.py` (utilities)

---

## Summary

| Severity | Count |
|----------|-------|
| Critical | 4     |
| Moderate | 2     |
| Minor    | 4     |
| Safety   | 3     |

---

## Critical Issues

### C1. Bus Servo Torque Enable/Disable Logic is Inverted

**File:** `ros_robot_controller_sdk.py:395-401`

The `bus_servo_enable_torque` method sends the wrong subcommand for the requested action.

**Current code:**
```python
def bus_servo_enable_torque(self, servo_id, enable):
    if enable:
        data = struct.pack("<BB", 0x0B, servo_id)  # 0x0B = Power OFF
    else:
        data = struct.pack("<BB", 0x0C, servo_id)  # 0x0C = Power ON
```

**Protocol spec (sections 4.5.5 and 4.5.6):**
- Subcommand `0x0B` = Motor Power **Off** (disable torque)
- Subcommand `0x0C` = Motor Power **On** (enable torque)

When `enable=True`, the code sends `0x0B` (power off), which is the opposite of the intended behavior.

**Suggested fix:**
```python
def bus_servo_enable_torque(self, servo_id, enable):
    if enable:
        data = struct.pack("<BB", 0x0C, servo_id)  # 0x0C = Power ON
    else:
        data = struct.pack("<BB", 0x0B, servo_id)  # 0x0B = Power OFF
    self.buf_write(PacketFunction.PACKET_FUNC_BUS_SERVO, data)
```

---

### C2. `enable_reception` Callback Overwrites Itself

**File:** `ros_robot_controller_node.py:114-117`

The subscription callback replaces itself with a boolean on first invocation:

```python
def enable_reception(self, msg):
    self.enable_reception = msg.data   # overwrites the method with a bool
    self.board.enable_reception(msg.data)
```

After the first message, `self.enable_reception` is a `bool`, not a callable. The topic subscription can never fire again. If `False` is sent, reception can never be re-enabled via the topic.

**Suggested fix:**
```python
def __init__(self, name):
    ...
    self._reception_enabled = False
    self.create_subscription(Bool, '~/enable_reception', self._enable_reception_cb, 1)
    ...

def _enable_reception_cb(self, msg):
    self.get_logger().info('enable_reception %s' % str(msg.data))
    self._reception_enabled = msg.data
    self.board.enable_reception(msg.data)
```
And update `pub_callback` to check `self._reception_enabled`.

---

### C3. `get_bus_servo_state` Calls Non-Existent SDK Methods

**File:** `ros_robot_controller_node.py:229, 249`

Two method calls reference names that do not exist in the `Board` class:

| Line | Code calls | Actual method name |
|------|-----------|-------------------|
| 229 | `self.board.bus_servo_read_voltage(i.id)` | `self.board.bus_servo_read_vin(i.id)` |
| 249 | `self.board.bus_servo_read_torque(i.id)` | `self.board.bus_servo_read_torque_state(i.id)` |

Both would raise `AttributeError` at runtime when voltage or torque state is requested.

**Suggested fix:**
```python
# Line 229
state = self.board.bus_servo_read_vin(i.id)

# Line 249
state = self.board.bus_servo_read_torque_state(i.id)
```

---

### C4. `get_pwm_servo_state` Has Wrong Service Handler Signature

**File:** `ros_robot_controller_node.py:151-164`

```python
def get_pwm_servo_state(self, msg):          # wrong: should be (self, request, response)
    states = []
    for i in msg.cmd:
        ...
    return [True, states]                     # wrong: should return response object
```

This is registered as a ROS2 service handler, but:
1. The method signature is `(self, msg)` instead of `(self, request, response)`
2. It returns `[True, states]` instead of populating and returning the `response` object

Compare with the working `get_bus_servo_state(self, request, response)` pattern.

**Suggested fix:**
```python
def get_pwm_servo_state(self, request, response):
    states = []
    for i in request.cmd:
        data = PWMServoState()
        if i.get_position:
            state = self.board.pwm_servo_read_position(i.id)
            if state is not None:
                data.position = [state]
        if i.get_offset:
            state = self.board.pwm_servo_read_offset(i.id)
            if state is not None:
                data.offset = [state]
        states.append(data)
    response.state = states
    response.success = True
    return response
```

---

## Moderate Issues

### M1. Motor ID Off-by-One (Potential)

**File:** `ros_robot_controller_sdk.py:342`

```python
def set_motor_speed(self, speeds):
    data = [0x01, len(speeds)]
    for i in speeds:
        data.extend(struct.pack("<Bf", int(i[0] - 1), float(i[1])))
```

The motor ID is decremented by 1 before being sent on the wire. The protocol spec examples (sections 4.3.1 and 4.3.2) use 1-based motor IDs (Motor 1 = `0x01`). This code would send Motor 1 as `0x00`.

No other device type (PWM servo, bus servo) applies this offset. This inconsistency is suspicious but may be an intentional firmware workaround. **Verify against actual hardware behavior before changing.**

**If this is a bug, the fix is:**
```python
data.extend(struct.pack("<Bf", int(i[0]), float(i[1])))
```

---

### M2. `pwm_servo_set_position` Includes Extra Count Byte Not in Spec

**File:** `ros_robot_controller_sdk.py:371-376`

```python
def pwm_servo_set_position(self, duration, positions):
    duration = int(duration * 1000)
    data = [0x01, duration & 0xFF, 0xFF & (duration >> 8), len(positions)]  # <-- len(positions) extra
    for i in positions:
        data.extend(struct.pack("<BH", i[0], i[1]))
```

The SDK packs: `subcommand(1) + duration(2) + count(1) + N*(id+pulse)` = **4 + 3N** bytes.

**Protocol spec (section 4.4.1):** Data Length = **3N + 3** (no count byte).
Spec example for 2 servos: `AA 55 04 09 01 D0 07 01 DC 05 02 C4 09 83` = 9 data bytes (3*2+3).

The SDK would produce 10 data bytes for the same 2-servo command. In contrast, `bus_servo_set_position` correctly includes a count byte because the bus servo spec (section 4.5.1) explicitly defines one (data length = 3N + 4).

**Note:** This may work if the firmware tolerates the extra byte. Verify against hardware before changing.

**If this is a bug, the fix is to remove `len(positions)`:**
```python
def pwm_servo_set_position(self, duration, positions):
    duration = int(duration * 1000)
    data = [0x01, duration & 0xFF, 0xFF & (duration >> 8)]
    for i in positions:
        data.extend(struct.pack("<BH", i[0], i[1]))
    self.buf_write(PacketFunction.PACKET_FUNC_PWM_SERVO, data)
```

---

## Minor Issues

### m1. Frame Format Comment is Wrong

**File:** `ros_robot_controller_sdk.py:13`

```python
# 0xAA 0x55 Length Function ID Data Checksum
```

The actual protocol and the state machine code use: `0xAA 0x55 Function Length Data Checksum`. There is no separate "ID" field; it is part of the data payload. The comment should be updated to match.

---

### m2. `bus_servo_set_temp_limit` Uses Signed Byte for Temperature

**File:** `ros_robot_controller_sdk.py:429`

```python
data = struct.pack("<BBb", 0x38, servo_id, int(limit))
```

The spec (section 4.5.16) defines the temperature threshold as `uint8` (unsigned, range 0-100). The code packs it as `b` (signed `int8`). For values 0-100 the wire representation is identical, but using `B` (unsigned) would be semantically correct.

---

### m3. `bus_servo_stop` Uses Undocumented Subcommand Under Bus Servo

**File:** `ros_robot_controller_sdk.py:433-436`

```python
def bus_servo_stop(self, servo_id):
    data = [0x03, len(servo_id)]
    data.extend(struct.pack("<"+'B'*len(servo_id), *servo_id))
    self.buf_write(PacketFunction.PACKET_FUNC_BUS_SERVO, data)
```

Subcommand `0x03` is not documented under the bus servo function (5) in the protocol spec. The spec documents `0x03` only under motor function (3) for "Stop Multiple Motors" with a bitmask format. This command sends to `PACKET_FUNC_BUS_SERVO` with a list-of-IDs format. This may be an undocumented firmware feature.

---

### m4. Protocol Spec Errors (Not Code Bugs)

Two errors found in the spec itself (`.wiki/hiwonder/RRC_Communication_Protocol_Specification.md`):

1. **Section 4.4.4 Example** (PWM Servo Deviation): Hex `AA 55 03 03 07 02 0A 53` uses function code `0x03` (MOTOR) instead of `0x04` (PWM_SERVO).
2. **Section 5.14** (PWM Servo Deviation Upload): Lists subcommand as `0x05` but the read deviation command (4.4.5) uses `0x09`. The response subcommand should be `0x09`.

---

## Verified Correct Implementations

The following protocol areas were reviewed and found correctly implemented:

| Area | SDK Method | Spec Section | Status |
|------|-----------|-------------|--------|
| Frame format (header, CRC) | `buf_write`, `recv_task` | 2 | Correct |
| Baud rate (1,000,000) | `Board.__init__` | 7 | Correct |
| LED control | `set_led` | 4.1 | Correct |
| Buzzer control | `set_buzzer` | 4.2 | Correct |
| Bus servo move | `bus_servo_set_position` | 4.5.1 | Correct |
| Bus servo set ID | `bus_servo_set_id` | 4.5.7 | Correct |
| Bus servo read ID | `bus_servo_read_id` (default 0xFE) | 4.5.8 | Correct |
| Bus servo set offset | `bus_servo_set_offset` | 4.5.9 | Correct |
| Bus servo save offset | `bus_servo_save_offset` | 4.5.11 | Correct |
| Bus servo set angle limit | `bus_servo_set_angle_limit` | 4.5.12 | Correct |
| Bus servo set voltage limit | `bus_servo_set_vin_limit` | 4.5.14 | Correct |
| PWM servo set offset | `pwm_servo_set_offset` | 4.4.4 | Correct |
| PWM servo read position | `pwm_servo_read_position` | 4.4.3 / 5.13 | Correct |
| PWM servo read offset | `pwm_servo_read_offset` | 4.4.5 / 5.14 | Correct |
| Bus servo read position | `bus_servo_read_position` | 4.5.2 / 5.1 | Correct |
| Bus servo read voltage | `bus_servo_read_vin` | 4.5.3 / 5.2 | Correct |
| Bus servo read temperature | `bus_servo_read_temp` | 4.5.4 / 5.3 | Correct |
| Bus servo read angle limit | `bus_servo_read_angle_limit` | 4.5.13 / 5.6 | Correct |
| Bus servo read voltage limit | `bus_servo_read_vin_limit` | 4.5.15 / 5.7 | Correct |
| Bus servo read temp limit | `bus_servo_read_temp_limit` | 4.5.17 / 5.8 | Correct |
| IMU data parsing | `get_imu` (`<6f` = 24 bytes) | 5.10 | Correct |
| Gamepad data parsing | `get_gamepad` (`<HB4b` = 7 bytes) | 5.11 | Correct |
| SBUS data parsing | `get_sbus` (`<16hBBBB` = 36 bytes) | 5.12 | Correct |
| Button event parsing | `get_button` / `packet_report_key` | 5.9 | Correct |
| CRC-8 checksum | `checksum_crc8` (table lookup) | 2 | Correct |
| Little-endian byte order | All `struct.pack("<...")` calls | 7 | Correct |
| Function code enum values | `PacketFunction` (0-12) | 3 | Correct |

---

## Recommendations

1. **Fix C1-C4 immediately** - these are runtime bugs that cause incorrect hardware behavior or `AttributeError` crashes.
2. **Verify M1 and M2 against hardware** - the motor ID offset and PWM servo count byte may be intentional firmware accommodations. Test with the actual board before changing.
3. **Update the protocol spec** - fix the two documentation errors identified in m4.
4. **Add integration tests** - the service handler bugs (C3, C4) indicate that `get_bus_servo_state` and `get_pwm_servo_state` have never been exercised end-to-end.

---

## Safety Issues (Added after live diagnostics)

### S1. No Thread Safety on Serial Port Writes (Race Condition)

**File:** `ros_robot_controller_sdk.py:320` (`buf_write`)

The `buf_write` method writes frames to the serial port without any locking. Multiple ROS callbacks (`set_motor_state`, `set_pwm_servo_state`, etc.) can invoke `buf_write` concurrently from different threads, causing interleaved byte sequences on the wire. The board's UART parser receives a corrupt frame and can enter an undefined state where it stops processing input entirely — motors keep running at last commanded speed, and no data (IMU, battery, etc.) comes back.

**Observed symptom:** Robot stuck executing last motor command. Live diagnostics confirmed:
- `/controller/cmd_vel` flowing at 10Hz with zero velocities
- `/ros_robot_controller/set_motor` publishing zero-speed commands
- `/ros_robot_controller/imu_raw` completely silent (no data from board)

**Fix applied:** Added `write_lock` (threading.Lock) to `buf_write`, acquired before `port.write()`.

---

### S2. No Board Health Monitoring or UART Recovery

**File:** `ros_robot_controller_node.py`

There was no mechanism to detect when the board stops responding. The serial port could stall indefinitely with no recovery path — the only fix was to physically power-cycle the robot.

The RRC protocol has no documented reset or ping command (`PACKET_FUNC_SYS` is only used for battery voltage reporting).

**Fix applied:**
- Added `reset_port()` method to `Board` class: closes and reopens the serial port, resets the parser state machine
- Added `_board_health_check` timer (1Hz) to `RosRobotController` node: monitors `imu_last_recv_time`, triggers port reset + motor stop if IMU data absent for >2 seconds
- `recv_task` updated to catch `SerialException`/`OSError` during port reset (prevents thread crash)
- Recovery logged via ROS logger; `board_health_timeout` configurable via parameter

---

### S3. Ackermann Steering Bugs (Wheels Not Centering, Wrong Direction)

**Files:** `controller/controller/ackermann.py`, `controller/controller/odom_publisher_node.py`

Two steering bugs discovered through on-robot testing:

1. **Wheels not returning to center on joystick release:** `ackermann.set_velocity()` returned `servo_angle=None` when `linear_speed=0`, and the `cmd_vel_callback` else branch (angular_z==0) did not publish any servo command. Result: steering servo held last angle indefinitely.

2. **Both left and right steering resulted in left turn:** The steering angle clamp `steering_angle = math.radians(45)` always produced a positive value regardless of input sign, losing the direction information.

**Fixes applied:**
- `ackermann.py`: Changed `return None, msg` to `return servo_angle, msg` (servo_angle initialized to 1500 = center). Added `math.copysign` to preserve sign during clamping.
- `odom_publisher_node.py`: Added servo publish in the `angular_z==0` branch. Added `cmd_vel_watchdog` timer (0.5s timeout) that stops motors and centers steering if no commands received.
