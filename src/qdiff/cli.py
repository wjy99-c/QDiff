"""Command-line entry points; imports do not start an experiment."""

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

from . import __version__
from .adapters import versions
from .model import Circuit
from .runner import Config, replay, run


def default_output():
    return Path("results") / datetime.now(UTC).strftime("qdiff-%Y%m%dT%H%M%S%fZ")


def parser():
    root = argparse.ArgumentParser(description="QDiff: local differential testing of quantum SDKs")
    root.add_argument("--version", action="version", version=__version__)
    sub = root.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="Show installed SDK versions without starting a run")
    campaign = sub.add_parser("run", help="Generate, mutate, and compare circuits")
    for key in ("cases", "qubits", "gates", "variants", "shots", "seed"):
        campaign.add_argument(f"--{key}", type=int, default=getattr(Config(), key))
    campaign.add_argument(
        "--backends",
        nargs="+",
        choices=["qiskit", "cirq", "pyquil"],
        default=list(Config().backends),
    )
    campaign.add_argument("--optimization-levels", nargs="+", type=int, default=[0, 3])
    campaign.add_argument("--alpha", type=float, default=0.01)
    campaign.add_argument("--tolerance", type=float, default=1e-8)
    campaign.add_argument("--timeout", type=float, default=60)
    campaign.add_argument("--input", type=Path, help="Version-1 JSON seed circuit")
    campaign.add_argument("--output", type=Path)
    repeat = sub.add_parser(
        "replay", help="Replay a saved case with the recorded circuits and seeds"
    )
    repeat.add_argument("case", type=Path)
    repeat.add_argument("--output", type=Path)
    return root


def main(argv=None):
    argument_parser = parser()
    args = argument_parser.parse_args(argv)
    try:
        if args.command == "doctor":
            print(
                json.dumps(
                    {"qdiff": __version__, "python": sys.version, "packages": versions()}, indent=2
                )
            )
            return 0
        output = (args.output or default_output()).resolve()
        if args.command == "replay":
            result = replay(args.case, output)
        else:
            fields = {key: getattr(args, key) for key in Config.__dataclass_fields__}
            config = Config(**fields)
            circuit = Circuit.load(args.input) if args.input else None
            result = run(config, output, seed_circuit=circuit)
        print(json.dumps({"output": str(output), **result}, indent=2))
        return 1 if result["flagged"] else 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        argument_parser.exit(2, f"qdiff: {exc}\n")
    except KeyboardInterrupt:
        print("qdiff: interrupted; completed case artifacts were retained", file=sys.stderr)
        return 130
