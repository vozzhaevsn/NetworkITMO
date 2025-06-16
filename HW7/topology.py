from bridge import Bridge
from port import Port

def connect_ports(p1, p2):
    p1.connected_to = p2
    p2.connected_to = p1

def create_bridges():
    b1 = Bridge(1)
    b2 = Bridge(2)
    b3 = Bridge(3)

    p1 = Port(1, 4)
    p2 = Port(2, 4)
    p3 = Port(3, 4)
    p4 = Port(4, 4)
    p5 = Port(5, 4)
    p6 = Port(6, 4)

    b1.add_port(p1)
    b1.add_port(p2)
    b2.add_port(p3)
    b2.add_port(p4)
    b3.add_port(p5)
    b3.add_port(p6)

    connect_ports(p1, p3)  # B1 ↔ B2
    connect_ports(p2, p5)  # B1 ↔ B3
    connect_ports(p4, p6)  # B2 ↔ B3

    return [b1, b2, b3]