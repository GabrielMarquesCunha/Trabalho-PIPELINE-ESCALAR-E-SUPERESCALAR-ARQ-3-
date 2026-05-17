from os import system
from tabulate import tabulate
from instructions import *

class BufferEntry:
    def __init__(self, entry, busy, instruction, state, value):
        self.entry = entry
        self.busy = busy
        self.instruction = instruction
        self.state = state
        self.value = value
        self.destination = self.instruction.dest

    def toArray(self):
        return [self.entry, self.busy, self.instruction.toString(), self.state, self.destination, self.value]

class ReservationEntry:
    def __init__(self, name, busy, op, vj, vk, qj, qk, dest, a):
        self.name = name
        self.busy = busy
        self.op = op
        self.vj = vj
        self.vk = vk
        self.qj = qj
        self.qk = qk
        self.dest = dest
        self.a = a

    def toArray(self):
        return [self.name, self.busy, self.op, self.vj, self.vk, self.qj, self.qk, self.dest, self.a]

class RegisterEntry:
    def __init__(self, name, reorder_number, busy):
        self.name = name
        self.reorder_number = reorder_number
        self.busy = busy

    def toArray(self):
        return [self.name, self.reorder_number, self.busy]

def fetch_instructions(reorder_buffer, instruction_list):
    i = 0
    n = len(reorder_buffer) if len(reorder_buffer) < len(instruction_list) else len(instruction_list)

    for i in range(0, n):
        reorder_buffer[i] = BufferEntry(i, "Yes", instruction_list[i], "", "")

    return reorder_buffer


def new_reorder(entries):
    arr = []

    for i in range(0, entries):
        arr.append(BufferEntry(i, "No", Instruction("", "", "", "", ""), "", ""))
    
    return arr

def new_reservation():
    arr = []
    stations = ["Load1", "Load2", "Add1", "Add2", "Add3", "Mult1", "Mult2"]

    for unity in stations:
        arr.append(ReservationEntry(unity, "No", "", "", "", "", "", "", ""))

    return arr


def new_registers(entries):
    arr = []

    for i in range(0, 32, 2): 
        arr.append(RegisterEntry("f{}".format(i), "", "No"))

    return arr

def print_horizontal(headers, data):
    i = 0
    dt = list(zip(*data))
    table_data = []
    for row in dt:
        table_data.append([headers[i]] + list(row))
        i += 1

    print(tabulate(table_data, tablefmt="plain"))

def get_array(obj):
    arr = []

    for element in obj:
        arr.append(element.toArray())    
    
    return arr

def print_tables(reorder_buffer, reservation_stations, register_status, cycle, branch):
    system("cls")

    print("\033[1mCycle: {}\033[0m".format(cycle))
    print("\033[1mWill Branch? {}\033[0m".format(branch))
    print('\033[1m-\033[0m' * 100)
    print("\033[1m" + "Reorder Buffer" + "\033[0m")
    print(tabulate(get_array(reorder_buffer), headers=["Entry", "Busy", "Instruction", "State", "Destination", "Value"]))

    print('\033[1m-\033[0m' * 100)
    print("\033[1m" + "Reservation Station" + "\033[0m")
    print(tabulate(get_array(reservation_stations), headers=["Name", "Busy", "Op", "Vj", "Vk", "Qj", "Qk", "Dest", "A"]))

    print('\033[1m-\033[0m' * 100)
    print("\033[1m" + "Register Status" + "\033[0m")

    headers = ["Field", "Reorder Entry", "Busy"]
    print_horizontal(headers, get_array(register_status))
    print('\033[1m-\033[0m' * 100)


# Mapeamento do tempo em ciclos das instruções (baseado em instructions.py)
ciclos_por_op = {
    "ld": 2, "sw": 4, 
    "addd": 2, "subd": 2, 
    "multd": 4, "divd": 8
}

# Dicionário auxiliar para contar quantos ciclos faltam por Estação de Reserva
rs_ciclos = {}

# Ponteiro para saber qual instrução deve ser 'emitida' em seguida
issue_pointer = 0
# Ponteiro para saber qual instrução deve ser 'comitada' em seguida
commit_pointer = 0

