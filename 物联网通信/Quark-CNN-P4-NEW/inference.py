from scapy.all import *
import time
import threading

class CNNMetadata(Packet):
    fields_desc = [#定义 P4 Header 映射的元数据格式
        ByteField("level", 0),
        ByteField("channel_index", 0),
        ByteField("conv2_flag", 0),
        ByteField("result_index", 0),
        ByteField("recirculate", 0),
        ByteField("quan_temp_2", 0),
        ByteField("ab_1", 0), ByteField("ab_2", 0), ByteField("ab_3", 0), ByteField("ab_4", 0),
        ByteField("cd_1", 0), ByteField("cd_2", 0), ByteField("cd_3", 0), ByteField("cd_4", 0),
        ByteField("ef_1", 0), ByteField("ef_2", 0), ByteField("ef_3", 0), ByteField("ef_4", 0),
        ByteField("gh_1", 0), ByteField("gh_2", 0), ByteField("gh_3", 0), ByteField("gh_4", 0),
        ByteField("abcd_1", 0), ByteField("abcd_2", 0), ByteField("abcd_3", 0), ByteField("abcd_4", 0),
        ShortField("ab_temp", 0),
        ShortField("cd_temp", 0),
        ByteField("quan_temp_1", 0),
        ByteField("maxnum", 0),
        ByteField("output_index", 0),
    ]

bind_layers(TCP, CNNMetadata, dport=1)
bind_layers(TCP, CNNMetadata, dport=2)

class CNNLooper:
    def __init__(self):
        # 原始特征值：diffserv 和 ttl
        self.diffserv = 128  # IPv4 diffserv字段
        self.ttl = 64      # IPv4 TTL字段，设置为常见的默认值64
        
        # 中间特征值全部初始化为0
        self.ab_features = [0, 0, 0, 0]     # ab_1到ab_4 (中间特征)
        self.cd_features = [0, 0, 0, 0]     # cd_1到cd_4 (中间特征)
        self.ef_features = [0, 0, 0, 0]     # ef_1到ef_4 (中间特征)
        self.gh_features = [0, 0, 0, 0]     # gh_1到gh_4 (中间特征)
        self.abcd_features = [0, 0, 0, 0]   # abcd_1到abcd_4 (中间特征)
        
        self.loop_cnt = 0
        self.received_packets = []  # 存储所有收到的包
        self.packet_received = threading.Event()
        self.is_inner_loop = False  # 新增：标记是否为内循环
        init_pkt = self.build_packet(
            level=1,
            recirculate=105,  
            src_mac="00:00:00:00:00:01",
            dst_mac="00:00:00:00:00:02",
            src_ip="10.0.0.1",
            dst_ip="10.0.0.2",
            sport=1,
            dport=2
        )
        self.last_meta = init_pkt[CNNMetadata]
