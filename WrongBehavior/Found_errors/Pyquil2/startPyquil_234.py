
from pyquil import Program, get_qc
from pyquil.gates import H, X, CNOT, MEASURE
from pyquil.pyqvm import PyQVM

def make_circuit()-> Program:

    prog = Program() # circuit begin
    #prog += X(0)


    return prog

if __name__ == '__main__':

    p = make_circuit()

    qvm = get_qc('3q-qvm')

    try:
        qvm.run(p)
    except:
        print("empty")
    qvm.run(Program(H(1)))