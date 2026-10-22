"""Isolated SDK process; all inputs and outputs are JSON data."""

import json
import sys
import traceback

from .adapters import execute
from .model import Circuit


def main():
    try:
        request = json.load(sys.stdin)
        result = execute(
            Circuit.from_dict(request["circuit"]),
            request["backend"],
            request["shots"],
            request["seed"],
            request["optimization_level"],
        )
        json.dump(result, sys.stdout, allow_nan=False)
        return 0
    except Exception:
        traceback.print_exc(file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
