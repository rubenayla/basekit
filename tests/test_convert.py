from fractions import Fraction

from dozenal_system import convert, equivalence_chain, from_fraction, parse_generic, to_fraction
from dozenal_system.notation import format_converted


def test_core_conversion_examples() -> None:
    assert convert("b_10", 10) == "9_12"
    assert convert("9_12", 12) == "b_10"


def test_roundtrip_integer_samples_across_bases() -> None:
    samples = [0, 1, 2, 10, 35, 97, 1024]
    bases = [2, 3, 8, 10, 12, 16, 36]

    for value in samples:
        for source_base in bases:
            source = format_converted(from_fraction(Fraction(value, 1), source_base))
            for target_base in bases:
                converted = convert(source, target_base)
                roundtrip = convert(converted, source_base)
                assert roundtrip == source


def test_fraction_terminating_and_repeating() -> None:
    # 1/3 is finite in base 12 and repeating in base 10
    assert convert("2_0.1", 12) == "b_0.4"
    assert convert("2_0.1", 10) == "9_0.(3)"


def test_negative_numbers() -> None:
    assert convert("9_-12", 12) == "b_-10"


def test_equivalence_chain_example() -> None:
    assert equivalence_chain("b_10", [12, 10]) == "b_10 = 9_12 = 12"


def test_boundaries_base_2_and_36() -> None:
    assert convert("9_5", 2) == "1_101"
    assert convert("9_35", 36) == "z_z"


def test_to_fraction_exact() -> None:
    parsed = parse_generic("b_10.6")
    value = to_fraction(parsed)
    assert value == Fraction(25, 2)