def issue(reorder_buffer, reservation_stations, register_status, cycle):
    global issue_pointer
    if issue_pointer >= len(reorder_buffer):
        return
    
    rob_entry = reorder_buffer[issue_pointer]
    # Ignora se não houver instrução carregada ou se já foi emitida
    if rob_entry.instruction.op == "" or rob_entry.state != "":
        return

    op = rob_entry.instruction.op
    
    # Determinar qual unidade usar
    station_type = ""
    if op in ["lw", "sw", "ld"]: station_type = "Load" if op in ["lw", "ld"] else "Store"
    elif op in ["add", "sub", "addd", "subd"]: station_type = "Add"
    elif op in ["mul", "div", "multd", "divd"]: station_type = "Mult" # Note que é 'Mult', para bater com 'Mult1'
    elif op == "bne": station_type = "Bne"

    # Encontrar estação vazia do tipo requisitado
    free_rs = next((rs for rs in reservation_stations if rs.busy == "No" and rs.name.startswith(station_type)), None)
    
    if free_rs:
        free_rs.busy = "Yes"
        free_rs.op = op
        free_rs.dest = rob_entry.entry

        # Simula leitura dos registradores (vj, vk) ou dependências (qj, qk)
        src1 = rob_entry.instruction.vj
        src2 = rob_entry.instruction.vk
        # Lógica para Vj / Qj (Source 1)
        if src1:
            reg1 = src1.replace("0(", "").replace(")", "") 
            reg_stat = next((r for r in register_status if r.name == reg1), None)
            
            if reg_stat and reg_stat.busy == "Yes":
                rob_idx = int(reg_stat.reorder_number)
                # Se a instrução geradora já tem o resultado pronto no ROB, pega direto
                if reorder_buffer[rob_idx].state in ["Write Result", "Commit"]:
                    free_rs.vj = reorder_buffer[rob_idx].value
                    free_rs.qj = ""
                else:
                    free_rs.qj = str(reg_stat.reorder_number)
            else:
                free_rs.vj = f"R[{src1}]" # Valor pronto
                free_rs.qj = ""

        # Lógica para Vk / Qk (Source 2)
        if src2:
            reg2 = src2.replace("0(", "").replace(")", "")
            reg_stat = next((r for r in register_status if r.name == reg2), None)
            
            if reg_stat and reg_stat.busy == "Yes":
                rob_idx = int(reg_stat.reorder_number)
                # Mesmo cheque para o segundo parâmetro
                if reorder_buffer[rob_idx].state in ["Write Result", "Commit"]:
                    free_rs.vk = reorder_buffer[rob_idx].value
                    free_rs.qk = ""
                else:
                    free_rs.qk = str(reg_stat.reorder_number)
            else:
                free_rs.vk = f"R[{src2}]" 
                free_rs.qk = ""
        dest_reg = rob_entry.destination
        if dest_reg != "" and op != "sw": 
            for reg in register_status:
                if reg.name == dest_reg:
                    reg.busy = "Yes"
                    reg.reorder_number = rob_entry.entry
                    break

        rob_entry.state = "Issue"
        rs_ciclos[free_rs.name] = ciclos_por_op.get(op, 1) 
        issue_pointer += 1


def execute(reservation_stations, reorder_buffer):
    for rs in reservation_stations:
        if rs.busy == "Yes" and rs.qj == "" and rs.qk == "":
            # Pode executar
            rs_name = rs.name
            if rs_name in rs_ciclos and rs_ciclos[rs_name] > 0:
                rs_ciclos[rs_name] -= 1
            
          
            if rs_name in rs_ciclos and rs_ciclos[rs_name] == 0:
                rob_idx = rs.dest
                if reorder_buffer[rob_idx].state == "Issue": 
                    reorder_buffer[rob_idx].state = "Execute"


def write_result(reorder_buffer, reservation_stations, register_status):
    for rs in reservation_stations:
        if rs.busy == "Yes":
            rob_entry = reorder_buffer[rs.dest]
            if rob_entry.state == "Execute":
                rob_entry.state = "Write Result"
                val_gerado = f"V{rs.dest}"
                rob_entry.value = val_gerado

                rs.busy = "No"
                rs.op = rs.vj = rs.vk = rs.qj = rs.qk = ""

                for waiting_rs in reservation_stations:
                    if waiting_rs.qj == str(rob_entry.entry):
                        waiting_rs.qj = ""
                        waiting_rs.vj = val_gerado
                    if waiting_rs.qk == str(rob_entry.entry):
                        waiting_rs.qk = ""
                        waiting_rs.vk = val_gerado


def commit(reorder_buffer, register_status):
    global commit_pointer
    if commit_pointer >= len(reorder_buffer):
        return

    head = reorder_buffer[commit_pointer]
    if head.state == "Write Result":
        head.state = "Commit"
        head.busy = "No"
        
        dest_reg = head.destination
        for reg in register_status:
            if reg.name == dest_reg and reg.reorder_number == head.entry:
                reg.busy = "No"
                reg.reorder_number = ""
                break
                
        commit_pointer += 1