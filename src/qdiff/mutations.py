"""Structural mutations and exact, local equivalent transformations.

Unlike the archived text substitutions, these rules retain operand direction.
Changing mutations produce new seeds; only equivalent mutations are compared
against their parent by the metamorphic oracle.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

from .model import GATES, Circuit, Gate


@dataclass(frozen=True)
class Mutation:
    circuit: Circuit
    rule: str
    position: int


def random_gate(width: int, rng: random.Random) -> Gate:
    name = rng.choice([name for name, (arity, _) in GATES.items() if arity <= width])
    arity, parameters = GATES[name]
    return Gate(
        name,
        tuple(rng.sample(range(width), arity)),
        (rng.uniform(-math.pi, math.pi),) if parameters else (),
    )


def generate(width: int, length: int, rng: random.Random) -> Circuit:
    return Circuit(width, tuple(random_gate(width, rng) for _ in range(length)))


def mutate(circuit: Circuit, rng: random.Random) -> Mutation:
    gates = list(circuit.gates)
    rule = rng.choice(["insert", "replace", "delete"] if gates else ["insert"])
    position = rng.randrange(len(gates) + (rule == "insert"))
    if rule == "insert":
        gates.insert(position, random_gate(circuit.num_qubits, rng))
    elif rule == "replace":
        gates[position] = random_gate(circuit.num_qubits, rng)
    else:
        del gates[position]
    return Mutation(Circuit(circuit.num_qubits, tuple(gates)), rule, position)


def inverse(gate: Gate) -> Gate:
    if gate.params:
        return Gate(gate.name, gate.qubits, (-gate.params[0],))
    return Gate(
        {"s": "sdg", "sdg": "s", "t": "tdg", "tdg": "t"}.get(gate.name, gate.name), gate.qubits
    )


def rewrites(circuit: Circuit):
    """Yield (rule, position, replacement, number consumed)."""
    for i, gate in enumerate(circuit.gates):
        name, qs = gate.name, gate.qubits
        if name in ("cx", "cz"):
            yield (
                f"{name}_decompose",
                i,
                (
                    Gate("h", (qs[1],)),
                    Gate("cz" if name == "cx" else "cx", qs),
                    Gate("h", (qs[1],)),
                ),
                1,
            )
        if name == "swap":
            yield "swap_decompose", i, (Gate("cx", qs), Gate("cx", qs[::-1]), Gate("cx", qs)), 1
        if name in ("s", "z"):
            half = Gate("t" if name == "s" else "s", qs)
            yield "phase_decompose", i, (half, half), 1
        if name in ("x", "z"):
            yield (
                "hadamard_conjugate",
                i,
                (Gate("h", qs), Gate("z" if name == "x" else "x", qs), Gate("h", qs)),
                1,
            )
            if circuit.num_qubits > 1:
                helper = (qs[0] + 1) % circuit.num_qubits
                pair = (helper, qs[0]) if name == "x" else (qs[0], helper)
                yield "cx_conjugate", i, (Gate("cx", pair), gate, Gate("cx", pair)), 1
        if gate.params:
            half = Gate(name, qs, (gate.params[0] / 2,))
            yield "rotation_split", i, (half, half), 1
        if i + 1 < len(circuit.gates):
            following = circuit.gates[i + 1]
            if not set(qs) & set(following.qubits) and gate != following:
                yield "commute_disjoint", i, (following, gate), 2


def equivalent(circuit: Circuit, rng: random.Random, rule: str | None = None) -> Mutation:
    candidates = list(rewrites(circuit))
    if rule:
        candidates = [candidate for candidate in candidates if candidate[0] == rule]
        if not candidates and rule != "inverse_pair":
            raise ValueError(f"Rule {rule!r} does not apply to this circuit")
    if rule == "inverse_pair" or not candidates or (rule is None and rng.random() < 0.3):
        gate = random_gate(circuit.num_qubits, rng)
        choice = ("inverse_pair", rng.randrange(len(circuit.gates) + 1), (gate, inverse(gate)), 0)
    else:
        choice = rng.choice(candidates)
    name, position, replacement, consumed = choice
    gates = circuit.gates[:position] + replacement + circuit.gates[position + consumed :]
    return Mutation(Circuit(circuit.num_qubits, gates), name, position)
