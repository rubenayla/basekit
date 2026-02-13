from basekit.notation import parse_generic


def test_parse_generic_basic() -> None:
    parsed = parse_generic("b_10")
    assert parsed.base == 12
    assert parsed.sign == 1
    assert parsed.int_digits == [1, 0]
    assert parsed.frac_digits == []


def test_parse_uppercase_normalized() -> None:
    parsed = parse_generic("B_1a")
    assert parsed.base == 12
    assert parsed.int_digits == [1, 10]


def test_parse_negative_fraction() -> None:
    parsed = parse_generic("9_-12.5")
    assert parsed.base == 10
    assert parsed.sign == -1
    assert parsed.int_digits == [1, 2]
    assert parsed.frac_digits == [5]


def test_parse_invalid_inputs() -> None:
    bad_values = [
        "b__10",
        "b_",
        "_10",
        "0_10",
        "b_1g",
        "b_10.",
        "bb_10",
    ]
    for value in bad_values:
        try:
            parse_generic(value)
            assert False, f"Expected ValueError for {value!r}"
        except ValueError:
            pass
