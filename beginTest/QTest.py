"""Compatibility entry point for the maintained QDiff CLI.

The original Python 3.7 runner is preserved in legacy_QTest.py for reference.
Install this checkout with `python -m pip install -e '.[all]'` before running.
"""

import sys

if __name__ == "__main__":
    try:
        from qdiff.cli import main
    except ModuleNotFoundError as exc:
        raise SystemExit("Install QDiff first: python -m pip install -e '.[all]'") from exc
    arguments = sys.argv[1:]
    if not arguments or arguments[0] not in ("run", "replay", "doctor", "--version"):
        arguments = ["run", *arguments]
    raise SystemExit(main(arguments))
