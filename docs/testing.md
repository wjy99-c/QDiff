# Execution and oracle contract

## Inputs and comparison scope

Every case is a bounded unitary circuit on 1–12 logical qubits initialized to
zero. All wires are measured at the end, with outcome integer `i` representing
the bitstring `q[n-1]...q[0]`. Numeric angles are radians. Dynamic control, reset,
partial readout, noise channels, symbolic angles, and hardware jobs are rejected
by the input vocabulary rather than approximated.

For each original circuit, QDiff constructs equivalent variants. Semantics-
changing insert/delete/replace mutations create *new* originals; they are never
asserted equivalent to their parents. A fixed master seed determines generation,
transformation choices, and separate RNG seeds for every SDK/variant/setting.
The corpus retains improvements in observed TVD (including sampling discrepancy)
and periodic fresh seeds. This heuristic is not a statistical bug probability.

Qiskit is transpiled and executed with Aer; levels 0 and 3 are distinct targets
by default. Cirq uses its native simulator without a hardware-specific compiler.
pyQuil runs in the built-in PyQVM, without quilc. These are different test paths,
not claims of interchangeable SDK optimization-level semantics.

## Exact comparisons

For every variant, compare all available pairs of SDK/settings. Within each
SDK/setting, also compare each equivalent variant with its original. Two checks
are used:

- TVD between the exact computational-basis probability vectors.
- Euclidean distance between the exact statevectors after global-phase alignment.

The default tolerance is `1e-8`; simulators use double precision. A relative-phase
fault can be reported even when the Z-basis probabilities are identical. Norm,
shape, finite-value, and shot-count checks detect malformed SDK output first.

Statevectors are compared in logical order. Cirq and PyQVM axes are reversed to
the canonical convention. For Qiskit, the transpiler's final logical-to-physical
permutation is used both to reorder amplitudes and to attach measurements.
Ignoring this mapping would create false discrepancies when optimization elides
SWAP gates.

These checks compare execution on the all-zero input. They are not a proof of
whole-program unitary equivalence. The regression suite separately validates
the equivalent rewrite rules against full unitaries on small circuits. A
differential disagreement identifies conflicting executions, not which SDK is
correct; no majority result is treated as ground truth.

## Sampling checks

Counts are compared to the *same SDK execution path's* exact probabilities.
The reported KS statistic is `max_i |F_counts(i) - F_exact(i)|`, using cumulative
probabilities over the fixed integer ordering. TVD is also reported, but is not
tested using a KS threshold.

For `n` shots and at most `m` sampling checks in the campaign, the threshold is
`sqrt(log(2*m/alpha)/(2*n))`. This combines the Dvoretzky–Kiefer–Wolfowitz bound
with a union bound, which applies to discrete distributions too and does not
require independence *between* comparisons. Here
`m = cases * (variants + 1) * number_of_SDK_settings`. The default campaign
family-wise sampling false-alarm bound is `alpha = 0.01`, assuming independent
shots from the stated exact distribution. A large bound means low power, not
evidence of correctness. The bound does not model floating-point uncertainty or
hardware noise. Repeated new campaigns introduce additional testing beyond the
scope of one campaign's bound.

Replay retains the original campaign's sampling budget. The SDK versions used
for replay are recorded anew. Do not tune thresholds on a case and interpret
the same case as an independent confirmatory result.

## Failures and artifacts

Circuit definitions are saved before SDK execution. Each SDK call runs in a
separate process with a configurable timeout; on POSIX, the worker process group
is killed on timeout or interruption. An SDK crash or invalid result remains in
the case report and makes the command return 1. Valid results from the other
SDKs are retained, but missing comparisons are not counted as successes.

Run manifests distinguish running, completed, and interrupted campaigns. A
completed campaign can contain flagged cases. Individual JSON writes are atomic;
an existing output directory is never reused. `case.json` plus the recorded
package versions provides the replay inputs. Native OpenQASM/Cirq JSON/Quil
files and raw arrays/counts are kept for investigation.

The CLI and regression tests do not contact quantum cloud services. Optional
SDK packages are imported only when selected, so a Qiskit-only environment can
run compiler-setting and metamorphic tests independently of Cirq and pyQuil.