#IP 层使用 diffserv 和 ttl 作为图像像素的模拟输入,CNNMetadata 中填入前一轮返回的中间特征（权重计算完的结果）
    def build_packet(self, level, recirculate, src_mac, dst_mac, src_ip, dst_ip, sport, dport):
        return Ether(src=src_mac, dst=dst_mac) / \
            IP(src=src_ip, dst=dst_ip, proto=6, tos=self.diffserv, ttl=self.ttl) / \
            TCP(sport=sport, dport=dport) / \
            CNNMetadata(#CNNMetadata 中填入前一轮返回的中间特征（权重计算完的结果）
                level=level,
                channel_index=1,
                conv2_flag=0,
                result_index=1,
                recirculate=recirculate,
                # 中间特征值全部初始化为0
                ab_1=self.ab_features[0], ab_2=self.ab_features[1], 
                ab_3=self.ab_features[2], ab_4=self.ab_features[3],
                cd_1=self.cd_features[0], cd_2=self.cd_features[1], 
                cd_3=self.cd_features[2], cd_4=self.cd_features[3],
                ef_1=self.ef_features[0], ef_2=self.ef_features[1], 
                ef_3=self.ef_features[2], ef_4=self.ef_features[3],
                gh_1=self.gh_features[0], gh_2=self.gh_features[1], 
                gh_3=self.gh_features[2], gh_4=self.gh_features[3],
                # abcd特征也初始化为0
                abcd_1=self.abcd_features[0], abcd_2=self.abcd_features[1],
                abcd_3=self.abcd_features[2], abcd_4=self.abcd_features[3],
                ab_temp=0,
                cd_temp=0,
                quan_temp_1=0,
                quan_temp_2=0,
                maxnum=0
            )

    def packet_handler(self, pkt):
        """数据包处理函数，收集所有包"""
        if pkt.haslayer(CNNMetadata):
            packet_info = {
                'packet': pkt,
                'timestamp': time.time(),
                'metadata': pkt[CNNMetadata]
            }
            self.received_packets.append(packet_info)
            
            # 新增：在内循环中，收到第二个包时立即停止监听
            if self.is_inner_loop and len(self.received_packets) >= 2:
                self.packet_received.set()  # 立即设置事件，停止监听
                return True  # 返回True表示停止监听

    def listen_async(self, recv_if, timeout=2):  # 修改超时为2秒
        """异步监听函数，收集2秒内的所有包"""
        self.received_packets = []  # 清空包列表
        
        def sniff_worker():           
            # 修改：在内循环中使用stop_filter来提前停止
            if self.is_inner_loop:
                sniff(
                    iface=recv_if, 
                    prn=self.packet_handler,
                    timeout=timeout,
                    stop_filter=lambda x: len(self.received_packets) >= 2 and x.haslayer(CNNMetadata)
                )
            else:
                sniff(
                    iface=recv_if, 
                    prn=self.packet_handler,
                    timeout=timeout
                )
            
            self.packet_received.set()  # 监听结束后设置事件
        
        # 启动监听线程
        listener_thread = threading.Thread(target=sniff_worker)
        listener_thread.daemon = True
        listener_thread.start()
        
        return listener_thread
    def display_all_packets(self):
        """展示所有收到的包"""
        if not self.received_packets:
            print("❌ 没有收到任何包")
            return None
        
        print(f"\n📋 收到的数据包:")
        print("=" * 40)
        
        # 使用最后一个包（最新收到的包）
        target_index = len(self.received_packets) - 1
        pkt_info = self.received_packets[target_index]
        pkt = pkt_info['packet']
        meta = pkt_info['metadata']
        timestamp = pkt_info['timestamp']
        
        print(f"\n📦 数据包 {target_index + 1} (时间戳: {time.strftime('%H:%M:%S.%f', time.localtime(timestamp))[:-3]})")
        print("-" * 40)
        
        # 显示以太网层信息
        if pkt.haslayer(Ether):
            eth = pkt[Ether]
            print(f"   以太网: {eth.src} → {eth.dst}")
        
        # 显示IP层信息
        if pkt.haslayer(IP):
            ip = pkt[IP]
            tcp = pkt[TCP]
            print(f"   IP/TCP: {ip.src}:{tcp.sport} → {ip.dst}:{tcp.dport}")
        
        # 显示CNNMetadata信息
        print(f"   CNNMetadata:")
        print(f"     level={meta.level}, channel_index={meta.channel_index}")
        print(f"     conv2_flag={meta.conv2_flag}, result_index={meta.result_index}")
        print(f"     recirculate={meta.recirculate}")
        print(f"     features:")
        print(f"       ab=[{meta.ab_1},{meta.ab_2},{meta.ab_3},{meta.ab_4}]")
        print(f"       cd=[{meta.cd_1},{meta.cd_2},{meta.cd_3},{meta.cd_4}]")
        print(f"       ef=[{meta.ef_1},{meta.ef_2},{meta.ef_3},{meta.ef_4}]")
        print(f"       gh=[{meta.gh_1},{meta.gh_2},{meta.gh_3},{meta.gh_4}]")
        print(f"       abcd=[{meta.abcd_1},{meta.abcd_2},{meta.abcd_3},{meta.abcd_4}]")
        print(f"     temps: ab_temp={meta.ab_temp}, cd_temp={meta.cd_temp}")
        print(f"     quan_temp_1={meta.quan_temp_1}, quan_temp_2={meta.quan_temp_2}")
        print(f"     maxnum={meta.maxnum}, output_index={meta.output_index}")
        
        print("=" * 80)
        
        return meta

    def loop_infer(self):
        while True:
            if self.loop_cnt == 0:
                send_if, recv_if = "veth0", "veth2"
                src_ip, dst_ip = "10.0.0.1", "10.0.0.2"
                sport, dport = 1, 2
                self.is_inner_loop = False  # 不是内循环
            elif  self.last_meta.level == 5 and self.last_meta.channel_index == 15 and self.last_meta.conv2_flag == 2:
                send_if, recv_if = "veth2", "veth0"
                src_ip, dst_ip = "10.0.0.2", "10.0.0.1"
                sport, dport = 2, 1
                self.is_inner_loop = False  # 外循环
            else:
                send_if, recv_if = "veth2", "veth2"
                src_ip = dst_ip = "10.0.0.2"
                sport = dport = 2
                self.is_inner_loop = True  # 这是内循环

            try:
                src_mac = get_if_hwaddr(send_if)
                dst_mac = get_if_hwaddr(recv_if)
            except Exception as e:
                print(f"❌ 获取MAC地址失败: {e}")
                # 使用默认MAC地址
                src_mac = dst_mac = "00:00:00:00:00:01"

            meta_copy = self.last_meta.copy()
            pkt = Ether(src=src_mac, dst=dst_mac) / \
                  IP(src=src_ip, dst=dst_ip, proto=6) / \
                  TCP(sport=sport, dport=dport) / \
                  meta_copy

            loop_type = "内循环" if self.is_inner_loop else "外循环"
            print(f"\n🚀 第 {self.loop_cnt + 1} 次循环 ({loop_type}) - 发送数据包 on {send_if} (sport={sport} → dport={dport})")
            print(f"📤 发送包的recirculate值: {meta_copy.recirculate}")
            
            # 启动异步监听
            self.packet_received.clear()
            listener_thread = self.listen_async(recv_if, timeout=2)
            
            # 等待一小段时间确保监听已启动
            time.sleep(0.1)
            
            # 发送数据包
            sendp(pkt, iface=send_if, verbose=False)
            print("✅ 数据包已发送")
            
            # 等待监听完成（2秒超时）
            if self.packet_received.wait(timeout=3):  # 给监听线程额外1秒的缓冲时间
                # 展示所有收到的包
                last_meta = self.display_all_packets()
                
                if last_meta is None:
                    print("❌ 没有收到任何包，退出循环")
                    break
                
                # 使用目标包的metadata进入下一次循环
                self.last_meta = last_meta

                if last_meta.recirculate == 1:
                    print(f"\n🎉 推理完成: 类别={last_meta.output_index} 概率={last_meta.maxnum}")
                    break
                else:
                    self.loop_cnt += 1
            else:
                print("❌ 监听超时，退出循环")
                break
            
            # 确保监听线程结束
            listener_thread.join(timeout=1)
            

if __name__ == "__main__":
    CNNLooper().loop_infer()
