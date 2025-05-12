## Отчет по работе утилиты nestat
netstat — это утилита командной строки, которая отображает различную информацию, связанную с сетью, включая:
·	Сетевые соединения (как входящие, так и исходящие)
·	Таблицы маршрутизации
·	Статистику сетевых интерфейсов
·	Соединения маскировки
·	Членство в мультикастах
·	Статистику протоколов
## Результаты выполнения
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 localhost:ipp           0.0.0.0:*               LISTEN     
tcp        0      0 debian:60510            ec2-34-237-73-95.:https ESTABLISHED
tcp        0      0 debian:51016            93.243.107.34.bc.:https ESTABLISHED
tcp        0      0 debian:42044            104.18.26.90:https      ESTABLISHED
tcp        0      0 debian:35840            149.154.167.99:https    ESTABLISHED
tcp        0      0 debian:45940            lb-140-82-112-21-:https ESTABLISHED
tcp        0      0 debian:47222            149.154.167.99:https    ESTABLISHED
tcp        0      0 debian:51976            149.154.167.99:https    ESTABLISHED
tcp        0      0 debian:47182            lb-140-82-114-26-:https ESTABLISHED
tcp        0      0 debian:48116            172.64.41.4:https       ESTABLISHED
tcp        0      0 debian:38520            lb-140-82-113-26-:https ESTABLISHED
## Анализ результатов
Основные данные:
 - Всего соединений: 11
 - Все соединения установлены через HTTPS
