from scapy.all import sniff, Ether, IP, TCP, UDP
import csv
import time


ETH_IPV4 = 0x0800
# ETH_ARP = 0x0806
ETH_IPV6 = 0x86DD

times = 10000

data = []

packets = sniff(count=times)


component = ["time_stamp", "MAC_dst", "MAC_src", "ETher_type", "ttl", "proto", "IP_src", "IP_dst", "sport", "dport", "Len"]





for pkt in packets:
    if pkt.haslayer(Ether):
        if pkt[Ether].type == ETH_IPV4:
            #IPv4
        
            if pkt.haslayer(TCP):
                data.append([time.time(), pkt[Ether].dst, pkt[Ether].src, pkt[Ether].type, pkt[IP].ttl, pkt[IP].proto, pkt[IP].src, pkt[IP].dst, pkt[TCP].sport, pkt[TCP].dport, len(pkt)])
            elif pkt.haslayer(UDP):
                data.append([time.time(), pkt[Ether].dst, pkt[Ether].src, pkt[Ether].type, pkt[IP].ttl, pkt[IP].proto, pkt[IP].src, pkt[IP].dst, pkt[UDP].sport, pkt[UDP].dport, len(pkt)])
            else:
                protocol = "Other"
                sport = None
                dport = None
                data.append([time.time(), pkt[Ether].dst, pkt[Ether].src, pkt[Ether].type, pkt[IP].ttl, pkt[IP].proto, pkt[IP].src, pkt[IP].dst, sport, dport, len(pkt)])
        else:
            pass
    else:
        pass





with open(r"/home/seowhy/arpdata/youtube/subpc_3_2_normal.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(component)

    writer.writerows(data)