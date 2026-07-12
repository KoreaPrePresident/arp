"""
2_generate_sample_data.py

[이 파일은 데모용입니다]
실제 프로젝트에서는 1_capture_packets.py 가 만든 captured_packets.csv 를 쓰면 됩니다.
여기서는 Claude가 실행하는 샌드박스에 네트워크 캡처 권한이 없기 때문에,
분석 스크립트(3_analyze_packets.py)를 실제로 돌려서 보여드리기 위해
'캡처된 것처럼 보이는' 가짜 패킷 데이터를 만듭니다.
"""

import csv
import random
from datetime import datetime, timedelta

OUTPUT_CSV = "captured_packets.csv"
CSV_FIELDS = ["timestamp", "src_ip", "dst_ip", "protocol", "src_port", "dst_port", "length"]

IPS = [f"192.168.0.{i}" for i in range(2, 8)]
EXTERNAL_IPS = ["142.250.206.14", "104.16.132.229", "17.253.144.10", "13.107.42.14"]
PROTOCOLS = ["TCP", "UDP"]
COMMON_PORTS = [80, 443, 53, 22, 3306, 8080]

random.seed(42)


def random_row(t0):
    proto = random.choice(PROTOCOLS)
    return {
        "timestamp": (t0 + timedelta(milliseconds=random.randint(0, 30000))).isoformat(timespec="milliseconds"),
        "src_ip": random.choice(IPS),
        "dst_ip": random.choice(EXTERNAL_IPS + IPS),
        "protocol": proto,
        "src_port": random.randint(1024, 65535),
        "dst_port": random.choice(COMMON_PORTS),
        "length": random.randint(64, 1500),
    }


def main(n=500):
    t0 = datetime.now()
    rows = [random_row(t0) for _ in range(n)]
    rows.sort(key=lambda r: r["timestamp"])

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[+] 샘플 패킷 {n}개를 {OUTPUT_CSV} 에 생성했습니다.")


if __name__ == "__main__":
    main()
