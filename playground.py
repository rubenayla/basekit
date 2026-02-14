from fractions import Fraction
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from basekit import base, dozenal as doz


def main() -> None:
    print("Basekit playground")
    print("------------------")

    a = doz(100)
    b = 144
    print(f"doz(100) -> {a}")
    print(f"doz(100) == 144 -> {a == b}")
    print(f"doz('b_100') -> {doz('b_100')}")
    print(f"doz('9_144') -> {doz('9_144')}")
    print(f"base(10)('9_144') -> {base(10)('9_144')}")

    ternary = base(3)
    print(f"base(3)(10) -> {ternary(10)}")

    print(f"doz.fmt(144) -> {doz.fmt(144)}")
    print(f"doz.fmt(144, marked=True) -> {doz.fmt(144, marked=True)}")

    one_third = Fraction(1, 3)
    print(f"base(10).fmt(1/3) -> {base(10).fmt(one_third)}")


if __name__ == "__main__":
    main()
