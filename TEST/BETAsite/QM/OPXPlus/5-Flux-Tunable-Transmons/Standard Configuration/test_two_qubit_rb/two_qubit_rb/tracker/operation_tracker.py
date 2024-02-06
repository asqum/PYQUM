from .gates import *

Sequence = list[Operation]


class OperationTracker:
    def __init__(self):
        self._current_command_id = 0
        self._operations: dict[int, Sequence] = {}

    def register_phase_xz(self, q, z, x, a):
        gate = PhasedXZ(q=q, z=z, x=x, a=a)
        self._register_operation(gate)

    def register_cz(self):
        gate = CZ()
        self._register_operation(gate)

    def register_cnot(self, q):
        gate = CNOT(q=q)
        self._register_operation(gate)

    def register_preparation(self):
        pass

    def register_measurement(self):
        pass

    def _register_operation(self, operation: Operation):
        if self._current_command_id in self._operations:
            command_list = self._operations[self._current_command_id]
        else:
            command_list = []
            self._operations[self._current_command_id] = command_list
        command_list.append(operation)

    def get_command_by_id(self, command_id: int):
        return self._operations[command_id]

    def set_current_command_id(self, command_id: int):
        self._current_command_id = command_id

    def print_operations(self):
        for i in self._operations.keys():
            print(f"Command {i}:")
            for j, operation in enumerate(self._operations[i]):
                print(f"\t{j}: {operation}")
            print("")
