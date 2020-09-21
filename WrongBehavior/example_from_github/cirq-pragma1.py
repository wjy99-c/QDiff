#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/15/20 3:47 PM
# @Author  : lingxiangxiang
# @File    : Complier?Bug.py

from typing import Optional

import cirq


class Opty(cirq.PointOptimizer):
    def optimization_at(
            self,
            circuit: 'cirq.Circuit',
            index: int,
            op: 'cirq.Operation'
    ) -> Optional[cirq.PointOptimizationSummary]:
        if (isinstance(op, cirq.ops.GateOperation) and isinstance(op.gate, cirq.CZPowGate)):
            return cirq.PointOptimizationSummary(
                clear_span=0, #run endlessly if clear_span=0
                clear_qubits=op.qubits,
                new_operations=[
                    cirq.CZ(*op.qubits),
                    cirq.X.on_each(*op.qubits),
                    cirq.X.on_each(*op.qubits),
                    cirq.CZ(*op.qubits),
                ]
            )

if __name__ == '__main__':


    circuit = cirq.Circuit(
        cirq.CZ(cirq.GridQubit(5, 2), cirq.GridQubit(5, 3)),
        cirq.CZ(cirq.GridQubit(6, 2), cirq.GridQubit(6, 3)),
        cirq.CZ(cirq.GridQubit(6, 3), cirq.GridQubit(7, 3)),
    )

#circuit = cirq.Circuit(
#    cirq.CZ(cirq.GridQubit(6, 2), cirq.GridQubit(6, 3)),
#    cirq.CZ(cirq.GridQubit(5, 2), cirq.GridQubit(5, 3)),
#    cirq.CZ(cirq.GridQubit(6, 3), cirq.GridQubit(7, 3)),
#)

#give different results

    print(circuit)
    print()

    Opty().optimize_circuit(circuit)

    print(circuit)