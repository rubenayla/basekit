"""Ergonomic base context API.

Examples:
    from basekit import base, dozenal as doz
    doz(100) == 144
    base(3)(10) == 3
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .convert import from_fraction, to_fraction
from .digits import char_to_value, validate_base
from .notation import parse_generic


@dataclass(frozen=True)
class BaseContext:
    """Context for parsing/formatting numbers in a fixed radix."""

    radix: int

    def __post_init__(self) -> None:
        validate_base(self.radix)

    def __call__(self, value: int | str) -> int | Fraction:
        """Parse digits in this base into Python numeric value.

        - int input is interpreted as a digit-sequence token (e.g., 100 in base 12 -> 144)
        - str input supports optional leading sign and optional single '.'
        - str input also accepts canonical marker notation, e.g. 'b_100' or '9_144'
        """
        if isinstance(value, int):
            token = str(value)
        elif isinstance(value, str):
            token = value.strip()
        else:
            raise TypeError(f"Unsupported value type: {type(value).__name__}")

        if token == "":
            raise ValueError("Empty token")

        if isinstance(value, str) and "_" in token:
            exact = to_fraction(parse_generic(token))
            return int(exact) if exact.denominator == 1 else exact

        sign = -1 if token.startswith("-") else 1
        unsigned = token[1:] if sign < 0 else token

        int_part, dot, frac_part = unsigned.partition(".")
        if not int_part:
            raise ValueError("Integer part cannot be empty")
        if dot and not frac_part:
            raise ValueError("Fractional part cannot be empty when '.' is present")
        if unsigned.count(".") > 1:
            raise ValueError("Only one decimal point is allowed")

        int_value = 0
        for ch in int_part.lower():
            digit = _digit_in_base(ch, self.radix)
            int_value = int_value * self.radix + digit

        frac_value = Fraction(0, 1)
        for i, ch in enumerate(frac_part.lower(), start=1):
            digit = _digit_in_base(ch, self.radix)
            frac_value += Fraction(digit, self.radix**i)

        result = Fraction(int_value, 1) + frac_value
        if sign < 0:
            result = -result
        return int(result) if result.denominator == 1 else result

    def fmt(self, value: int | Fraction, marked: bool = False) -> str:
        """Format a base-10 numeric value into this base.

        Default output is unmarked digits (e.g. '100').
        If marked=True output canonical marker notation (e.g. 'b_100').
        """
        exact = value if isinstance(value, Fraction) else Fraction(value)
        converted = from_fraction(exact, self.radix)

        frac = converted.frac_nonrepeat
        if converted.frac_repeat:
            frac = f"{frac}({converted.frac_repeat})"

        number = converted.int_part if not frac else f"{converted.int_part}.{frac}"
        if marked:
            return f"{converted.marker}_{number}"
        return number


def base(radix: int) -> BaseContext:
    """Create a base context for ergonomic parse/format operations."""
    return BaseContext(radix)


dozenal = base(12)


def _digit_in_base(ch: str, base_value: int) -> int:
    digit = char_to_value(ch)
    if digit >= base_value:
        raise ValueError(f"Digit {ch!r} is invalid for base {base_value}")
    return digit
