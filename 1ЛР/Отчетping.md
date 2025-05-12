# Отчет по работе утилиты ping
Утилита ping является одним из базовых инструментов сетевой диагностики, используемым для проверки доступности узлов в IP-сетях. Она работает по протоколу ICMP, отправляя пакеты на указанный адрес и измеряя время до получения ответа. Основные задачи ping включают проверку связи с удаленным хостом, измерение времени отклика и выявление потерь пакетов.

## Результаты выполнения
semyon@debian:~$ ping yandex.ru -c 5
PING yandex.ru (5.255.255.77) 56(84) bytes of data.
64 bytes from yandex.ru (5.255.255.77): icmp_seq=1 ttl=55 time=160 ms
64 bytes from yandex.ru (5.255.255.77): icmp_seq=2 ttl=55 time=204 ms
64 bytes from yandex.ru (5.255.255.77): icmp_seq=3 ttl=55 time=125 ms
64 bytes from yandex.ru (5.255.255.77): icmp_seq=4 ttl=55 time=149 ms
64 bytes from yandex.ru (5.255.255.77): icmp_seq=5 ttl=55 time=173 ms

--- yandex.ru ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4002ms
rtt min/avg/max/mdev = 125.240/162.219/203.997/26.084 ms

 Анализ результатов

### Доступность узла:
- Узел доступен
- IP-адрес: 5.255.255.77
  ## Задержка (rtt) :
  - Минимальная : 125.24 мс
  - Средняя : 162.22 мс
  - Максимальная : 204.00 мс
### TTL (Time To Live):
- TTL=55
