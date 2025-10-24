
import hashlib
from scapy.all import Ether, IP, TCP, sendp, sniff
from inference import CNNMetadata  # 保证此类定义与你的 inference.py 一致


class CNNCacheController:
    def __init__(self, interface="veth0"):
        self.interface = interface
        self.cache = {}  # 哈希特征向量 → 分类结果

    def extract_feature_key(self, metadata):
        fields = [
            metadata.ab_1, metadata.ab_2, metadata.ab_3, metadata.ab_4,
            metadata.cd_1, metadata.cd_2, metadata.cd_3, metadata.cd_4,
            metadata.ef_1, metadata.ef_2, metadata.ef_3, metadata.ef_4,
            metadata.gh_1, metadata.gh_2, metadata.gh_3, metadata.gh_4
        ]
        key_str = "_".join(map(str, fields))
        return hashlib.sha256(key_str.encode()).hexdigest()

    def build_packet(self, metadata):
        return Ether() / IP(src="10.0.0.1", dst="10.0.0.2") / TCP() / metadata

    def send_final_result(self, metadata, result):
        metadata.level = 0  # 表示不再需要处理
        metadata.recirculate = 0
        metadata.output_index = result
        pkt = self.build_packet(metadata)
        sendp(pkt, iface=self.interface, verbose=False)
        print(f"[Cache Hit] Sent cached result class {result}")

    def listen_for_result(self, timeout=5):
        print(f"[*] Listening for result packet for up to {timeout} seconds...")
        packets = sniff(timeout=timeout, iface=self.interface, filter="ip")

        for pkt in packets:
            if CNNMetadata in pkt:
                output_index = pkt[CNNMetadata].output_index
                recirculate = pkt[CNNMetadata].recirculate
                print(f"[+] Got result: output_index={output_index}, recirculate={recirculate}")
                return output_index, recirculate

        print("[!] Timeout: no valid CNN result packet received.")
        return None, None

    def run_cnn_pipeline(self, metadata):
        for level in range(1, 6):
            metadata.level = level
            pkt = self.build_packet(metadata)
            sendp(pkt, iface=self.interface, verbose=False)
            print(f"[CNN] Sent level {level}")
            output_index, recirculate = self.listen_for_result()
            if recirculate == 0 and output_index is not None:
                return output_index
        return -1  # 出错情况

    def process_packet(self, metadata):
        key = self.extract_feature_key(metadata)
        if key in self.cache:
            self.send_final_result(metadata, self.cache[key])
        else:
            result = self.run_cnn_pipeline(metadata)
            if result != -1:
                self.cache[key] = result
                self.send_final_result(metadata, result)
            else:
                print("[Error] No result received from CNN pipeline.")

    def run_test(self):
        test_metadata = CNNMetadata(
            level=1, recirculate=1, output_index=0,
            ab_1=10, ab_2=20, ab_3=30, ab_4=40,
            cd_1=5, cd_2=0, cd_3=0, cd_4=0,
            ef_1=0, ef_2=0, ef_3=0, ef_4=0,
            gh_1=0, gh_2=0, gh_3=0, gh_4=0,
            channel_index=0, conv2_flag=0, result_index=0, quan_temp_2=0
        )
        self.process_packet(test_metadata)


if __name__ == "__main__":
    controller = CNNCacheController()
    controller.run_test()
