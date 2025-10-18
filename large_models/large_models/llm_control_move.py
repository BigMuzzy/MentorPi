#!/usr/bin/env python3
# encoding: utf-8
# @Author: Aiden
# @Date: 2025/03/06
import time
import rclpy
import threading
import json  # 导入 json 模块，用于安全地解析 JSON 字符串
from speech import speech
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String, Bool
from std_srvs.srv import Trigger, SetBool, Empty

from large_models.config import *
from large_models_msgs.srv import SetModel, SetString, SetInt32
from ros_robot_controller_msgs.msg import SetPWMServoState, PWMServoState 

from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

PROMPT_mecanum = '''
#角色任务
你是一辆智能小车，可以通过 x 方向和 y 方向控制线速度,单位m/s，并通过 z 方向控制角速度,单位rad/s，t控制时间单位s。需要根据输入的内容，生成对应的指令。

 ##要求与限制
1.确保速度范围正确：
线速度：x, y ∈ [-1.0, 1.0]（负值表示反方向）
角速度：z ∈ [-1.0, 1.0]（逆时针为负，顺时针为正）
2.顺序执行多个动作，输出一个 包含多个移动指令的 action 列表，仅在最后一个动作后添加 [0.0, 0.0, 0.0, 0.0] 以确保小车停止。
3.x和y默认为0.2, z默认为1, t默认为1。 
4.为每个动作序列编织一句精炼（5至10字）、风趣且变化无穷的反馈信息，让交流过程妙趣横生。
5.直接输出json结果，不要分析，不要输出多余内容。
6.格式：{  
  "action": [["x1", "y1", "z1", "t1"], ["x2", "y2", "z2", "t2"], ..., ["0", "0", "0", "0"]],  
  "response": "xx"  
}  

##结构要求##：
 - `"action"`键下承载一个按执行顺序排列的函数名称字符串数组，当找不到对应动作函数时action输出[]。 
- `"response"`键则配以精心构思的简短回复，完美贴合上述字数与风格要求。 

## 实施原则 - 在最终输出前，实施全面校验，确保回复不仅格式合规，而且内容充满意趣，无一遗漏上述规范。

## 任务示例
输入: 往前走一秒，然后后退一秒，顺时针旋转一圈，停止运动，然后漂移，最后逆时针旋转180度。
输出: {"action":[[0.2, 0.0, 0.0, 1.0], [-0.2, 0.0, 0.0, 1.0], [0.0, 0.0, 1.0, 6.28], [0.0, 0.0, 0.0, 0.0], [0.2, 0.2, -1.0, 1.0], [0.0, 0.0, -1.0, 3.14], [0.0, 0.0, 0.0, 0.0]],"response": "前进后退转圈漂移，最后潇洒"}
输入: 漂移
输出: {"action": [[0.2, 0.2, 1.0, 1.0], [0.0, 0.0, 0.0, 0.0]], "response": "漂移登场，帅到掉渣`"}
输入：向前移动 2 秒，然后顺时针旋转 1 秒
输出：{"action": [[0.2, 0.0, 0.0, 2.0], [0.0, 0.0, 1.0, 1.0],[0,0, 0.0, 0.0, 0.0]], "response": "前进 2 秒，然后顺时针旋转 1 秒，出发！"}
输入：向前走1米
输出：{"action": [[0.2, 0.0, 0.0, 2.0], [0.0, 0.0, 0.0, 0.0]], "response": "好嘞"}
'''
PROMPT_ackerman = '''
# 角色任务
你是一辆智能阿克曼小车，可以通过 x 方向控制线速度（单位：米/秒），通过 z 方向控制角速度（单位：弧度/秒），t 控制时间（单位：秒）。需要根据输入的内容，生成对应的指令。

## 要求与限制
1. 速度范围：
   - 线速度 x ∈ [-0.5, 0.5]（负值表示反方向）
   - 角速度 z ∈ [-1.0, 1.0]（右转为负，左转为正）
2. 动作序列：
   - 顺序执行多个动作，输出一个包含多个移动指令的 action 列表。
   - 必须在每一个动作后添加 [0.0, 0.0, 0.0, 0.0] 以确保小车停止。
3. 默认值：
   - x 默认为 0.14913351833820343, z 默认为 0.5696415155040463, t 默认为 2。
4. 反馈信息：
   - 为每个动作序列编织一句精炼（5至10字）、风趣且变化无穷的反馈信息。
5. 输出格式：
   - JSON 格式，不要分析，不要输出多余内容。
   - {
       "action": [["x1", "y1", "z1", "t1"], ["x2", "y2", "z2", "t2"], ..., ["0", "0", "0", "0"]],
       "response": "xx"
     }

## 结构要求
- "action" 键下承载一个按执行顺序排列的函数名称字符串数组。 如果找不到对应动作函数，则 action 输出 []。
- "response" 键则配以精心构思的简短回复。

## 实施原则
- 在最终输出前，实施全面校验，确保回复不仅格式合规，而且内容充满意趣，无一遗漏上述规范。

## 任务示例

输入：向前走 1 米
输出：{"action": [["0.5", "0.0", "0.0", "2.0"], ["0.0", "0.0", "0.0", "0.0"]], "response": "好嘞，这就出发！"}

输入：左转
输出: {"action": [["0.14913351833820343", "0.0", "0.5696415155040463", "2.0"], ["0.0", "0.0", "0.0", "0.0"]], "response": "向左转弯！"}

输入: 右转
输出: {"action": [["0.14913351833820343", "0.0", "-0.5696415155040463", "2.0"], ["0.0", "0.0", "0.0", "0.0"]], "response": "向右转弯！"}
输入：向前走 1 米,左转1秒,右转1秒
输出：{"action": [["0.5", "0.0", "0.0", "2.0"], ["0.0", "0.0", "0.0", "0.0"],["0.14913351833820343", "0.0", "0.5696415155040463", "2.0"],["0.0", "0.0", "0.0", "0.0"],["0.14913351833820343", "0.0", "-0.5696415155040463", "2.0"], ["0.0", "0.0", "0.0", "0.0"]], "response": "好嘞，这就出发！"}

'''


