"""Digit and base utilities for generic base-marker notation."""

from __future__ import annotations

DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"
MIN_BASE = 2
MAX_BASE = len(DIGITS)


def validate_base(base: int) -> None:
    """Validate supported base range."""
    if not isinstance(base, int):
        raise ValueError(f"Base must be int, got {type(base).__name__}")
    if base < MIN_BASE or base > MAX_BASE:
        raise ValueError(f"Base must be in [{MIN_BASE}, {MAX_BASE}], got {base}")


def char_to_value(char: str) -> int:
    """Return numeric value for a digit character."""
    if len(char) != 1:
        raise ValueError(f"Expected one digit char, got {char!r}")
    try:
        return DIGITS.index(char.lower())
    except ValueError as exc:
        raise ValueError(f"Invalid digit {char!r}") from exc


def value_to_char(value: int) -> str:
    """Return digit character for a value."""
    if not isinstance(value, int):
        raise ValueError(f"Digit value must be int, got {type(value).__name__}")
    if value < 0 or value >= len(DIGITS):
        raise ValueError(f"Digit value out of range: {value}")
    return DIGITS[value]


def marker_to_base(marker: str) -> int:
    """Decode base marker into numeric base.

    Marker is the digit corresponding to ``base - 1``.
    Example: marker '9' => base 10, marker 'b' => base 12.
    """
    value = char_to_value(marker)
    base = value + 1
    validate_base(base)
    return base


def base_to_marker(base: int) -> str:
    """Encode base into marker digit (base - 1)."""
    validate_base(base)
    return value_to_char(base - 1)
