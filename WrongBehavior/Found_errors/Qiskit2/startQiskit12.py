# qubit number=5
# total number=6
#using cnot and failed

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import BasicAer, execute
from pprint import pprint


def bitwise_xor(s: str, t: str) -> str:
    length = len(s)
    res = []
    for i in range(length):
        res.append(str(int(s[i]) ^ int(t[i])))
    return ''.join(res[::-1])


def bitwise_dot(s: str, t: str) -> str:
    length = len(s)
    res = 0
    for i in range(length):
        res += int(s[i]) * int(t[i])
    return str(res % 2)

def make_oracle(n:int,secret_string)->QuantumCircuit:
    # implement the oracle O_f
    # NOTE: use multi_control_toffoli_gate ('noancilla' mode)
    # https://qiskit.org/documentation/_modules/qiskit/aqua/circuits/gates/multi_control_toffoli_gate.html
    # https://quantumcomputing.stackexchange.com/questions/3943/how-do-you-implement-the-toffoli-gate-using-only-single-qubit-and-cnot-gates
    # https://quantumcomputing.stackexchange.com/questions/2177/how-can-i-implement-an-n-bit-toffoli-gate
    k=int(n/2)
    input_qubits = QuantumRegister(k, "ofc")
    output_qubits = QuantumRegister(k, "oft")
    oracle = QuantumCircuit(input_qubits, output_qubits, name="Of")

    for i in range(k):
        oracle.cx(input_qubits[i],output_qubits[i])

    if sum(secret_string):  # check if the secret string is non-zero
            # Find significant bit of secret string (first non-zero bit)
        significant = list(secret_string).index(1)

            # Add secret string to input according to the significant bit:
        for j in range(len(secret_string)):
            if secret_string[j] > 0:
                oracle.cx(input_qubits[significant], output_qubits[j])
        # oracle.barrier()
    pos = [0, len(secret_string) - 1]  # Swap some qubits to define oracle. We choose first and last:
    oracle.swap(output_qubits[pos[0]], output_qubits[pos[1]])
    return oracle

def make_circuit(n:int) -> QuantumCircuit:
    # circuit begin
    input_qubit = QuantumRegister(n,"qc")
    classical = ClassicalRegister(n, "qm")
    prog = QuantumCircuit(input_qubit, classical)
    prog.h(input_qubit[1]) # number=1
    prog.h(input_qubit[0]) # number=2
    prog.cx(input_qubit[1],input_qubit[0]) # number=5
    prog.cnot(input_qubit[1],input_qubit[0])

    oracle = make_oracle(n,[0,1])
    k=int(n/2)
    prog.append(oracle.to_gate(),[input_qubit[i] for i in range(k)]+[input_qubit[i] for i in range(k,n)])
    prog.h(input_qubit[1])  # number=3
    prog.h(input_qubit[0])  # number=4

    # circuit end

    for i in range(n):
        prog.measure(input_qubit[i], classical[i])


    return prog



if __name__ == '__main__':


    prog = make_circuit(4)
    backend = BasicAer.get_backend('qasm_simulator')

    info = execute(prog, backend=backend, shots=1024).result().get_counts()

    #writefile = open("../../data/startQiskit0.csv","w")
    pprint(info)#,writefile)
    #writefile.close()