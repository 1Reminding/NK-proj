import paho.mqtt.client as mqtt
import time
import random
import string
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from datetime import datetime

# 全局设备状态
device_status = {
    "light": "off",
    "heater": "off",
    "speaker": "off"
}

# 用户设备绑定关系
user_device_bindings = {}

# MQTT服务器参数
mqtt_broker = "127.0.0.1"
mqtt_port = 8877

# 已处理的随机数（Nonce）集合，按用户ID区分
processed_nonces = {}

# 加载公钥
with open("public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(key_file.read())

# 格式化日志信息并添加分隔线
def log_info(message, level="INFO", separator=False):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if separator:
        print("\n" + "=" * 50)  # 分割线
    print(f"[{current_time}] [{level}] {message}")
    if separator:
        print("=" * 50)  # 分割线

# 初始化MQTT客户端
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    log_info("连接到MQTT服务器成功", separator=True)
    client.subscribe("devices/+/control")  # 订阅所有用户的控制主题
    client.subscribe("devices/+/bind")  # 订阅所有用户的绑定主题

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    user_id = topic.split("/")[1]  # 从主题中提取用户ID
    log_info(f"接收到消息 - 用户ID: {user_id} | 主题: {topic} | 内容: {payload}", "DEBUG", separator=True)

    # 识别绑定请求和其他控制或查询指令
    if "bind" in topic:
        process_bind_request(user_id, payload)
    else:
        process_control_or_query(user_id, payload)

# 处理绑定请求
def process_bind_request(user_id, device):
    if user_id not in user_device_bindings:
        user_device_bindings[user_id] = set()

    # 检查是否已绑定
    if device in user_device_bindings[user_id]:
        log_info(f"用户 {user_id} 已绑定设备 {device}", "INFO")
    else:
        user_device_bindings[user_id].add(device)
        log_info(f"用户 {user_id} 成功绑定设备 {device}", "INFO")

    client.publish(f"devices/{user_id}/response", f"绑定设备 {device} 成功")

# 处理控制或查询指令
def process_control_or_query(user_id, payload):
    command, timestamp, nonce, signature_hex = payload.rsplit(",", 3)
    device = command.split("on")[0] if "on" in command else command.split("off")[0]

    # 验证签名
    message = f"{command},{timestamp},{nonce}".encode()
    signature = bytes.fromhex(signature_hex)
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        log_info("签名验证通过")
    except Exception as e:
        log_info(f"签名验证失败：{e}", "ERROR")
        client.publish(f"devices/{user_id}/response", "签名验证失败，操作拒绝")
        return

    # 时间戳验证
    current_time = time.time()
    if current_time - float(timestamp) > 60:
        log_info(f"指令已超时，操作拒绝", "WARNING")
        client.publish(f"devices/{user_id}/response", "指令已超时，操作拒绝")
        return

    # 随机数（Nonce）验证
    if user_id not in processed_nonces:
        processed_nonces[user_id] = set()
    if nonce in processed_nonces[user_id]:
        log_info(f"检测到重放攻击 - 用户ID: {user_id} | Nonce: {nonce} 已处理", "WARNING")
        client.publish(f"devices/{user_id}/response", "检测到重放攻击，操作拒绝")
        return
    else:
        processed_nonces[user_id].add(nonce)

    # 检查用户是否绑定了该设备
    if user_id not in user_device_bindings or device not in user_device_bindings[user_id]:
        log_info(f"用户 {user_id} 未绑定设备 {device}，操作拒绝", "WARNING")
        client.publish(f"devices/{user_id}/response", f"未绑定设备 {device}，请先绑定")
        return

    # 继续处理控制或查询指令
    if command in ["lighton", "lightoff", "heateron", "heateroff", "speakeron", "speakeroff"]:
        process_control_command(command)
    elif command in ["light", "heater", "speaker"]:
        process_status_query(command, user_id)

# 控制指令处理
def process_control_command(command):
    global device_status

    if command == "lighton":
        device_status["light"] = "on"
    elif command == "lightoff":
        device_status["light"] = "off"
    elif command == "heateron":
        device_status["heater"] = "on"
    elif command == "heateroff":
        device_status["heater"] = "off"
    elif command == "speakeron":
        device_status["speaker"] = "on"
    elif command == "speakeroff":
        device_status["speaker"] = "off"

    # 将控制状态更新广播给所有用户
    status_message = f"{command.split('on')[0]} 已 {'打开' if 'on' in command else '关闭'}"
    client.publish("devices/broadcast", status_message)  # 广播状态更新
    log_info(f"已广播控制结果：{status_message}", separator=True)

# 状态查询处理
def process_status_query(device, user_id):
    status = device_status.get(device, "未知设备")
    timestamp = str(time.time())
    response_message = f"{device} 当前状态：{status}"
    # 仅向请求查询的用户发送状态更新
    client.publish(f"devices/{user_id}/response", response_message)
    log_info(f"已发送 {user_id} 的 {device} 状态：{status}", separator=True)

# 设置回调函数
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port, 60)
client.loop_start()

while True:
    pass
