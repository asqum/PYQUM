from .operation_tracker import *


class SequenceTracker:
    def __init__(self, operation_tracker: OperationTracker):
        self.operation_tracker: OperationTracker = operation_tracker
        self._sequences: list[Sequence] = []
        self._sequences_as_command_ids: list[list[int]] = []

    def make_sequence(self, command_ids: list[int]):
        self._sequences.append([])
        self._sequences_as_command_ids.append([])
        for command_id in command_ids:
            self.add_operation_to_current_sequence_as_command_id(command_id)
            operations = self.operation_tracker.get_command_by_id(command_id)
            for operation in operations:
                self.add_operation_to_current_sequence(operation)

    def add_operation_to_current_sequence_as_command_id(self, command_id: int):
        self._sequences_as_command_ids[-1].append(command_id)

    def add_operation_to_current_sequence(self, operation: Operation):
        self._sequences[-1].append(operation)

    def print_sequences(self):
        for i, sequence in enumerate(self._sequences):
            print(f"Sequence {i}:")
            print(f"\tCommand IDs: {self._sequences_as_command_ids[i]}")
            print(f"\tGates:")
            for j, operation in enumerate(sequence):
                print(f"\t\t{j}: {operation}")
            print("")

    def verify_sequences(self):
        for i, sequence in enumerate(self._sequences):
            d = qutip.basis(2, 0) * qutip.basis(2, 0).dag()
            rho = qutip.tensor(d, d)
            for operation in sequence:
                rho = operation.matrix() * rho * operation.matrix().dag()
            assert rho == qutip.tensor(d, d), f"expected to end at |00><00|, got {rho}"
        print(f"Verification passed for all {len(self._sequences)} sequence(s).")
