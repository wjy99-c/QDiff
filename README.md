# QDiff

## Repository structure:

WrongBehavior: All bugs and potential errors found by QDiff.

benchmark: QDiff will save all generated quantum programs in this folder. If you want to change the seed program, you can replace startCirq0.py, startPyquil0.py, and startQiskit0.py

data: All experiment programs are store under this folder in each directory.

mutation: Mutation and equivalent transformation operators. If you want to add your own mutation/equivalent transformation rules, please edit here.

beginTest: Main start entry. Include all the testing oracle logic.

transitionBackend: Backend transformation.


-----


## Getting Started:

In order to run QDiff, you'll need to install Qiskit, Cirq, and Pyquil first. If you want to use IBM quantum computer, you need to register an IBM account.

You can start QDiff directly with the default seed programs:

python3 ./beginTest/QTest.py
