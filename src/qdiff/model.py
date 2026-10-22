"""Versioned, SDK-independent unitary circuits with terminal full-register readout.

Wire 0 is the least significant bit everywhere, including native SDK results.
JSON inputs are data; QDiff never executes user-supplied Python source.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path

# (number of qubits, number of numeric parameters)
GATES = {
    **dict.fromkeys(("h", "x", "y", "z", "s", "sdg", "t", "tdg", "id"), (1, 0)),
    **dict.fromkeys(("rx", "ry", "rz", "p"), (1, 1)),
    **dict.fromkeys(("cx", "cz", "swap"), (2, 0)),
    "ccx": (3, 0),
}
MAX_QUBITS = 12  # Dense statevectors are deliberately bounded in the local runner.
MAX_GATES = 10000


def integer(value, name: str, low: int, high: int) -> int:
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{name} must be an integer in [{low}, {high}]")
    return value


@dataclass(frozen=True)
class Gate:
    name: str
    qubits: tuple[int, ...]
    params: tuple[float, ...] = ()

    def __post_init__(self):
        if not isinstance(self.name, str) or self.name not in GATES:
            raise ValueError(f"Unsupported gate: {self.name!r}")
        object.__setattr__(self, "qubits", tuple(self.qubits))
        object.__setattr__(self, "params", tuple(self.params))
        arity, parameters = GATES[self.name]
        if len(self.qubits) != arity or len(self.params) != parameters:
            raise ValueError(f"{self.name} needs {arity} qubits and {parameters} parameters")
        for q in self.qubits:
            integer(q, "qubit", 0, MAX_QUBITS - 1)
        if len(set(self.qubits)) != arity:
            raise ValueError("A gate cannot use the same qubit twice")
        if any(type(p) not in (int, float) or not math.isfinite(p) for p in self.params):
            raise ValueError("Gate parameters must be finite real numbers")
        object.__setattr__(self, "params", tuple(float(p) for p in self.params))

    def to_dict(self):
        return {"gate": self.name, "qubits": list(self.qubits), "params": list(self.params)}

    @classmethod
    def from_dict(cls, value):
        if not isinstance(value, dict) or set(value) - {"gate", "qubits", "params"}:
            raise ValueError("Each gate must contain only gate, qubits, and optional params")
        if not {"gate", "qubits"} <= set(value):
            raise ValueError("Each gate requires gate and qubits")
        if not isinstance(value["qubits"], list) or not isinstance(value.get("params", []), list):
            raise ValueError("Gate qubits and params must be arrays")
        return cls(value["gate"], tuple(value["qubits"]), tuple(value.get("params", [])))


@dataclass(frozen=True)
class Circuit:
    num_qubits: int
    gates: tuple[Gate, ...]

    def __post_init__(self):
        integer(self.num_qubits, "num_qubits", 1, MAX_QUBITS)
        object.__setattr__(self, "gates", tuple(self.gates))
        if len(self.gates) > MAX_GATES:
            raise ValueError(f"Circuits are limited to {MAX_GATES} gates")
        for gate in self.gates:
            if not isinstance(gate, Gate) or any(q >= self.num_qubits for q in gate.qubits):
                raise ValueError("Gate uses a qubit outside the circuit")

    def to_dict(self):
        return {
            "schema_version": 1,
            "num_qubits": self.num_qubits,
            "gates": [g.to_dict() for g in self.gates],
        }

    @classmethod
    def from_dict(cls, value):
        if not isinstance(value, dict) or set(value) != {"schema_version", "num_qubits", "gates"}:
            raise ValueError("Circuit requires exactly schema_version, num_qubits, and gates")
        if type(value["schema_version"]) is not int or value["schema_version"] != 1:
            raise ValueError("Unsupported circuit schema_version (expected 1)")
        if not isinstance(value["gates"], list):
            raise ValueError("gates must be an array")
        return cls(value["num_qubits"], tuple(Gate.from_dict(g) for g in value["gates"]))

    @classmethod
    def load(cls, path: str | Path):
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))

    @property
    def fingerprint(self):
        return hashlib.sha256(json.dumps(self.to_dict(), sort_keys=True).encode()).hexdigest()


def derived_seed(seed: int, *parts) -> int:
    data = json.dumps([seed, *parts], sort_keys=True).encode()
    return int.from_bytes(hashlib.sha256(data).digest()[:4], "big")
