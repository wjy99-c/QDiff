# QDiff

QDiff tests quantum SDKs by executing the same circuit across implementations
and comparing it with equivalent circuit variants. The maintained runner supports
**Python 3.11–3.12, Qiskit 2.6 + Aer 0.18, Cirq 1.7, and pyQuil 4.22**.
It runs locally, with no IBM account, QPU job, or Rigetti QVM/quilc server required.

The original research programs, discovered-behavior records, and experiment data
remain in this repository. See [migration notes](docs/migration.md) for the
boundary between the maintained runner and the historical artifact.

## Install and run

From a checkout, create a clean environment (Python 3.12 recommended):

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[all]'
qdiff doctor
qdiff run --cases 3 --variants 2 --shots 1024 --seed 17 --output results/first-run
```

On Windows, activate with `.venv\Scripts\activate` instead. SDK wheel availability
depends on the platform; CI covers Linux on Python 3.11 and 3.12.

For a Qiskit-only installation and compiler-setting comparison:

```sh
python -m pip install -e '.[qiskit]'
qdiff run --backends qiskit --optimization-levels 0 3 --cases 3
```

`python -m qdiff` is equivalent to `qdiff`. The original documented entry point
also works after installation:

```sh
python beginTest/QTest.py --cases 3 --shots 1024
```

Each run uses a new output directory. Existing results are never overwritten.
Exit codes: **0** means no discrepancies observed; **1** means discrepancies,
invalid SDK results, crashes, or timeouts were recorded; **2** means a setup/input
error; **130** means interrupted. A discrepancy is a candidate for investigation,
not an automatically confirmed SDK bug.

## What is tested

1. Generate bounded random circuits, or load a JSON seed. Insert/delete/replace
   mutations produce new test seeds. Retain seeds that increase observed output
   discrepancy, with periodic fresh-seed retention.
2. Construct distinct equivalent variants using inverse pairs, CNOT/CZ/SWAP
   decomposition, phase decomposition, conjugation, rotation splitting, and
   reordering of disjoint gates.
3. Run each circuit in Qiskit Aer (optimization levels 0 and 3 by default),
   Cirq's simulator, and pyQuil's local PyQVM. Each execution has a timeout and
   independent deterministic RNG seed.
4. Compare exact statevectors up to global phase and output probabilities, both
   across SDKs/settings and between each original/variant pair. Compare each
   SDK's sampled counts against its exact probabilities using a cumulative KS
   statistic and a DKW bound with a campaign-wide multiple-test correction.
5. Save all circuits, native programs, counts, amplitudes, seeds, versions,
   checks, and errors. Identical circuit structures are deduplicated.

Canonical bitstrings are **q[n−1]…q[0]**: qubit 0 is the rightmost bit. Qiskit
final-layout permutations are explicitly undone before comparing statevectors,
and physical measurements are mapped to the corresponding logical bits.

See [oracle and execution details](docs/testing.md) for interpretation and limits.

## Supply and replay a circuit

```sh
qdiff run --input examples/asymmetric.json --cases 1 --variants 4 --output results/asymmetric
qdiff replay results/asymmetric/case-0000 --output results/asymmetric-replay
```

Inputs use [this small JSON schema](examples/bell.json). Supported gates:
`id`, `h`, `x`, `y`, `z`, `s`, `sdg`, `t`, `tdg`, `rx`, `ry`, `rz`, `p`,
`cx`, `cz`, `swap`, and `ccx`. Angles are finite numeric radians. Circuits have
1–12 qubits, start in the all-zero state, and end with measurement of every qubit.
Mid-circuit measurement, reset, classical control, symbolic parameters, noisy
models, and hardware submission are outside this runner's input contract.

Replay preserves the saved circuits, target settings, and simulator seeds. It
uses the currently installed SDK versions and records them, so the same case can
also test a different SDK release. Identical output across different releases
or platforms is not guaranteed. Never execute archived `.py` programs just to
import a seed; translate their circuit construction to the JSON schema instead.

## Results

Each output directory contains:

| File | Contents |
| --- | --- |
| `manifest.json` | Configuration, package/Python versions, execution mode, run status |
| `summary.json` | Case totals, discrepancies, and execution failures |
| `case-NNNN/case.json` | Complete replay bundle: original, variants, rules, configuration |
| `case-NNNN/report.json` | Differential, metamorphic, and sampling checks |
| `case-NNNN/<variant>/circuit.json` | SDK-independent circuit |
| `case-NNNN/<variant>/<target>.json` | SDK result, seed, timing, counts, statevector, stderr |
| `case-NNNN/<variant>/*.native.*` | Executed OpenQASM 3, Cirq JSON, or Quil program |

Raw output goes under `results/` by default and is excluded from Git. The runner
never writes into the historical `data/` or `benchmark/` directories.

## Development

```sh
python -m pip install -e '.[all,dev]'
python -m pytest
ruff check src tests beginTest/QTest.py
python -m build
```

Tests cover asymmetric bit ordering, idle wires, all supported gates across the
three SDKs, full-unitary preservation of equivalent transformations, Qiskit final
layouts, replay, timeouts, malformed inputs, and injected phase/sampling faults.
Pytest is restricted to `tests/`; archived experiment scripts are not collected.

The Python 3.12 dependency snapshot in
[`requirements/python312-tested.txt`](requirements/python312-tested.txt) records
the environment used for the modernization checks. To recreate it:

```sh
python -m pip install -r requirements/python312-tested.txt
python -m pip install --no-deps -e .
```

## Repository layout

| Directory | Role |
| --- | --- |
| `src/qdiff/`, `tests/`, `examples/` | Maintained implementation, regression tests, inputs |
| `docs/`, `requirements/` | Migration, oracle documentation, tested dependency snapshot |
| `beginTest/QTest.py` | Compatibility launcher for the maintained CLI |
| `beginTest/legacy_QTest.py`, other `beginTest/` scripts | Historical Python 3.7 runners |
| `mutation/`, `compare/`, `transitionBackend/` | Historical implementation, retained for reference |
| `WrongBehavior/`, `benchmark/`, `data/`, testing records | Original research artifact and observations |

The full historical checkout is large. A smaller development checkout is possible:

```sh
git clone --filter=blob:none --sparse https://github.com/wjy99-c/QDiff.git
cd QDiff
git sparse-checkout set src tests examples docs requirements beginTest .github
```
