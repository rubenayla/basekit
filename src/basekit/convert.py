"""Exact conversion engine for canonical generic notation."""

from __future__ import annotations

from fractions import Fraction

from .digits import base_to_marker, validate_base, value_to_char
from .notation import ConvertedNumber, format_converted, parse_generic


def to_fraction(parsed) -> Fraction:
    """Convert a parsed canonical number into exact ``Fraction``."""
    base = parsed.base

    int_value = 0
    for digit in parsed.int_digits:
        int_value = int_value * base + digit

    frac_value = Fraction(0, 1)
    for index, digit in enumerate(parsed.frac_digits, start=1):
        frac_value += Fraction(digit, base**index)

    value = Fraction(int_value, 1) + frac_value
    if parsed.sign < 0:
        value = -value
    return value


def from_fraction(value: Fraction, base: int) -> ConvertedNumber:
    """Convert an exact fraction to target base with repeating notation."""
    validate_base(base)
    if not isinstance(value, Fraction):
        value = Fraction(value)

    marker = base_to_marker(base)

    sign = "-" if value < 0 else ""
    absolute = abs(value)

    integer_part = absolute.numerator // absolute.denominator
    remainder = absolute.numerator % absolute.denominator

    int_part = f"{sign}{_encode_non_negative_int(integer_part, base)}"

    if remainder == 0:
        return ConvertedNumber(
            base=base,
            marker=marker,
            int_part=int_part,
            frac_nonrepeat="",
            frac_repeat="",
        )

    seen_remainders: dict[int, int] = {}
    frac_digits: list[str] = []
    denominator = absolute.denominator

    while remainder and remainder not in seen_remainders:
        seen_remainders[remainder] = len(frac_digits)
        remainder *= base
        digit, remainder = divmod(remainder, denominator)
        frac_digits.append(value_to_char(digit))

    if remainder:
        repeat_start = seen_remainders[remainder]
        nonrepeat = "".join(frac_digits[:repeat_start])
        repeat = "".join(frac_digits[repeat_start:])
    else:
        nonrepeat = "".join(frac_digits)
        repeat = ""

    return ConvertedNumber(
        base=base,
        marker=marker,
        int_part=int_part,
        frac_nonrepeat=nonrepeat,
        frac_repeat=repeat,
    )


def convert(value: str, to_base: int) -> str:
    """Convert canonical string to canonical string in target base."""
    parsed = parse_generic(value)
    exact = to_fraction(parsed)
    converted = from_fraction(exact, to_base)
    return format_converted(converted)


def equivalence_chain(value: str, bases: list[int], include_decimal_plain: bool = True) -> str:
    """Return conversion chain string like: ``b_10 = 9_12 = 12``."""
    if not bases:
        raise ValueError("bases cannot be empty")

    parsed = parse_generic(value)
    exact = to_fraction(parsed)

    chain = [format_converted(from_fraction(exact, base)) for base in bases]

    if include_decimal_plain:
        chain.append(_fraction_to_plain_decimal_or_ratio(exact))

    return " = ".join(chain)


def _encode_non_negative_int(number: int, base: int) -> str:
    if number < 0:
        raise ValueError("Expected non-negative integer")
    if number == 0:
        return "0"

    digits: list[str] = []
    n = number
    while n > 0:
        n, remainder = divmod(n, base)
        digits.append(value_to_char(remainder))
    return "".join(reversed(digits))


def _fraction_to_plain_decimal_or_ratio(value: Fraction) -> str:
    """Format exact value as plain base-10 number when finite, else ``num/den``."""
    if value.denominator == 1:
        return str(value.numerator)

    sign = "-" if value < 0 else ""
    numerator = abs(value.numerator)
    denominator = value.denominator

    # Base-10 finite decimal iff reduced denominator has only 2 and/or 5 factors.
    d = denominator
    power_two = 0
    power_five = 0

    while d % 2 == 0:
        power_two += 1
        d //= 2
    while d % 5 == 0:
        power_five += 1
        d //= 5

    if d != 1:
        return f"{value.numerator}/{value.denominator}"

    scale = max(power_two, power_five)
    factor_two = 2 ** (scale - power_five)
    factor_five = 5 ** (scale - power_two)
    scaled_numerator = numerator * factor_two * factor_five

    ten_pow = 10**scale
    whole, remainder = divmod(scaled_numerator, ten_pow)

    if scale == 0 or remainder == 0:
        return f"{sign}{whole}"

    frac = f"{remainder:0{scale}d}".rstrip("0")
    return f"{sign}{whole}.{frac}"
