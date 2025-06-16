class Port:
    def __init__(self, port_id, cost, connected_bridge=None, priority=128):
        self.port_id = port_id
        self.cost = cost
        self.priority = priority
        self.connected_bridge = connected_bridge
        self.state = "BLOCKING"
        self.role = None

    @property
    def pid(self):
        return (self.priority << 12) | self.port_id

    def __str__(self):
        return f"Port-{self.port_id}(Cost={self.cost}, PID={self.pid}, State={self.state}, Role={self.role})"