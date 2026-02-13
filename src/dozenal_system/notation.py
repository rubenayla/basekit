"""Parsing and formatting for canonical generic notation.

Canonical syntax:
    <base-marker>_<number>

Examples:
    b_10   (base 12 marker 'b', number '10')
    9_12   (base 10 marker '9', number '12')
"""

from __future__ import annotations

from dataclasses import dataclass
import re

from .digits import base_to_marker, char_to_value, marker_to_base

_CANONICAL_RE = re.compile(r"^(?P<marker>[0-9a-zA-Z])_(?P<number>-?[0-9A-Za-z]+(?:\.[0-9A-Za-z]+)?)$")


@dataclass(frozen=True)
class ParsedNumber:
    """Parsed canonical number in an arbitrary base."""

    base: int
    sign: int
    int_digits: list[int]
    frac_digits: list[int]


@dataclass(frozen=True)
class ConvertedNumber:
    """Canonical output parts produced from exact conversion."""

    base: int
    marker: str
    int_part: str
    frac_nonrepeat: str
    frac_repeat: str


def parse_generic(value: str) -> ParsedNumber:
    """Parse canonical generic notation ``<base-marker>_<number>``.

    Accepted examples: ``b_10``, ``9_-12``, ``f_7a.2``
    Repeating input with parentheses is intentionally not supported in v1.
    """
    if not isinstance(value, str):
        raise ValueError(f"Value must be str, got {type(value).__name__}")

    text = value.strip()
    match = _CANONICAL_RE.match(text)
    if not match:
        raise ValueError(
            "Invalid canonical format. Expected '<base-marker>_<number>', "
            "e.g. 'b_10' or '9_-12.5'"
        )

    marker = match.group("marker")
    number = match.group("number").lower()
    base = marker_to_base(marker)

    sign = -1 if number.startswith("-") else 1
    unsigned = number[1:] if sign < 0 else number

    int_part, dot, frac_part = unsigned.partition(".")
    if not int_part:
        raise ValueError("Integer part cannot be empty")
    if dot and not frac_part:
        raise ValueError("Fractional part cannot be empty when '.' is present")

    int_digits = [_parse_digit(ch, base) for ch in int_part]
    frac_digits = [_parse_digit(ch, base) for ch in frac_part] if frac_part else []

    return ParsedNumber(base=base, sign=sign, int_digits=int_digits, frac_digits=frac_digits)


def format_converted(converted: ConvertedNumber) -> str:
    """Format converted parts to canonical generic notation string."""
    marker = converted.marker or base_to_marker(converted.base)
    frac = converted.frac_nonrepeat
    if converted.frac_repeat:
        frac = f"{frac}({converted.frac_repeat})"

    number = converted.int_part if not frac else f"{converted.int_part}.{frac}"
    return f"{marker}_{number}"


def _parse_digit(char: str, base: int) -> int:
    value = char_to_value(char)
    if value >= base:
        raise ValueError(f"Digit {char!r} is invalid for base {base}")
    return value
