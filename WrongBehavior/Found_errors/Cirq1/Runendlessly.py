
import cirq
from typing import Optional
import sys
from math import sqrt, floor, pi,log2
import numpy as np
class Opty(cirq.PointOptimizer):
    def optimization_at(
            self,
            circuit: 'cirq.Circuit',
            index: int,
            op: 'cirq.Operation'
    ) -> Optional[cirq.PointOptimizationSummary]:
        if (isinstance(op, cirq.ops.GateOperation) and isinstance(op.gate, cirq.CZPowGate)):
            return cirq.PointOptimizationSummary(
                clear_span=-2,
                clear_qubits=op.qubits, #also run endlessly when I set (cirq.GridQubit(2,1),cirq.GridQubit(1,2))
                new_operations=[
                    cirq.X.on_each(*op.qubits),
                    cirq.X.on_each(*op.qubits),
                    cirq.CZ(*op.qubits),
                ]
            )

#thatsNoCode



def make_circuit(input_qubit):


    c = cirq.Circuit() # circuit begin


    c.append(cirq.CZ.on(input_qubit[3],input_qubits[1])) # number=6



    # circuit end

    c.append(cirq.measure(*input_qubit, key='result'))

    return c



def bitstring(bits):
    return ''.join(str(int(b)) for b in bits)

if __name__ == '__main__':
    qubit_count = 4

    input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]
    circuit = make_circuit(input_qubits)

    circuit_sample_count = 1024
    Opty().optimize_circuit(circuit)


    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=circuit_sample_count)

    frequencies = result.histogram(key='result', fold_func=bitstring)

    print(format(frequencies))