PROMPT_map = {
    "MentorPi_Acker": PROMPT_ackerman,
    "MentorPi_Mecanum": PROMPT_mecanum,
}

class LLMControlMove(Node):
    def __init__(self, name):
        rclpy.init()
        super().__init__(name)
        
        self.action = []
        self.llm_result = ''
        self.running = True
        self.action_finish = False
        self.play_audio_finish = False
        
        timer_cb_group = ReentrantCallbackGroup()
        self.tts_text_pub = self.create_publisher(String, 'tts_node/tts_text', 1)
        self.create_subscription(String, 'agent_process/result', self.llm_result_callback, 1)
        self.create_subscription(Bool, 'tts_node/play_finish', self.play_audio_finish_callback, 1, callback_group=timer_cb_group)
        self.set_model_client = self.create_client(SetModel, 'agent_process/set_model')
        self.set_model_client.wait_for_service()

        self.awake_client = self.create_client(SetBool, 'vocal_detect/enable_wakeup')
        self.awake_client.wait_for_service()
        self.set_mode_client = self.create_client(SetInt32, 'vocal_detect/set_mode')
        self.set_mode_client.wait_for_service()
        self.set_prompt_client = self.create_client(SetString, 'agent_process/set_prompt')
        self.set_prompt_client.wait_for_service()
        self.mecanum_pub = self.create_publisher(Twist, '/controller/cmd_vel', 1)
        self.servo_state_pub = self.create_publisher(SetPWMServoState, 'ros_robot_controller/pwm_servo/set_state', 10) 

        self.declare_parameter('machine_type', 'default_machine')

        self.machine_type = self.get_parameter('machine_type').get_parameter_value().string_value

        self.get_logger().info(f"machine_type in __init__: {self.machine_type}")  # 添加这行代码
        self.timer = self.create_timer(0.0, self.init_process, callback_group=timer_cb_group)

    def get_node_state(self, request, response):
        return response

    def init_process(self):
        self.timer.cancel()

        msg = SetModel.Request()
        msg.model = llm_model
        msg.model_type = 'llm'
        msg.api_key = api_key
        msg.base_url = base_url
        self.send_request(self.set_model_client, msg)

        self.get_logger().info(f"machine_type in init_process: {self.machine_type}") 

        # 选择prompt
        if self.machine_type == 'MentorPi_Acker':
            prompt_to_use = PROMPT_ackerman
            self.get_logger().info("Using PROMPT_ackerman")  
        elif self.machine_type == 'MentorPi_Mecanum':
            prompt_to_use = PROMPT_mecanum
            self.get_logger().info("Using PROMPT_mecanum")
        else:
            prompt_to_use = PROMPT_mecanum
            self.get_logger().info("Using default PROMPT_mecanum") 

        self.get_logger().info(f"Sending prompt to agent_process/set_prompt: {prompt_to_use}")  

        msg = SetString.Request()
        msg.data = prompt_to_use
        self.send_request(self.set_prompt_client, msg)

        speech.play_audio(start_audio_path)
        threading.Thread(target=self.process, daemon=True).start()
        self.create_service(Empty, '~/init_finish', self.get_node_state)
        self.get_logger().info('\033[1;32m%s\033[0m' % 'start')

    def send_request(self, client, msg):
        future = client.call_async(msg)
        while rclpy.ok():
            if future.done() and future.result():
                return future.result()

    def llm_result_callback(self, msg):
        self.llm_result = msg.data

    def play_audio_finish_callback(self, msg):
        self.play_audio_finish = msg.data

    def process(self):
        while self.running:
            if self.llm_result:
                msg = String()
                if 'action' in self.llm_result:  #
                    try:
                        result = json.loads(self.llm_result[self.llm_result.find('{'):self.llm_result.rfind('}') + 1]) 
                    except json.JSONDecodeError as e:
                        self.get_logger().error(f"JSONDecodeError: {e}")
                        self.llm_result = ''
                        continue

                    self.get_logger().info(str(result))
                    action_list = []
                    if 'action' in result:
                        action_list = result['action']
                        self.get_logger().info(f"Extracted action_list: {action_list}")  
                    if 'response' in result:
                        response = result['response']
                        self.get_logger().info(f"Extracted response: {response}")  
                    msg.data = response
                    self.tts_text_pub.publish(msg)
                    for i in action_list:
                        twist_msg = Twist()
                        twist_msg.linear.x = float(i[0])
                        twist_msg.linear.y = float(i[1])
                        twist_msg.angular.z = float(i[2])
                        self.mecanum_pub.publish(twist_msg)

                        #  舵机回中 #### MODIFIED ####
                        if self.machine_type == 'MentorPi_Acker' and float(i[2]) == 0.0:
                            servo_state = PWMServoState()
                            servo_state.id = [3]
                            servo_state.position = [1500] 
                            data = SetPWMServoState()
                            data.state = [servo_state]
                            data.duration = 0.2  
                            self.servo_state_pub.publish(data)
                            self.get_logger().info("Sending servo to center position")

                        time.sleep(float(i[3]))
                else:  # 没有对应的行为，只回答
                    response = self.llm_result
                    msg.data = response
                    # self.tts_text_pub.publish(msg)
                self.action_finish = True
                self.llm_result = ''
            else:
                time.sleep(0.01)
            if self.play_audio_finish and self.action_finish:
                self.play_audio_finish = False
                self.action_finish = False
                msg = SetInt32.Request()
                msg.data = 2
                self.send_request(self.set_mode_client, msg)
                # msg = SetBool.Request()
                # msg.data = True
                # self.send_request(self.awake_client, msg)
        rclpy.shutdown()

def main():
    node = LLMControlMove('llm_control_move')
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    node.destroy_node()
 
if __name__ == "__main__":
    main()
