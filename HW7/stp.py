def run_stp(bridges):
    # Этап 1: Выбор корневого моста
    root_bridge = min(bridges, key=lambda b: b.get_bid())
    for b in bridges:
        b.root_id = root_bridge.get_bid()
        b.path_cost = 0 if b == root_bridge else float('inf')

    # Этап 2: Выбор корневых портов
    for b in bridges:
        if b != root_bridge:
            best_port = None
            best_params = (float('inf'), float('inf'), float('inf'), float('inf'))
            
            for port in b.ports:
                if not port.connected_to:
                    continue
                    
                neighbor = port.connected_to.connected_bridge
                total_cost = neighbor.path_cost + port.cost
                neighbor_bid = neighbor.get_bid()
                neighbor_pid = port.connected_to.pid
                self_pid = port.pid
                new_params = (total_cost, neighbor_bid, neighbor_pid, self_pid)
                
                if new_params < best_params:
                    best_port = port
                    best_params = new_params
            
            if best_port:
                b.root_port = best_port
                b.path_cost = best_params[0]
                best_port.role = "Root Port"
                best_port.state = "FORWARDING"

    # Этап 3: Выбор назначенных портов
    processed_links = set()
    for b in bridges:
        for port in b.ports:
            if not port.connected_to:
                continue
                
            link_id = tuple(sorted([id(port), id(port.connected_to)]))
            if link_id in processed_links:
                continue
                
            processed_links.add(link_id)
            other_port = port.connected_to
            other_bridge = other_port.connected_bridge
            
            cost1 = b.path_cost + port.cost
            cost2 = other_bridge.path_cost + other_port.cost
            
            if cost1 < cost2:
                port.role = "Designated Port"
                port.state = "FORWARDING"
            elif cost1 > cost2:
                other_port.role = "Designated Port"
                other_port.state = "FORWARDING"
            else:
                if b.get_bid() < other_bridge.get_bid():
                    port.role = "Designated Port"
                    port.state = "FORWARDING"
                elif b.get_bid() > other_bridge.get_bid():
                    other_port.role = "Designated Port"
                    other_port.state = "FORWARDING"
                else:
                    if port.pid < other_port.pid:
                        port.role = "Designated Port"
                        port.state = "FORWARDING"
                    else:
                        other_port.role = "Designated Port"
                        other_port.state = "FORWARDING"

    # Этап 4: Блокировка остальных портов
    for b in bridges:
        for port in b.ports:
            if not port.role:
                port.role = "Blocked"
                port.state = "BLOCKING"