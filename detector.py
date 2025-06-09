from scapy.all import *
from collections import defaultdict
import time
import argparse
import threading

FRAG_THRESHOLD = 100      
OVERLAP_THRESHOLD = 5     
CLEANUP_INTERVAL = 10     
WINDOW_SIZE = 5           

ip_frag_count = defaultdict(int)
ip_overlap_count = defaultdict(int)
timestamps = defaultdict(list)
last_cleanup = time.time()

def cleanup_old_entries():
    """Периодическая очистка устаревших записей"""
    global last_cleanup
    while True:
        current_time = time.time()
        if current_time - last_cleanup > CLEANUP_INTERVAL:
            for ip in list(timestamps.keys()):
                timestamps[ip] = [t for t in timestamps[ip] 
                                 if current_time - t < WINDOW_SIZE * 2]
                
                if not timestamps[ip]:
                    del timestamps[ip]
                    if ip in ip_frag_count: 
                        del ip_frag_count[ip]
                    if ip in ip_overlap_count: 
                        del ip_overlap_count[ip]
            
            last_cleanup = current_time
        time.sleep(CLEANUP_INTERVAL)

def detect_anomalies(ip):
    """Анализ трафика на аномалии"""
    current_time = time.time()
    
    window_events = [t for t in timestamps[ip] 
                   if current_time - t < WINDOW_SIZE]
    
    frag_rate = len(window_events)
    overlap_rate = ip_overlap_count.get(ip, 0)
    

    if frag_rate > FRAG_THRESHOLD:
        print(f"[!] Фрагментационная атака: {ip} - {frag_rate} фрагментов/сек")
        
    if overlap_rate > OVERLAP_THRESHOLD:
        print(f"[!!!] Перекрытие фрагментов: {ip} - {overlap_rate} перекрытий")

def process_packet(packet):
    """Обработка каждого IP-пакета"""
    if not packet.haslayer(IP) or packet[IP].flags & 0x1 == 0:
        return
    
    ip_src = packet[IP].src
    current_time = time.time()
    
    ip_frag_count[ip_src] += 1
    timestamps[ip_src].append(current_time)
    

    if packet[IP].frag > 0 and hasattr(packet, 'payload'):
        prev_end = max(timestamps[ip_src][-10:], default=0)
        if current_time - prev_end < 0.1:  
            ip_overlap_count[ip_src] += 1
    
    detect_anomalies(ip_src)

def start_sniffing():
    """Запуск сниффера"""
    print("[*] Запуск детектора IP Fragmentation атак...")
    print(f"[*] Параметры детекции:")
    print(f"    - Макс. фрагментов/сек: {FRAG_THRESHOLD}")
    print(f"    - Макс. перекрытий/сек: {OVERLAP_THRESHOLD}")
    print(f"    - Анализируемое окно: {WINDOW_SIZE} сек")
    
    sniff(filter="ip and (ip[6] & 0x1 != 0 or ip[6] & 0x1FFF != 0)", 
          prn=process_packet, 
          store=0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Детектор IP Fragmentation атак")
    args = parser.parse_args()

    threading.Thread(target=cleanup_old_entries, daemon=True).start()
    
    start_sniffing()