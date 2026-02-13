"""Command-line interface for basekit conversions."""

from __future__ import annotations

import argparse
import sys

from .convert import convert, equivalence_chain


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="basekit", description="Convert numbers across bases 2..36")
    subparsers = parser.add_subparsers(dest="command", required=True)

    convert_parser = subparsers.add_parser("convert", help="Convert one canonical value")
    convert_parser.add_argument("value", help="Canonical value like b_10 or 9_-12.5")
    convert_parser.add_argument("--to-base", type=int, required=True, help="Target base in range 2..36")

    chain_parser = subparsers.add_parser("chain", help="Build equivalence chain across bases")
    chain_parser.add_argument("value", help="Canonical value like b_10")
    chain_parser.add_argument("--bases", required=True, help="Comma-separated base list, e.g. 12,10")

    args = parser.parse_args(argv)

    try:
        if args.command == "convert":
            print(convert(args.value, args.to_base))
            return 0

        if args.command == "chain":
            bases = _parse_bases_csv(args.bases)
            print(equivalence_chain(args.value, bases, include_decimal_plain=True))
            return 0

        parser.error("Unknown command")
        return 2
    except (TypeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


def _parse_bases_csv(raw: str) -> list[int]:
    parts = [part.strip() for part in raw.split(",")]
    if not parts or any(part == "" for part in parts):
        raise ValueError("--bases must be a comma-separated list of integers")

    bases: list[int] = []
    for part in parts:
        try:
            bases.append(int(part))
        except ValueError as exc:
            raise ValueError(f"Invalid base value: {part!r}") from exc
    return bases


if __name__ == "__main__":
    raise SystemExit(main())
