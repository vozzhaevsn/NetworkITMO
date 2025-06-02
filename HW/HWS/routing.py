import heapq

class Router:
    def __init__(self, name):
        self.name = name
        self.connections = {}
        self.routing_table = {}

    def connect(self, neighbor, cost):
        self.connections[neighbor] = cost
        neighbor.connections[self] = cost

    def build_routing_table(self, network):
        distances = {r: float('inf') for r in network}
        previous = {}
        distances[self] = 0
        heap = [(0, self)]

        while heap:
            current_dist, current = heapq.heappop(heap)
            if current_dist > distances[current]:
                continue
            for neighbor, cost in current.connections.items():
                new_dist = current_dist + cost
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current
                    heapq.heappush(heap, (new_dist, neighbor))

        self.routing_table = {}
        for router in network:
            if router == self or router not in previous:
                continue
            next_hop = router
            while previous[next_hop] != self:
                next_hop = previous[next_hop]
            self.routing_table[router.name] = (next_hop.name, distances[router])

    def __lt__(self, other):
        return self.name < other.name

    def send_packet(self, destination_name, network):
        current = self
        path = [current.name]
        total_cost = 0

        print(f"\nПакет из {self.name} в {destination_name}:")
        while current.name != destination_name:
            route = current.routing_table.get(destination_name)
            if not route:
                print(f"❌ Нет маршрута до {destination_name}")
                return
            next_hop_name, _ = route
            next_router = None
            hop_cost = 0
            for neighbor, cost in current.connections.items():
                if neighbor.name == next_hop_name:
                    next_router = neighbor
                    hop_cost = cost
                    break
            total_cost += hop_cost
            print(f"{current.name} → {next_hop_name} (стоимость {hop_cost})")
            current = next_router
            path.append(current.name)

        print("✅ Достиг цели!")
        print("Путь:", " → ".join(path))
        print(f"Суммарная стоимость: {total_cost}")
r1 = Router("R1")
r2 = Router("R2")
r3 = Router("R3")
r4 = Router("R4")
r5 = Router("R5")
r6 = Router("R6")

r1.connect(r2, 1)    
r1.connect(r3, 10)   
r1.connect(r5, 5)     
r2.connect(r4, 5)     
r3.connect(r4, 1)     
r4.connect(r5, 3)     
r5.connect(r6, 2)     

network = [r1, r2, r3, r4, r5, r6]
# Строим таблицы маршрутов
for router in network:
    router.build_routing_table(network)
# Отправляем пакет из R1 в R4
print("Пакет из R1 в R4 (до изменения стоимости)")
r1.send_packet("R4", network)
# Изменяем стоимость связи R1-R3
print("\nИзменение стоимости R1-R3 с 10 на 1")
r1.connections[r3] = 1
r3.connections[r1] = 1
for router in network:
    router.build_routing_table(network)
print("\nПакет из R1 в R4 (после изменения стоимости)")
r1.send_packet("R4", network)