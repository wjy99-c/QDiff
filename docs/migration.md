# Migration from the original QDiff artifact

The original code targets a Python 3.7-era quantum software stack. Its programs
and results remain available for historical study; they are not silently
rewritten or relabeled as new experiment results.

The maintained implementation is the `qdiff-testing` package in `src/qdiff/`.
The `qdiff` command and `python beginTest/QTest.py` both invoke it. The original
main runner is preserved as `beginTest/legacy_QTest.py`. Other historical entry
points, SDK converters, and mutation scripts retain their original dependency
requirements; they are not supported entry points for the current SDK stack.

## Changes

| Historical behavior | Maintained behavior |
| --- | --- |
| `python3.7`, hardcoded relative paths, module-level output files | Current interpreter, explicit output paths, import-safe modules |
| `qiskit.execute`, `BasicAer`, `IBMQ`, old fake-provider imports | `transpile` and separately installed `qiskit_aer.AerSimulator` |
| Old `cirq.google` compilation helpers | `cirq-core` simulator and explicit qubit ordering |
| `QVMConnection` and a running Rigetti server | pyQuil 4 local `PyQVM`; no server or account |
| SDK-specific source-code regex substitutions | Validated immutable circuit/gate objects and structural mutations |
| Displayed circuit text used as identity | SHA-256 of canonical circuit data |
| String/CSV count parsing with inconsistent bit reversal | Structured SDK results and one explicit little-endian convention |
| Fixed thresholds and a non-cumulative function named KS | Exact state checks plus a true CDF-based KS sampling bound |
| Shell execution without reliable error/timeout handling | Isolated SDK processes, checked exit status, saved stderr, timeouts |
| Implicit hardware execution in the active runner | Explicit local simulator contract; no cloud submissions |

The new SWAP decomposition uses `CX(a,b); CX(b,a); CX(a,b)`. The old text rule
emitted the same CNOT direction three times. The maintained regression suite
checks full unitaries so that an accidental agreement only on the all-zero input
cannot validate a faulty transformation rule.

## pyQuil compatibility

pyQuil 4.22 deprecates `PyQVM` in preparation for version 5, while recommending
continued use of the public v4 API until that migration. QDiff bounds its extra
to `<5` and captures the warnings in execution records. It explicitly selects
the NumPy wavefunction engine. The `sdg`/`tdg` operations are expressed as
`PHASE(-pi/2)`/`PHASE(-pi/4)` because PyQVM's matrix execution path does not
implement Quil DAGGER modifiers. This adapter tests local pyQuil simulation;
it does not test quilc compilation or a remote QVM/QPU.

## Scope of this migration

The maintained workflow exercises ideal SDK simulation, Qiskit compiler settings,
and equivalent transformations. It does not reproduce the original paper's
hardware experiment, shot-allocation heuristic, Sycamore-specific compiler
pipeline, historical issue counts, or noise thresholds. Its new run reports
must not be presented as reproductions of the archived paper evaluation.

Hardware testing requires a separate contemporary provider adapter and a noise-
aware experimental protocol. The local discrepancy oracle must not be used to
declare every hardware/ideal distribution difference a compiler bug.

Original executable seeds should be translated to the documented JSON gate
vocabulary. Loading arbitrary old Python files could execute obsolete cloud or
filesystem actions, and the three checked-in seed programs do not describe the
same algorithm. They are therefore not automatically executed or imported.
