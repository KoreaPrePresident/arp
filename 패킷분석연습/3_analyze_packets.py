"""
3_analyze_packets.py

captured_packets.csv 를 읽어서 기본적인 트래픽 분석을 수행합니다.
- 프로토콜별 패킷 수
- 목적지 IP별 패킷 수 (Top 5)
- 목적지 포트별 패킷 수 (Top 5)
- 패킷 길이 통계
- 프로토콜 비율 파이 차트 저장 (packet_analysis.png)
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # 화면 없이 파일로 저장하기 위한 백엔드
import matplotlib.pyplot as plt

INPUT_CSV = "captured_packets.csv"


def main():
    df = pd.read_csv(INPUT_CSV, parse_dates=["timestamp"])
    print(f"[+] 총 {len(df)}개의 패킷을 불러왔습니다.\n")

    # 1. 프로토콜별 패킷 수
    print("=== 프로토콜별 패킷 수 ===")
    proto_counts = df["protocol"].value_counts()
    print(proto_counts, "\n")

    # 2. 목적지 IP Top 5
    print("=== 목적지 IP Top 5 ===")
    print(df["dst_ip"].value_counts().head(5), "\n")

    # 3. 목적지 포트 Top 5 (어떤 서비스로 트래픽이 몰리는지)
    print("=== 목적지 포트 Top 5 ===")
    print(df["dst_port"].value_counts().head(5), "\n")

    # 4. 패킷 길이 통계
    print("=== 패킷 길이(length) 통계 ===")
    print(df["length"].describe(), "\n")

    # 5. 초당 패킷 수 (트래픽 흐름)
    df["second"] = df["timestamp"].dt.floor("s")
    per_second = df.groupby("second").size()
    print("=== 초당 패킷 수 (앞 5개) ===")
    print(per_second.head(5), "\n")

    # 6. 시각화: 프로토콜 비율 파이차트 + 초당 트래픽 라인차트
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    axes[0].pie(proto_counts.values, labels=proto_counts.index, autopct="%1.1f%%",
                colors=["#4C72B0", "#DD8452", "#55A868"])
    axes[0].set_title("Protocol Ratio")

    axes[1].plot(per_second.index, per_second.values, marker="o", color="#4C72B0")
    axes[1].set_title("Packets per Second")
    axes[1].set_xlabel("Time")
    axes[1].set_ylabel("Packet Count")
    axes[1].tick_params(axis="x", rotation=30)

    fig.tight_layout()
    fig.savefig("packet_analysis.png", dpi=150)
    print("[+] 시각화 결과를 packet_analysis.png 로 저장했습니다.")


if __name__ == "__main__":
    main()
