import paho.mqtt.client as mqtt
import time
import random
import string
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from datetime import datetime

# MQTT服务器参数
mqtt_broker = "127.0.0.1"
mqtt_port = 8877

# 用户唯一标识和控制主题
user_id = "user2"  # 用户唯一标识符，可以为每个用户设置不同的ID
control_topic = f"devices/{user_id}/control"
status_topic = f"devices/{user_id}/response"  # 用户私有的响应主题
bind_topic = f"devices/{user_id}/bind"  # 设备绑定主题
broadcast_topic = "devices/broadcast"  # 接收广播消息的主题

# 加载私钥
with open("private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None
    )

# 生成随机数（Nonce）
def generate_nonce(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# 初始化MQTT客户端
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("连接到MQTT服务器成功")
    client.subscribe(status_topic)         # 订阅用户私有的响应主题
    client.subscribe(broadcast_topic)      # 订阅广播主题

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    if topic == status_topic:
        print( payload)
    elif topic == broadcast_topic:
        print( payload)

def send_command(command):
    timestamp = str(time.time())
    nonce = generate_nonce()  # 生成随机数
    message = f"{command},{timestamp},{nonce}".encode()

    # 使用私钥签名消息
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # 将签名转换为可传输的字符串格式
    signature_hex = signature.hex()

    # 构造包含签名的消息
    command_with_signature = f"{command},{timestamp},{nonce},{signature_hex}"

    # 发布控制指令消息
    client.publish(control_topic, command_with_signature)


# 发送绑定请求
def send_bind_request(device):
    client.publish(bind_topic, device)


# 设置回调函数
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port, 60)

# 保持程序运行
client.loop_start()

# 获取用户输入并发送绑定请求或控制指令
print("输入以下指令以控制设备：\n")
print("绑定设备：输入 'bind <设备名称>'，例如 'bind light'")
print("控制设备：输入 'lighton' 开启灯，输入 'lightoff' 关闭灯")
print("加热器：输入 'heateron' 开启，输入 'heateroff' 关闭")
print("音响：输入 'speakeron' 开启，输入 'speakeroff' 关闭")
print("查询设备状态：输入 'light'、'heater' 或 'speaker' 查询状态")

while True:
    time.sleep(0.5)
    user_input = input("请输入指令：")
    if user_input.startswith("bind "):
        device_to_bind = user_input.split(" ")[1]
        send_bind_request(device_to_bind)  # 发送绑定请求
    else:
        send_command(user_input)  # 发送控制指令
