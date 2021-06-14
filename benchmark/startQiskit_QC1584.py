# qubit number=4
# total number=38
import cirq
import qiskit
from qiskit import IBMQ
from qiskit.providers.ibmq import least_busy

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import BasicAer, execute, transpile
from pprint import pprint
from qiskit.test.mock import FakeVigo
from math import log2
import numpy as np
import networkx as nx

def make_circuit(n:int) -> QuantumCircuit:
    # circuit begin
    input_qubit = QuantumRegister(n,"qc")
    classical = ClassicalRegister(n, "qm")
    prog = QuantumCircuit(input_qubit, classical)
    prog.h(input_qubit[0]) # number=1
    prog.h(input_qubit[1]) # number=2
    prog.h(input_qubit[2])  # number=3
    prog.h(input_qubit[3])  # number=4

    for edge in E:
        k = edge[0]
        l = edge[1]
        prog.cp(-2 * gamma, input_qubit[k-1], input_qubit[l-1])
        prog.p(gamma, k)
        prog.p(gamma, l)

    prog.rx(2 * beta, range(len(V)))

    prog.h(input_qubit[0]) # number=12
    prog.h(input_qubit[1]) # number=22
    prog.cz(input_qubit[2],input_qubit[1]) # number=23
    prog.h(input_qubit[1]) # number=24
    prog.cz(input_qubit[3],input_qubit[0]) # number=13
    prog.h(input_qubit[0]) # number=14
    prog.y(input_qubit[3]) # number=20
    prog.h(input_qubit[0]) # number=9
    prog.h(input_qubit[0]) # number=35
    prog.cz(input_qubit[1],input_qubit[0]) # number=36
    prog.h(input_qubit[0]) # number=37
    prog.z(input_qubit[1]) # number=29
    prog.cx(input_qubit[1],input_qubit[0]) # number=30
    prog.cx(input_qubit[1],input_qubit[0]) # number=32
    prog.z(input_qubit[1]) # number=33
    prog.cx(input_qubit[1],input_qubit[0]) # number=34
    prog.cz(input_qubit[3],input_qubit[0]) # number=10
    prog.y(input_qubit[3]) # number=17
    prog.h(input_qubit[0]) # number=11
    prog.y(input_qubit[2]) # number=7
    prog.y(input_qubit[2]) # number=8
    prog.y(input_qubit[1]) # number=15
    prog.y(input_qubit[1]) # number=16
    prog.swap(input_qubit[2],input_qubit[0]) # number=18
    prog.swap(input_qubit[2],input_qubit[0]) # number=19
    prog.cx(input_qubit[3],input_qubit[0]) # number=25
    prog.cx(input_qubit[3],input_qubit[0]) # number=26
    # circuit end

    for i in range(n):
        prog.measure(input_qubit[i], classical[i])


    return prog



if __name__ == '__main__':
    n = 4
    V = np.arange(0, n, 1)
    E = [(0, 1, 1.0), (0, 2, 1.0), (1, 2, 1.0), (3, 2, 1.0), (3, 1, 1.0)]

    G = nx.Graph()
    G.add_nodes_from(V)
    G.add_weighted_edges_from(E)

    step_size = 0.1

    a_gamma = np.arange(0, np.pi, step_size)
    a_beta = np.arange(0, np.pi, step_size)
    a_gamma, a_beta = np.meshgrid(a_gamma, a_beta)

    F1 = 3 - (np.sin(2 * a_beta) ** 2 * np.sin(2 * a_gamma) ** 2 - 0.5 * np.sin(4 * a_beta) * np.sin(4 * a_gamma)) * (
                1 + np.cos(4 * a_gamma) ** 2)

    result = np.where(F1 == np.amax(F1))
    a = list(zip(result[0], result[1]))[0]

    gamma = a[0] * step_size
    beta = a[1] * step_size

    prog = make_circuit(4)
    IBMQ.load_account() 
    provider = IBMQ.get_provider(hub='ibm-q') 
    provider.backends()
    backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= 2 and not x.configuration().simulator and x.status().operational == True))
    sample_shot =2720

    info = execute(prog, backend=backend, shots=sample_shot).result().get_counts()
    backend = FakeVigo()
    circuit1 = transpile(prog,backend,optimization_level=2)

    writefile = open("../data/startQiskit_QC1584.csv","w")
    print(info,file=writefile)
    print("results end", file=writefile)
    print(circuit1.__len__(),file=writefile)
    print(circuit1,file=writefile)
    writefile.close()