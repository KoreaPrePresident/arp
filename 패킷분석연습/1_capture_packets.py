"""
1_capture_packets.py

실시간으로 네트워크 패킷을 캡처해서 CSV 파일로 저장하는 스크립트입니다.

[중요]
- Claude가 실행 중인 샌드박스 환경에는 네트워크 인터페이스 접근 권한이 없어서
  이 스크립트는 여기서 직접 실행할 수 없습니다.
- 사용자의 실제 PC(Windows/Mac/Linux)에서 실행해야 하며, 관리자 권한(sudo)이 필요합니다.
- Windows는 Npcap(https://npcap.com) 설치가 필요합니다.

실행 방법:
    pip install scapy
    sudo python3 1_capture_packets.py        # Linux/Mac
    (관리자 권한 cmd/PowerShell) python 1_capture_packets.py   # Windows

캡처를 멈추려면 Ctrl+C 를 누르세요.
"""

import csv
import time
from datetime import datetime

from scapy.all import sniff, IP, TCP, UDP

OUTPUT_CSV = "captured_packets.csv"
CSV_FIELDS = [
    "timestamp",
    "src_ip",
    "dst_ip",
    "protocol",
    "src_port",
    "dst_port",
    "length",
]


def packet_to_row(pkt):
    """패킷 하나에서 CSV에 저장할 정보를 뽑아낸다."""
    if IP not in pkt:
        return None  # IP 계층이 없는 패킷(ARP 등)은 건너뜀

    ip_layer = pkt[IP]

    if TCP in pkt:
        proto = "TCP"
        sport = pkt[TCP].sport
        dport = pkt[TCP].dport
    elif UDP in pkt:
        proto = "UDP"
        sport = pkt[UDP].sport
        dport = pkt[UDP].dport
    else:
        proto = str(ip_layer.proto)  # 그 외 프로토콜 번호
        sport = None
        dport = None

    return {
        "timestamp": datetime.now().isoformat(timespec="milliseconds"),
        "src_ip": ip_layer.src,
        "dst_ip": ip_layer.dst,
        "protocol": proto,
        "src_port": sport,
        "dst_port": dport,
        "length": len(pkt),
    }


def main(capture_seconds=30, iface=None):
    print(f"[+] {capture_seconds}초 동안 패킷을 캡처합니다. (Ctrl+C로 중단 가능)")

    rows = []

    def handle_packet(pkt):
        row = packet_to_row(pkt)
        if row:
            rows.append(row)
            print(f"  캡처: {row['src_ip']} -> {row['dst_ip']} ({row['protocol']})")

    # count=0 이면 무한 캡처, timeout으로 시간 제한
    sniff(prn=handle_packet, store=False, timeout=capture_seconds, iface=iface)

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[+] 총 {len(rows)}개 패킷을 {OUTPUT_CSV} 에 저장했습니다.")


if __name__ == "__main__":
    main(capture_seconds=30)
