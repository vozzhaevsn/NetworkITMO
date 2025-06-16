from topology import create_bridges
from stp import run_stp

bridges = create_bridges()
run_stp(bridges)

print("="*50)
print("Финальное состояние сети:")
print("="*50)
for bridge in bridges:
    bridge.print_ports()