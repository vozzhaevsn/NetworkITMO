from port import Port

class Bridge:
    def __init__(self, bridge_id, priority=32768):
        self.bridge_id = bridge_id
        self.priority = priority
        self.mac = bridge_id
        self.ports = []
        self.root_id = (self.priority << 48) | self.mac
        self.root_port = None
        self.path_cost = 0

    def get_bid(self):
        return (self.priority << 48) | self.mac

    def add_port(self, port: Port):
        port.connected_bridge = self
        self.ports.append(port)

    def print_ports(self):
        print(f"\nBridge {self.bridge_id}")
        print(f"  BID: {self.get_bid()}")
        print(f"  Root ID: {self.root_id}")
        print(f"  Path Cost: {self.path_cost}")
        if self.root_port:
            print(f"  Root Port: Port {self.root_port.port_id}")
        for port in self.ports:
            print(f"  {port}")