#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/23/20 12:18 AM
# @Author  : lingxiangxiang
# @File    : pyquil-penny-forest.py

import pennylane as qml
from pennylane import expval, var


if __name__ == '__main__':

    dev_numpy = qml.device('forest.numpy_wavefunction', wires=2)
    dev_simulator = qml.device('forest.wavefunction', wires=2)
    dev_pyqvm = qml.device('forest.qvm', device='2q-pyqvm', shots=1000)
    dev_qvm = qml.device('forest.qvm', device='2q-qvm', shots=1000)


    @qml.qnode(dev_qvm)
    def circuit(x, y, z):
        qml.RZ(z, wires=[0])
        qml.RY(y, wires=[0])
        qml.RX(x, wires=[0])

        qml.CNOT(wires=[0, 1])
        return expval(qml.PauliZ(0)), var(qml.PauliZ(1))

    print(circuit(0.2, 0.1, 0.3))