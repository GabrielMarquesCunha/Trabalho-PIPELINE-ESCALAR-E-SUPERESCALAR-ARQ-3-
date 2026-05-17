from utils import *
import sys
from instructions import instructions_t1, instructions_t2

if len(sys.argv) < 2:
    print("Uso: python main.py [t1 ou t2]")
    sys.exit(1)

test_choice = sys.argv[1].lower()

if test_choice == "t2":
    selected_instructions = instructions_t2
    branch = "no" 
else:
    selected_instructions = instructions_t1
    branch = "no"

reorder_buffer = new_reorder(8)
reservation_stations = new_reservation()
register_status = new_registers(8)
        
cycle = 0
next = "y"

reorder_buffer = fetch_instructions(reorder_buffer, selected_instructions)

while next != "n":
    commit(reorder_buffer, register_status)
    write_result(reorder_buffer, reservation_stations, register_status)
    execute(reservation_stations, reorder_buffer)
    issue(reorder_buffer, reservation_stations, register_status, cycle)

    print_tables(reorder_buffer, reservation_stations, register_status, cycle, branch)

    print("Continue? No [n] or Yes [any]: ")
    next = input()
    cycle += 1