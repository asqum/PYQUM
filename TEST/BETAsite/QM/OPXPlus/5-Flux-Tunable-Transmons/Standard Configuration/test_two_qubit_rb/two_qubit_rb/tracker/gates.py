from dataclasses import dataclass
from typing import Union

import numpy as np
import qutip
from qutip.qip import operations


@dataclass
class PhasedXZ:
    q: int      # control qubit index
    x: float    # amplitude scaling float
    z: float
    a: float

    def __str__(self):
        return f"PXZ({self.q}, amp={self.x}, z={self.z}, a={self.a})"

    def matrix(self):
        # phxz_00 = np.exp(1j * np.pi * self.x / 2) * np.cos(np.pi * self.x / 2)
        # phxz_01 = -1j * np.exp(1j * np.pi * (self.x / 2 - self.a)) * np.sin(np.pi * self.x / 2)
        # phxz_10 = -1j * np.exp(1j * np.pi * (self.x / 2 + self.z + self.a)) * np.sin(np.pi * self.x / 2)
        # phxz_11 = np.exp(1j * np.pi * (self.x / 2 + self.z)) * np.cos(np.pi * self.x / 2)
        # phased_xz = qutip.Qobj([
        #     [phxz_00, phxz_01],
        #     [phxz_10, phxz_11]
        # ])

        x, a, z = self.x, self.a, self.z

        Z = qutip.sigmaz()
        X = qutip.sigmax()
        def R(theta, U):
            return (-1j * theta / 2 * U).expm()

        def U_X(theta):
            return np.exp(1j * theta / 2) * R(theta, X)

        def U_fr(angle):
            theta = -2 * np.pi * angle
            return R(theta, Z)
            # return np.exp(1j * theta/2) * R(theta, Z)

        def U_impl(x, a, z):
            U_1 = U_fr(a / 2)
            U_2 = U_X(np.pi * x)
            U_3 = U_fr(-(a + z) / 2)

            return U_3 * U_2 * U_1

        phased_xz = U_impl(x, a, z)

        if self.q == 1:
            return qutip.tensor(phased_xz, qutip.qeye(2))
        elif self.q == 2:
            return qutip.tensor(qutip.qeye(2), phased_xz)
        else:
            raise NotImplementedError()


@dataclass
class CZ:
    def __str__(self):
        return f"CZ"

    def matrix(self):
        return operations.cz_gate(2, 0)


@dataclass
class CNOT:
    q: int      # control qubit index

    def __str__(self):
        return f"CNOT({self.q}, {2 if self.q == 1 else 1})"

    def matrix(self):
        return operations.cnot(2, self.q-1, self.get_target() - 1)
        # return operations.cnot(2, self.get_target() - 1, self.q - 1)

    def get_target(self):
        return 2 if self.q == 1 else 1


Operation = Union[PhasedXZ, CZ, CNOT]
